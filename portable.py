#!/usr/bin/python3

import datetime
import re
import sqlite3
import urllib.request
import warnings

from Bio import BiopythonDeprecationWarning
from Bio import Entrez
from Bio import SeqIO
from Bio.Seq import MutableSeq

warnings.simplefilter("ignore",BiopythonDeprecationWarning)

def Parser():

    '''Base on annotations in genbank files to extract fragments from Chloroplast Genome Sequence.'''

    Taxon=int(Record.features[0].qualifiers["db_xref"][0][6:])
    Organism=Record.annotations["organism"]
    Accession=Record.annotations["accessions"][0]
    Gene=[]
    All=[]
    Type="whole"
    Start=1
    End=len(Record)
    Sequence=str(Record.seq)
    Name=Organism
    Strand=1
    rec=[Taxon,Organism,Accession,Name,Type,Start,End,Strand,Sequence,Date]
    All.append(rec)
    global SeqDB
    SeqDB=[]
    for i in Record.features:
        if i.type=="gene" and "gene" in i.qualifiers:
            if i.location_operator!="join":
                Type="gene"
                Start=int(i.location.start)
                End=int(i.location.end)
                Sequence=str(Record.seq[Start:End])
                Name=str(i.qualifiers["gene"][0])
                Strand=str(i.location.strand)
                rec=[Taxon,Organism,Accession,Name,Type,Start,End,Strand,Sequence,Date]
                Gene.append(rec)
            elif i.location_operator=="join":
                Type="gene"
                Start=int(i.sub_features[0].location.start)
                End=int(i.sub_features[0].location.end)
                Name=str(i.qualifiers["gene"][0])
                Strand=str(i.location.strand)
                Sequence=""
                rec=[Taxon,Organism,Accession,Name,Type,Start,End,Strand,Sequence,Date]
                Gene.append(rec)
                Start=int(i.sub_features[1].location.start)
                End=int(i.sub_features[1].location.end)
                Sequence="".join([str(Record.seq[Start:End]),str(Record.seq[Start:End])])
                rec=[Taxon,Organism,Accession,Name,Type,Start,End,Strand,Sequence,Date]
        elif i.type=="CDS" and "gene" in i.qualifiers:
            Type="cds"
            Start=int(i.location.start)
            End=int(i.location.end)
            Sequence=str(Record.seq[Start:End])
            Name=str(i.qualifiers["gene"][0]).replace(" ","_")
            Strand=str(i.location.strand)
            rec=[Taxon,Organism,Accession,Name,Type,Start,End,Strand,Sequence,Date]
            All.append(rec)
        elif i.type=="tRNA" and "gene" in i.qualifiers:
            Type="tRNA"
            Start=int(i.location.start)
            End=int(i.location.end)
            Sequence=str(Record.seq[Start:End])
            if len(Sequence)>=100:
                Sequence=""
            Name=str(i.qualifiers["gene"][0]).replace(" ","_")
            Strand=str(i.location.strand)
            rec=[Taxon,Organism,Accession,Name,Type,Start,End,Strand,Sequence,Date]
            All.append(rec)
        elif i.type=="rRNA":
            Type="rRNA"
            Start=int(i.location.start)
            End=int(i.location.end)
            Sequence=str(Record.seq[Start:End])
            Name=str(i.qualifiers["product"][0]).replace(" ","_")
            Strand=str(i.location.strand)
            rec=[Taxon,Organism,Accession,Name,Type,Start,End,Strand,Sequence,Date]
            All.append(rec)
        elif i.type=="exon" and "gene" in i.qualifiers :
            Type="exon"
            Start=int(i.location.start)
            End=int(i.location.end)
            Sequence=str(Record.seq[Start:End])
            if "number" in i.qualifiers:
                Name="_".join([str(i.qualifiers["gene"][0]),"exon",str(i.qualifiers["number"][0])])
            else:
                Name="_".join([str(i.qualifiers["gene"][0]),"exon"])
            Strand=int(i.location.strand)
            rec=[Taxon,Organism,Accession,Name,Type,Start,End,Strand,Sequence,Date]
            All.append(rec)
        elif i.type=="intron" and "gene" in i.qualifiers:
            Type="intron"
            Start=int(i.location.start)
            End=int(i.location.end)
            Sequence=str(Record.seq[Start:End])
            Strand=str(i.location.strand)
            if "number" in i.qualifiers:
                Name="_".join([str(i.qualifiers["gene"][0]),"intron",str(i.qualifiers["number"][0])])
            else:
                Name="_".join([str(i.qualifiers["gene"][0]),"intron"])
            rec=[Taxon,Organism,Accession,Name,Type,Start,End,Strand,Sequence,Date]
            All.append(rec)
    Gene.sort(key=lambda x:x[5])

    for i in range(len(Gene)-1):
        Type="spacer"
        This=Gene[i]
        Next=Gene[i+1]
        Tail=This[6]+1
        Head=Next[5]-1
        Sequence=str(Record.seq[Tail:Head])
        Name="_".join(["-".join([This[3],Next[3]]),"Spacer"])
        Strand=0
        rec=[Taxon,Organism,Accession,Name,Type,Start,End,Strand,Sequence,Date]
        All.append(rec)
    All.extend(Gene)

    SeqDB.extend(All)
    return 

def InitSeq():

    '''Init Sequence Database'''

    con=sqlite3.connect("./test/DB")
    cur=con.cursor()
    cur.execute("create table if not exists main (Taxon int,Organism text,Accession text,Name text,Type text,Head int,Tail int, Strand text,Sequence text,Date text,ID integer PRIMARY KEY);")
    for row in SeqDB:
        if row[8]!="":
            cur.execute("insert into main (Taxon,Organism,Accession,Name,Type,Head,Tail,Strand,Sequence,Date) values (?,?,?,?,?,?,?,?,?,?);",(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]))
    con.commit()
    cur.close()
    con.close()
    print("Done.\n")
    return
    
def SeqQuery():

    '''Sequence query function, to be continued.'''

    Querytype=input("1.Specific fragment\n2.Specific Organism\n3.Specific gene\n4.All\n")
    if Querytype not in ["1","2","3","4"]:
        raise ValueError('wrong input!\n')
    con=sqlite3.connect("./test/DB")
    cur=con.cursor()
    if Querytype=="1":
        Organism=input("Organism:\n")
        Gene=input("Gene:\n")
        Type=input("Fragment type(gene,cds,rRNA,tRNA,exon,intron,spacer):\n")
        cur.execute("select Taxon,Organism,Name,Type,Strand,Sequence from main where Name like ? and Type=? and Organism=?",('%'+Gene+'%',Type,Organism))
        Result=cur.fetchall()
    elif Querytype=="2":
        Organism=input("Organism:\n")
        Type=input("Fragment type(gene,cds,rRNA,tRNA,exon,intron,spacer,whole,fragments):\n")
        if Type=="fragments":
            cur.execute("select Taxon,Organism,Name,Type,Strand,Sequence,Head from main where Organism=?  order by Head",(Organism,))
        else:
            cur.execute("select Taxon,Organism,Name,Type,Strand,Sequence,Head from main where Organism=? and Type=? order by Head",(Organism,Type))
        Result=cur.fetchall()
    elif Querytype=="3":
        Gene=input("Gene:\n")
        Type=input("Fragment type(gene,cds,rRNA,tRNA,exon,intron,spacer):\n")
        cur.execute("select Taxon,Organism,Name,Type,Strand,Sequence from main where Name like ? and Type=? order by Taxon",('%'+Gene+'%',Type))
        Result=cur.fetchall()
    elif Querytype=="4":
        cur.execute("select Taxon,Organism,Name,Type,Strand,Sequence,Head from main order by Taxon")
        Result=cur.fetchall()

    All=[]
    for i in Result:
        Title="|".join([str(i[0]),i[1],i[2],i[3]])
        Sequence=MutableSeq(i[5])
        if i[4]=="-1":
            Sequence.seq=Sequence.reverse_complement()
        Record=[Title,Sequence]
        All.append(Record)

    Output=input("Enter output filename:\n")
    Fileout=open(".".join([Output,"fasta"]),"w")
    for i in All:
        Fileout.write(">%s\n%s\n"%(i[0],i[1]))
    cur.close()
    con.close()
    Fileout.close()
    print("Done.\n")
    return 

def UpdateSeqDBFromGenbank():
    '''Update Sequence database from Genbank, need time to download.'''

    Down=urllib.request.urlopen("http://www.ncbi.nlm.nih.gov/genomes/GenomesGroup.cgi?taxid=2759&opt=plastid").read().decode("utf-8")
    GenomeList=re.findall("((?<=nuccore/)[0-9]{9})",Down)
    Entrez.email="wpwupingwp@outlook.com"
    handle=Entrez.read(Entrez.epost(db="nuccore",id=",".join(GenomeList)))
    W=handle["WebEnv"]
    K=handle["QueryKey"]
    GenomeContent=Entrez.efetch(db="nuccore",webenv=W,query_key=K,rettype="gb",retmode="text")
    Output=open("genbank","w")
    Output.write(GenomeContent.read())
    Output.close()
    UpdateSeqFromFile("genbank")
    
def UpdateSeqFromFile(FileIn):
    '''Update Sequence database from private file.'''
    global Record
    handle=open(FileIn,"r")
    Records=SeqIO.parse(FileIn,"genbank")
    for Record in Records:
        Parser()
    InitSeq()
    handle.close()
    return

def InitTaxon():
    
    '''Init Taxon database from file. to be continued(add download function'''

    Id=dict()
    Data=list()
    Name=dict()
    Specie=list()
    Son=dict()
    GreatSon=dict()
    Parent=dict()
    Rank=dict()
    global Taxon
    Taxon=list()
    with open('./test/name','r') as In:
        Raw=list(In.readlines())
        for record in Raw:
            add=record.replace('\n','').split(sep='|')
            if add[0] not in Name or add[2]=='scientific name':
                Name[add[0]]=add[1]
    with open('./test/nodes','r') as In:
        Raw=list(In.readlines())
        for record in Raw:
            add=record.replace('\n','').split(sep=' ')
            Id[add[0]]=add[1]
            Rank[add[0]]=add[2]
            if add[2]=='species':
                Specie.append(add[0])
    for specie in Specie:
        record=[specie,]
        while Id[specie]!='1' :
            record.append(Id[specie])
            specie=Id[specie]
#        if '33090' in record:
#            record.pop()
#            record.pop()
            Data.append(record)
    for data in Data:
        for n in range(len(data)):
            if data[n] not in Parent:
                Parent[data[n]]=data[(n+1):]
            if n==0:
                continue
            if data[n] not in Son:
                Son[data[n]]={data[n-1],}
            else:
                Son[data[n]].add(data[n-1])
            if data[n] not in GreatSon:
                GreatSon[data[n]]={data[0],}
            else:
                GreatSon[data[n]].add(data[0])
    for specie in Name.items():
        if specie[0] not in Son:
            Son[specie[0]]=set()
        if specie[0] not in Parent:
            Parent[specie[0]]=list()
        if specie[0] not in GreatSon:
            GreatSon[specie[0]]=set()
        record=[specie[0],Name[specie[0]],Rank[specie[0]],Son[specie[0]],Parent[specie[0]],GreatSon[specie[0]]]
        Taxon.append(record)

    con=sqlite3.connect('./test/DB')
    cur=con.cursor()
    cur.execute('create table if not exists taxon (Id text,Name text,Rank text,Son text,Parent text,GreatSon text);')
    for line in Taxon:
        Son=' '.join(line[3])
        Parent=' '.join(line[4])
        GreatSon=' '.join(line[5])
        cur.execute('insert into taxon (Id,Name,Rank,Son,Parent,GreatSon) values (?,?,?,?,?,?);',(line[0],line[1],line[2],Son,Parent,GreatSon))
    con.commit()
    cur.close()
    con.close()
    print('Done.\n')
    return
    
def TaxonQueryAuto(Id,Rank):

    '''Taxon query for seqquery, may be remove'''

    con=sqlite3.connect('./test/DB')
    cur=con.cursor()
    cur.execute('select Parent from taxon where Id=? or Name=?;',(Id,'%'+Name+'%'))
    Result=cur.fetchall()
    Rank=dict()
    for record in Record:
        Rank[result[0]]=result[1]
    '''to be contiuned'''

def TaxonQueryNoAuto():

    '''Interactive query taxon database.'''

    while True:
        Querytype=input('1.by id\n2.by name\n')
        if Querytype not in ['1','2']:
            return
        con=sqlite3.connect('./test/DB')
        cur=con.cursor()
        if Querytype=='1':
            Id=input('taxon id:\n')
            cur.execute('select * from taxon where Id=?;',(Id,))
            Result=cur.fetchall()
        elif Querytype=='2':
            Name=input('scientific name:\n')
            cur.execute('select * from taxon where Name like ?;',('%'+Name+'%',))
            Result=cur.fetchall()
        cur.execute('select Id,Name from taxon;')
        Result2=cur.fetchall()
        cur.close()
        con.close()
        Namedict={'':''}
        for item in Result2:
            Namedict[item[0]]=item[1]
        for i in Result:
            Id=i[0]
            Name=i[1]
            Rank=i[2]
            Son=i[3].split(sep=' ')
            Sonname=list()
            for item in Son:
                Sonname.append(Namedict[item])
            Parent=i[4].split(sep=' ')
            Parentname=list()
            for item2 in Parent:
                Parentname.append(Namedict[item2])
            GreatSon=i[5].split(sep=' ')
            GreatSonname=list()
            for item3 in GreatSon:
                GreatSonname.append(Namedict[item3])
            handle=open('out.txt','a',encoding='utf-8')
            handle.write(''.join(['id      : ',Id,'\n']))
            handle.write(''.join(['name    : ',Name,'\n']))
            handle.write(''.join(['rank    : ',Rank,'\n']))
            handle.write(''.join(['parent  : ','->'.join(Parentname),'\n']))
            handle.write(''.join(['son     : ',','.join(Sonname),'\n']))
            handle.write(''.join(['greatson: ',','.join(GreatSonname),'\n\n']))

#__main()__

'''main function, entrance of the program.'''

Option=input("Select:\n1.Update database from GenBank\n2.Add pvirate data\n3.Query\n")
Date=str(datetime.datetime.now())[:19].replace(" ","-")
if Option=="1":
    UpdateSeqFromGenbank()
elif Option=="2":
    FileIn=input("Genbank format filename:\n")
    UpdateSeqFromFile(FileIn)
elif Option=="3":
    SeqQuery()
else:
    print("Input error!\n")
