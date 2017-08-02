# About
Here are some python scripts I wrote. Most of them process fasta/fastq/gb
files.

From now on, I will add some descriptions for each program.

You can type 
>python3 pyfile -h

or

>python3 pyfile

to print usage of each program.

You can ask me any question about these programs via
**wpwupingwp@outlook.com** .

# Requirement

1. [python3](https://www.python.org/downloads/)

    Be sure to install python3 rather than python 2.7. Besides, to use
    subprocess.run(), you would better install python **3.5** or above.

2. [biopython](http://biopython.org/wiki/Download)

3. [BLAST Suite](https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download)

And notice that all scripts were just tested on Linux system, although
theoretically they may works fine on Windows.

# Batch

Many of programs in this repository support batch mode. See examples below.
Note that "\*.fasta" is files you want to process, and _i_ is variable you can
use other name if you want. And parameters of program was omitted.

## Microsoft Windows

> for i in (\*.fasta) do python program.py %i

## Linux

> for i in \*.fasta;do python3 program.py $i

# Help information

Just type:

> python3 program.py -h

# This folder

## parallel.py

Parallel run other programs.

### Usage

> python3 parallel.py "command %i" "file"

Make sure you do not omit quotation mark.

The "%i" in "command" is the filename. You can use glob pattern in "file".

### example

> python3 parallel.py "python3 gb2fasta.py %i" "\*.gb" 

## split.py

Split fasta or fastq files according to given "-s".


### Usage

> python3 split.py -i input_file -s 10000000 -o output_path

It only support fasta or fastq file. The option "-s" means how many sequences
you want in one file. The default value is 100000. You can change output
folder by "-o".

### Example

> python3 split.py -i pe150.fastq -s 100000 -o pe150\_split

## convert.py

Convert file format.

### Usage

> python3 convert.py old_file_name old_format new_file_name new_format

### Example

> python3 convert.py Zea.nex nexus Zea.fasta fasta

## xml2fasta.py

Convert xml format BLAST result to fasta format and output result table.

### Usage

1. BLAST your sequences.
2. Download *xml* format result.
3. Run

> python3 xml2fasta.py BlastResult.xml

> python3 xml2fasta.py BlastResult.xml -s

> python3 xml2fasta.py BlastResult.xml -ss

*If you use option "-s", it will only proces first hsp for each hit in every
query sequence.*

*If you use option "-ss", it will only process first hsp of first hit for each
query sequence.*

Note that for Microsoft Windows user, maybe you should replace "python3" with
"python".

### Result

- fasta file. The first sequence is your query sequence, and others are
  matched fragment sequences of the query.
- tsv file. Table for simple analyze.
- NotFound.log Hint for those query sequences did not found match by BLAST.

## trim.py

Trim fragment in given fasta file, or replace trimmed bases with 'N'.

### Usage

> python3 trim.py input.fasta start-end -n

Here _start_ and _end_ are integers, and end could larger than length of
sequence if you want to cut off sequence's tail.

If you set option "-n", then all bases you want to trim will become "N".

### Example

> python3 trim.py rbcL.fasta 200-250

## no_same.py

Remove identical sequence in give fasta/nexus file. New file will be write
into ".new" with the same format of input file.

Duplicated sequences will be printed on screen.

## Usage

> python3 no_same.py input_file

### Example

> python3 no_same.py cbs.fasta

## vlookup_assistant.py

Expand a given table according to range.

Input table (CSV format) looks like this:

>    A,B,C

It will generate a new table:

>    D,E 

where D was expanded from range(B, C) and E is related A.

## add_gene_name.py

Rename fasta files in one directory according to gene info provided by the
first record in each file

## pick.py

Pick fasta record according to id list

## screen.py

Screen sequence assembled by _spades_ according to sequence length and
coverage info in sequence id.

**Warning: This program use regular expression to recognize infomation, it may
generate wrong output when it was used on other sequence if format.**

# old

Some old code.

# cp

Some program to deal with genbank files, most of them belongs to chloroplast.

# plot

Use *matplotlib* to draw figures for my master thesis.

# inhibitor

Some code to analyze data from microreader. For Cystathionine beta-synthase
inhibitor project.

# Template

Some useful code fragments.

# 1kp

Programs for [1kp](http://www.onekp.com/public_data.html).
