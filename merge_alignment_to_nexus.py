#!/usr/bin/python3

from Bio.Nexus import Nexus
from glob import glob

alignments = list(glob('*.aln'))
name_data = [(name, Nexus.Nexus(name)) for name in alignments]
combine = Nexus.combine(name_data)
combine.write_nexus_data(filename=open('merge.nexus', 'w'))
