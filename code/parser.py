from Bio import Medline
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
with open("../data/perloutput.txt") as handle:
    records = Medline.parse(handle)
    count = 0
    for record in records:
        if record['MH']:
            print(record['MH'])
        count += 1
    print(count)