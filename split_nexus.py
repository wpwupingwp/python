#!/usr/bin/python3

from Bio.Nexus import Nexus
from sys import argv

data = Nexus.Nexus(argv[1])
data.write_nexus_data_partitions(filename='split',
                                 charpartition=data.charsets)
