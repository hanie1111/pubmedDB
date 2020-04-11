# AUTHOR: Hanie Samimi
# CREATE DATE: 11 April 2020

To run this project:
	1- Run perlpipeline3.pl from pubmedDB/result/. 
	   This script has been generated using ebot tool and pubmedDB/result/inputID.txt as its input.
	   The inputID.txt contains a list of pubmedIDs from question 1.
	   Results will be saved at pubmedDB/result/perloutput.txt
	   To regenrate perlpipeline3.pl it, visit https://www.ncbi.nlm.nih.gov/Class/PowerTools/eutils/ebot/ebot.cgi
	
	2- Run runall.py
	   It reads records from pubmedDB/result/perloutput.txt, stores them in pubmedDB database and runs a set of queries on
	   pubmedDB.
