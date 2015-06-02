#!../flask/bin/python
from __future__ import print_function
from sys import path
path.insert(0,'..')

import argparse
import re
from datetime import datetime, timedelta
from calendar import month_abbr
from records import app
from records.models.query import getLogs
from dbConnect import dbFunction

parser = argparse.ArgumentParser()
parser.add_argument("--sort_by", '-s', choices=['module', 'count', 'user'],
                    default='count',
                    help='sort records by which attribute? (DEFAULT: count)')
parser.add_argument('--sort_order', '-o', choices=['asc', 'desc'],
                    default='desc',
                    help='order records by ascending or descending? (DEFAULT: DESC)')
parser.add_argument('--module_filter', '-f', nargs='+',
                    default=[],
                    help='enter the space-separated names of modules you would like to see (DEFAULT: no filter')
parser.add_argument('--begin_date', '-b', required=True,
                    help="[DD-]MM-YYYY at which to begin the query")
parser.add_argument('--end_date', '-e', required=True,
                    help="[DD-]MM-YYYY at which to end the query (inclusive)")
parser.add_argument('--period', '-p', choices=['day', 'month', 'year', 'timespan'],
                    default='month',
                    help='over what period should the query be divided? (DEFAULT: month)')

args = parser.parse_args()

# CHECK INPUT
###
# Dates
###
dayPattern = re.compile("^[0-3][1-9]-[0-1][0-9]-[0-9]{4}$")
monthPattern = re.compile("^[0-1][0-9]-[0-9]{4}$")
# begin_date
if monthPattern.match(args.begin_date):
  startDate = datetime.strptime('01-' + args.begin_date, '%d-%m-%Y')
elif dayPattern.match(args.begin_date):
  startDate = datetime.strptime(args.begin_date, '%d-%m-%Y')
else:
  print("Please give a begin date in a valid format.")
  exit(1)
# end_date
if monthPattern.match(args.end_date):
  endDate = datetime.strptime('01-' + args.end_date, '%d-%m-%Y')
  # switch endDate to be inclusive
  if endDate.month < 12:
    endDate = datetime(endDate.year, endDate.month + 1, 1)
  else:
    endDate = datetime(endDate.year + 1, 1, 1)
elif dayPattern.match(args.end_date):
  endDate = datetime.strptime(args.end_date, '%d-%m-%Y')
  # switch endDate to be inclusive
  endDate = endDate + timedelta(days = 1)
else:
  print("Please give an end date in a valid format.")
  exit(1)

with app.app_context():
  labels, results = getLogs(startDate, endDate, 
                            timeAggregation=args.period,
                            filters={ 'module' : args.module_filter },
                            sortBy=args.sort_by,
                            sortOrder=args.sort_order)

### FORMATTING DATA
dateTabWidth = 7
contentTabWidth = 25

timespanFlag = 'timespan' in labels
if timespanFlag:
  del(labels[0])

for i in range(len(labels)):
  if labels[i] not in ['year', 'month', 'day']:
    contentIdx = i
    break
try:
  monthIdx = labels.index('month')
except:
  monthIdx = None

### PRINT THE TOP HEADER
print("PACKAGES FOR PERIOD " + args.begin_date + " - " + args.end_date + ":")
if not timespanFlag:
  labelStr = "".join([str(l).ljust(dateTabWidth) for l in labels[:contentIdx]])
else:
  labelStr = ""
labelStr += "".join([str(l).ljust(contentTabWidth) for l in labels[contentIdx:]])
print(labelStr)
print("="*len(labelStr))
listDelta = [None] * len(labels)

### PRINT THE REST
for result in results:
  result = list(result)
  # Convert the month number to an abbreviation
  if monthIdx:
    result[monthIdx] = month_abbr[result[monthIdx]]
  # Find the smallest index at which the previous result differs from the current one
  # This is so that we don't have a column with "2014 2014 2014 2014 2014...." Thus,
  # we only print columns when their values change
  for i in range(len(labels)):
    if listDelta[i] != result[i]:
      changeIdx = i
      break
  listDelta = list(result)
  # Format answer:
  printString = ""
  # Date whitespace
  if not timespanFlag:
    printString += "".join(["".ljust(dateTabWidth) 
                           for i in range(min(contentIdx, changeIdx))])
  # Content whitespace
  printString += "".join(["".ljust(contentTabWidth)
                          for i in range(min(contentIdx, changeIdx), changeIdx)])
  # Date info
  if not timespanFlag:
    printString += "".join([str(r).ljust(dateTabWidth)
                            for r in result[changeIdx:contentIdx]])
  # Content info
  printString += "".join([str(r).ljust(contentTabWidth)
                          for r in result[contentIdx:]])
  # Print the record
  print(printString)
