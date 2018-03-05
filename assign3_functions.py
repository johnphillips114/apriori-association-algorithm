#This file contains the individual functions for the program

import argparse
from itertools import chain, combinations

def loadDB(dataFile):
    #Copy data from file to a data structure, skip first line of headers
    with open(dataFile) as f:
        next(f)
        dataSource = f.readlines()

    itemSet = set()
    transactionList = list()
    for row in dataSource:
        setRow = frozenset(row.split())
        transactionList.append(setRow)
        for item in row.split():
            itemSet.add(frozenset([item]))
    return itemSet, transactionList

# create the frequent 1-itemsets dictionary
def buildFirstItemset(transactionList, itemSet, minSup):
    freqItemSet = dict()
    lenTrans = len(transactionList)
    for item in itemSet:
        count = 0
        for row in transactionList:
            if item.issubset(row):
                count = count + 1
        #Calculate the support for the item
        support = float(count/lenTrans)
        #For 1 item itemsets, we can just check them all if they meet the
        #minimum support because we have no apriori knowledge yet to help
        #prune
        if support >= minSup:
            freqItemSet.update([(item, support)])
    return freqItemSet

# Generate the candidate combinations of k item itemsets
def generateCandidates(k, transactionList, prevItemSet):
    candidateList = list()
    itemSet = joinSet(prevItemSet, k)
    for item in itemSet:
        candidateList.append(frozenset([item]))
    return candidateList

#obtained from https://github.com/asaini/Apriori/blob/master/apriori.py
def joinSet(itemSet, length):
    joinedSet = set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])
    return joinedSet

#using apriori algorithm to find all frequent K-itemSets(K>=2)
def genFrequentKItemset(transactionList, itemSet, minSup, k):
    freqItemSet = dict()
    lenTrans = len(transactionList)
    #newItemSet is the new candidates of k item itemsets
    newItemSet = joinSet(itemSet, k)
    #now we check if the candidates meet the support requirement
    for item in newItemSet:
        count = 0
        for row in transactionList:
            if item.issubset(row):
                count = count + 1
        #Calculate the support for the item
        support = float(count/lenTrans)
        if support >= minSup:
            freqItemSet.update([(item, support)])
    return freqItemSet


#Mine all strong rules from frequent K-itemsets
def createRules(allFrequentItems, minSup, minCon):
    rules = list()
    #Each value in the dictionary satisfies the support requirement, so we
    #need to check all of their pairs for the confidence values
    for itemSet, support in allFrequentItems.items():
        #only consider itemSets of two or more items
        if len(itemSet) > 1:
            for predictor in subsets(itemSet):
                #response is the remaining value(s) in the set
                response = itemSet.difference(predictor)
                #Only consider pairs that have a response
                if len(response) > 0:
                    #change predictor to a frozenset from a string for comparing
                    predictor = frozenset(predictor)
                    #Cases where either the predictor or response occur
                    pOrR = predictor | response
                    #calculate the confidence value
                    con = float(allFrequentItems[pOrR]) / allFrequentItems[predictor]
                    if con >= minCon:
                        rules.append((predictor, response, con, support))
    return rules

#This function generates the subsets for a frozenset of multiple entries
#retrieved from https://github.com/abarmat/python-apriori/blob/master/apriori.py
def subsets(itemset):
    return chain(*[combinations(itemset, i + 1) for i, a in enumerate(itemset)])

# Output all mined rules into the external file called "Rules"
# TODO: get rid of the frozensets in the output, include attribute titles
def outputRules(allRules):
    f = open('Rules.txt', 'w')
    i = 1
    for rule in allRules:
        predictor, response, con, support = rule
        f.write('Rule #{0}: (Support={1}, Confidence={2})\n'.format(i, support, con))
        f.write('({0} ---> {1})\n\n'.format(str(predictor), str(response)))
        i = i + 1
    f.close()
    return ""
