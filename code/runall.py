# FILE: pubmedDB.py
# AUTHOR: Hanie Samimi
# CREATE DATE: 10 April 2020

# PACKAGES
from Bio import Medline
import pymongo
import re
import os
import pdb

# CREATE DB
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["pubmedDB"]
mycol = mydb["Article"]


# PARSER
def parser(inputFile):

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with open(inputFile) as handle:
        records = Medline.parse(handle)
        count = 0
        for record in records:
            abstractVal = record.get('AB')
            titleVal = record.get('TI')
            keywordsVal = record.get('OT')
            meshVal = record.get('MH')
            count +=1
            mycol.insert_one({"title": titleVal, "Abstract": abstractVal, "keywords": keywordsVal, "meshterms": meshVal})
        print(count)


# MAIN

# call perl script
# os.system("cd ../data/ | perl ../code/perlpipe3.pl")


# call parser
os.chdir(os.path.dirname(os.path.abspath(__file__)))
parser("../data/perloutput.txt")

