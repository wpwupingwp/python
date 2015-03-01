import sys
from Bio import SeqIO

def main():
    handle=open(sys.argv[1],'r')
    data=SeqIO.parse(handle,'gb')
    target=list()
    for record in data:
        organism=record.annotations['organism'].replace(' ','_')
        accession=record.annotations['accessions'][0]
        sequence=str(record.seq)
        name=''
        for feature in record.features:
            if feature.type=='misc_feature': 
                name=str(feature.qualifiers['note'][0]).replace(' ','_')
            elif feature.type=='gene' and 'gene' in feature.qualifiers:
                name=str(feature.qualifiers['gene'][0]).replace(' ','_')
        target.append([organism,accession,name,sequence])
    handle_out=open(sys.argv[1].replace('.gb','.fasta'),'w')
    for item in target:
        handle_out.write('>')
        handle_out.write('|'.join([item[0],item[1],item[2]]))
        handle_out.write('\n')
        handle_out.write(item[3])
        handle_out.write('\n')
    print('Done.')

if __name__=='__main__':
    main()