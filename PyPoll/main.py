"""
date: 2018-09-01
author: Marie-Oceane
description: 
In this challenge, you are tasked with helping a small, rural town modernize its vote-counting process. (Up until now, Uncle Cleetus had been trustfully tallying them one-by-one, but unfortunately, his concentration isn't what it used to be.)
You will be give a set of poll data called election_data.csv. 

The dataset is composed of three columns: Voter ID, County, and Candidate. 

Your task is to create a Python script that analyzes the votes and calculates each of the following:
-> The total number of votes cast
-> A complete list of candidates who received votes
-> The percentage of votes each candidate won
-> The total number of votes each candidate won
-> The winner of the election based on popular vote.

In addition, your final script should both print the analysis to the terminal and export a text file wit

"""
import csv
import logging
import numpy as np

# Logging set-up
#---------------
# this will allow us to write in a text-file and in the terminal at the same time
logfile = "results.txt"
open(logfile, 'w').close()  #to delete the existing content of the file
# we only need to set up the INFO level
level = logging.INFO
format = '%(message)s'
handlers = [logging.FileHandler(logfile), logging.StreamHandler()]
logging.basicConfig(level = level, format = format, handlers = handlers)

#Initializing
#------------
names = [] # list of the candidates
nbVotes = []    # nb of votes for each candidate
csvpath = "election_data.csv"

# Counting the votes
#-------------------
with open(csvpath, newline='',encoding='utf-8') as csvfile:
    #open the csvfile
    csvreader = csv.reader(csvfile, delimiter=',')
    #skip the header line
    next(csvreader,None)    
    #looping on each row
    for row in csvreader:
        if names.count(row[2]) == 1:    # if data has already been collected for the candidate
            nbVotes[names.index(row[2])] += 1   #incrementing the number of votes            
        else: # if the candidate has not been parsed yet
            names.append(row[2])    # we add the name in the list
            nbVotes.append(1)       # consider its first vote
            
# Processing the counted votes (total, pc of votes, winner)
#-------------------------------------------------
total = sum(nbVotes)    # total nb of votes
pc_votes = [votes/total*100 for votes in nbVotes] # percents of votes for each candidate
winner = names[np.argmax(nbVotes)]  # Name of the winner

# Printing the results
#--------------------
# first we can zip the values
results = zip(names, pc_votes, nbVotes)
logging.info("Election results")
logging.info("----------------------")
logging.info(f'Total votes: {total}')
logging.info('----------------------')
# results for each candidate
for res in results:
    logging.info("%s: %.1f%% (%i)"%(res))
logging.info('----------------------')    
# Winner
logging.info(f'Winner: {winner}')
logging.info('----------------------') 
