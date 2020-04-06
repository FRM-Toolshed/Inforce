#!/usr/bin/env python

import os
import csv
import re
import collections
# import numpy as np
# import pandas as pd

def converttocsv(directory):
    os.chdir(directory)
    for i in range(1, 29):
        currfile = "pol" + str(i) + "_nofee.txt"
        f = open(currfile, "r+")

        l = f.readlines()
        f.close()

        f2 = open("pol" + str(i) + "_nofee.csv", "w+")

        for line in l:
            f2.write(line)

        f2.close()

def pullitems(Items, directory, outfile):
    os.chdir(directory)

    ItemsDict = collections.defaultdict(list)

    for i in range(1, 29):
        currfile = "pol" + str(i) + "_.txt"
        f = open(currfile, "r+")

        l = f.readlines()

        names = re.split(",",l[0])

        values = re.split(",",l[1])

        for item in Items:
            index = names.index(item)
            value = values[index]

            ItemsDict[item].append(value)
        
        f.close()

    # df = pd.DataFrame.from_dict(ItemsDict)
    # df.to_csv(r'C:\XYZMortality')

    csv_file = outfile
    keys = sorted(ItemsDict.keys())

    with open(csv_file, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter = ',')
        writer.writerow(keys)
        writer.writerows(zip(*[ItemsDict[key] for key in keys]))



def edititems(Items, directory, outdir):
    os.chdir(directory)

    for i in range(1, 26):
        currfile = "pol" + str(i) + "_nofee.txt"

        f = open(currfile, "r+")

        l = f.readlines()

        names = re.split(",",l[0])

        values = re.split(",",l[1])

        for item in Items:
            if item == 'ITMVersion':
                values[names.index(item)] = '4'
            elif item == 'IODAgeStart':
                values[names.index(item)] = values[names.index('ProductCol')]
            elif item == 'LapseTableNumber':
                if int(values[names.index(item)]) > 24:
                    values[names.index(item)] = str(int(values[names.index(item)]) - 18)
            elif item == 'FixedAcctCurrentCreditedRate':
                values[names.index(item)] = str(0.0154771)
        
        f.close()


        f2 = open(outdir +  "/" + currfile, "w+")

        line1 = ','.join(names)
        line2 = ','.join(values)

        f2.write(line1)
        f2.write(line2)

        f2.close()

def splitinforce(directory, Inforcefile):
    os.chdir(directory)

    f = open(Inforcefile, "r+")

    f_wb = open(Inforcefile.replace(".txt", "_wb.txt"), "w+")
    f_ab = open(Inforcefile.replace(".txt", "_ab.txt"), "w+")
    f_ib = open(Inforcefile.replace(".txt", "_ib.txt"), "w+")
    f_db = open(Inforcefile.replace(".txt", "_db.txt"), "w+")

    l = f.readlines()

    header = True
    GMWBIndCol = 0
    GMIBIndCol = 0
    GMABIndCol = 0

    for line in l:
        if header:
            f_wb.write(line)
            f_ab.write(line)
            f_db.write(line)
            f_ib.write(line)
            header = False

            splitline = re.split(",",line)

            for x, y in enumerate(splitline):
                if y =="GMWB_INDICATOR":
                    GMWBIndCol = x
                elif y == "GMIB_IND":
                    GMIBIndCol = x
                elif y == "GMAB_IND":
                    GMABIndCol = x
        else:
            splitline = re.split(",", line)
            if splitline[GMWBIndCol] != "0":
                f_wb.write(line)
            elif splitline[GMABIndCol] != "0":
                f_ab.write(line)
            elif splitline[GMIBIndCol] != "0":
                f_ib.write(line)
            else:
                f_db.write(line)

    f.close()
    f_ab.close()
    f_db.close()
    f_wb.close()
    f_ib.close()


def additems(Items, directory, outdir):
    os.chdir(directory)

    for i in range(29, 34):
        currfile = "pol" + str(i) + "_nofee.txt"

        f = open(currfile, "r+")

        l = f.readlines()

        names = re.split(",",l[0])
        names[len(names) -1] = names[len(names) -1].replace('\n', '')
        values = re.split(",",l[1])
        values[len(names) -1] = values[len(names) -1].replace('\n', '')

        for item in Items:
            names.append(item)
            values.append('0')

        names[len(names) -1] = names[len(names) -1] + '\n'
        values[len(names) -1] = values[len(names) -1] + '\n'

        f2 = open(outdir + "/" + currfile, "w+")

        line1 = ','.join(names)
        line2 = ','.join(values)

        f2.write(line1)
        f2.write(line2)

        f2.close()

    # df = pd.DataFrame.from_dict(ItemsDict, orient = 'index')
    # df.to_csv(r'C:\XYZMortality\Check3.csv')

    # csv_file = 'Check3.csv'
    # keys = sorted(ItemsDict.keys())

    # with open(csv_file, 'w') as csvfile:
    #     writer = csv.writer(csvfile, delimiter = ',')
    #     writer.writerow(keys)
    #     writer.writerows(zip(*[ItemsDict[key] for key in keys]))




if __name__ == "__main__":
    ############ Trim Inforce Down to select Columns #####################
    # pullitems(['IssueDate', 'Age', 'StartDate', 'ValDate', 'GMWBIndicator','VixFeeColumn','JointLifeBeneficiaryAge'], r'C:\XYZMortality', 'Ages.csv')
    
    ############ Edits select Inforce Columns ##################
    # edititems(['ITMVersion', 'IODAgeStart', 'LapseTableNumber'], r'C:\XYZMortality', r'C:\XYZMortality')
    # edititems(['FixedAcctCurrentCreditedRate'], r'C:\XYZMortality', r'C:\XYZMortality')
    
    ############ Converts Text File to CSV #################
    # converttocsv(r'C:\XYZMortality')
   
    ############ Add columns to Inforce ###############
    # additems(['DBRollupRate2', 'DBRollupRate_AgeSwitch'], r'C:\XYZMortality', r'C:\XYZMortality')
    
    
    ############ Split Inforce into separate files by column Value ###############
    splitinforce(r'C:\XYZMortality', "Inforce_Inf20200327_Val20200403_EV15.txt")
