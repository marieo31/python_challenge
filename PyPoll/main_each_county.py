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
logfile = "results_by_county.txt"
open(logfile, 'w').close()  #to delete the existing content of the file
# we only need to set up the INFO level
level = logging.INFO
format = '%(message)s'
handlers = [logging.FileHandler(logfile), logging.StreamHandler()]
logging.basicConfig(level = level, format = format, handlers = handlers)

#Initializing
#------------
csvpath = "election_data.csv"
counties = {} # dico for the results per county
names = []    # list of the candidates (global results)
nbVotes = []  # nb of votes for each candidate (global results)

# Counting the votes
#-------------------
with open(csvpath, newline='',encoding='utf-8') as csvfile:
    #open the csvfile
    csvreader = csv.reader(csvfile, delimiter=',')
    #skip the header line
    next(csvreader,None)    
    #looping on each row
    for row in csvreader:
        current_county = row[1]
        current_name = row[2]
        if current_county in counties: # if data has already been collected for this county
            if counties[current_county]['names'].count(current_name) == 1: # if vote has already been counted for this candidate
                counties[current_county]['nbVotes'][counties[current_county]['names'].index(current_name)] += 1 #incrementing the number of votes for the candidate
            else:  # if it's the first vote for this candidate in the current county
                counties[current_county]['names'].append(current_name)  # we add the name in the list
                counties[current_county]['nbVotes'].append(1)           # consider its first vote
                                        
        else:   #if data hasen't been collected yet for this county            
            counties[current_county] = {'names':[],'nbVotes':[]}  # we add the empty subdico to counties dictionnary
            counties[current_county]['names'].append(current_name)  # we add the first candidate name for the county
            counties[current_county]['nbVotes'].append(1)           # and consider the vote
            
        if names.count(row[2]) == 1:    # if data has already been collected for the candidate
            nbVotes[names.index(row[2])] += 1   #incrementing the number of votes            
        else: # if the candidate has not been parsed yet
            names.append(row[2])    # we add the name in the list
            nbVotes.append(1)       # consider its first vote
            
# let's go crazy and sort the candidates according to the number of votes

            
# Processing the counted votes (total, pc of votes, winner)
#----------------------------------------------------------
# total number of votes
total_per_county = [sum(counties[county]['nbVotes']) for county in counties]
total = sum(total_per_county)   # total nb of votes by suming up the regional results
total2 = sum(nbVotes)    # total nb of votes by suming up the global results
if total != total2: # let's check if the results are consistents
    print("Something went wrong: the global results don't match the counties results.")
    exit()
# Global results (pc of votes and winner)    
pc_votes = [votes/total*100 for votes in nbVotes] # percents of votes for each candidate
winner = names[np.argmax(nbVotes)]  # Name of the winner
# calculating the pc of votes per county
for county in counties:
    counties[county]['total'] = sum(counties[county]['nbVotes'])
    counties[county]['pc_votes'] = [votes/counties[county]['total']*100 for votes in counties[county]['nbVotes']]

# Printing the results
#--------------------
# first we can zip the values
results = zip(names, pc_votes, nbVotes)
logging.info("----------------------")
logging.info("Election results")
logging.info("----------------------\n")
logging.info('Global results:')
logging.info('----------------------')
logging.info(f'  ->Total votes: {total}')
# results for each candidate
for res in results:
    logging.info("  ->%s: %.1f%% (%i)"%(res))
logging.info('----------------------')    
# Winner
logging.info(f'>>> Winner: {winner}')
logging.info('----------------------') 
logging.info('\n Regional results')
logging.info('---------------------')
for county in counties:
    logging.info(f' Results for {county}: ')
    logging.info(f"  -> Total votes: {counties[county]['total']}")
    # ziping the results for the current county
    local_results = zip(counties[county]['names'],  counties[county]['pc_votes'], counties[county]['nbVotes'])
    for res in local_results:
        logging.info("  -> %s: %.1f%% (%i)"%(res))
    logging.info('-------------------')