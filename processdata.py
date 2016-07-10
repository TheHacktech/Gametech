'''
'''

import csv
import json
from collections import Counter

# Parse function from Google Games
# Might be useful later. Not currently used. At all.
# def read_file(filename, delimiter, skiprows=0, typecast=str):
#     with open(filename) as f:
#         res = []
#         try:
#             skip = 0
#             for line in f:
#                 # print line
#                 if (skip >= skiprows):
#                     res.append(map(typecast, line.rstrip().split(delimiter)))
#                 skip += 1
#             return res
#         except :
#             print "error"
#             return res

def extractGreylock():
    print "Entering extractGreylock"
    hacktechEntries = []
    with open('greylockdata.csv', 'rU') as csvfile:
        spamreader = list(csv.reader(csvfile, delimiter=',', quotechar='"'))

        schools = [row[0].split('(')[0].strip() for row in list(spamreader)[1:] if row[0] != ""]
        yearcount = Counter([row[0].split('(')[-1].split(')')[0].strip() for row in list(spamreader)[1:] if row[0] != ""])
        names = [[row[1].strip(), row[2].strip()] for row in list(spamreader)[1:] if row[1] != ""]
        companies = [row[3].strip() for row in list(spamreader)[1:] if row[3] != ""]
        years = [row[0].split('(')[-1].split(')')[0].strip() for row in list(spamreader)[1:] if row[0] != ""]
    return [schools, yearcount, names, companies, years]


def toDashboardForm(greydata):
    graphform = []
    helper = {}

    # Find min year and max year
    firstyear = min(greydata[1])
    lastyear = max(greydata[1])

    # Change data to something nice to change it into
    for u in set(greydata[0]):
        helper[u] = {key: 0 for key in range(int(firstyear), int(lastyear) + 1)}
        
    count = Counter(zip(greydata[0], greydata[4]))
    for c in count:
        helper[c[0]][int(c[1])] += count[c]

    # Change data to its final form
    for key, value in helper.iteritems():
        thing = {}
        thing['State'] = key
        thing['freq'] = value
        graphform.append(thing)

    print graphform
    # f = open('compiled_project_data_languages.json', 'w')
    # f.write(json.dumps(graphform))


# greydata in format [schools, years, names, companies]
greydata = extractGreylock()

toDashboardForm(greydata)

# combineData(devpost, hacktech)

# f = open('final_data.json', 'w')
# f.write(json.dumps(devpost))


# categories = list(categories)


# toCategoryGraphForm(categories, devpost)
# # toLanguageGraphForm(categories, devpost, languages)
# # toVennForm(categories, devpost)













