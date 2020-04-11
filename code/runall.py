# FILE: pubmedDB.py
# AUTHOR: Hanie Samimi
# CREATE DATE: 10 April 2020

# PACKAGES
from Bio import Medline
import pymongo
import re
import os
import pdb
import time

# CREATE DB
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["pubmedDB"]
mycol = mydb["Article"]

# PARSER
def parser(inputFile):
    print("Creating pubmedDB database ...")

    #Change current directory to where the code is saved since inputFile is a relational address:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with open(inputFile) as handle:
        # Each record is related to one article
        records = Medline.parse(handle)
        count = 0
        # Fetch desired info of each record
        for record in records:
            abstractVal = record.get('AB')
            titleVal = record.get('TI')
            keywordsVal = record.get('OT')
            meshVal = record.get('MH')
            count +=1
            # Insert record into pubmedDB
            mycol.insert_one({"title": titleVal, "abstract": abstractVal, "keywords": [keywordsVal], "meshterms": [meshVal]})
        print("Inserted {} records into pubmedDB".format(count))

# MAIN
# START TIME
start_time = time.clock()
print(time.strftime('%X %x %S %Z'))

# call parser
# Parse the medline format file (downaloded using ../result/perlpipeline3.pl)
os.chdir(os.path.dirname(os.path.abspath(__file__)))
parser("../data/perloutput.txt")

# INDEX
# Indexing pubmedDB based on words in both abstract and title for faster query processing
mycol.create_index([("abstract",pymongo.TEXT),("title",pymongo.TEXT)])

# ANALYZE pubmedDB
print("Analyzing the pubmedDB ...")
words = ["bacterial", "pathogens"]
phrase = "\"bacterial pathogens\""
# db.Article.distinct("abstract",{$text: {$search: "bacterial"}}).length
q1 = mycol.distinct("title",{"$text": {"$search": words[0],"$caseSensitive":False}}) #Articles contain the WORD "bacterial"
q2 = mycol.distinct("title",{"$text": {"$search": words[1],"$caseSensitive":False}}) #Articles contain the WORD "pathogens"
q3 = set(q1).intersection(set(q2)) #Articles contain both WORDs "bacterial" and "pathogens"
q4 = mycol.distinct("title",{"$text": {"$search": phrase,"$caseSensitive":False}}) #Articles contain the PHRASE "bacterial pathogens"

print("Summary:")
print("Number of articles contain the word \'bacterial\': {}".format(len(q1)))
print("Number of articles contain the word \'pathogens\': {}".format(len(q2)))
print("Number of articles contain both words \'bacterial\' and \'pathogens\' {}".format(len(q3)))
print("Number of articles contain the phrase \'bacterial pathogens\': {}".format(len(q4)))

#END TIME
print(time.strftime('%X %x %S %Z'))

