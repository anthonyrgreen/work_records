#!../flask/bin/python
from __future__ import print_function
from sys import path
path.insert(0,'..')

import argparse
import re
from datetime import datetime, timedelta
from records import app
from records.models.query import getLogs
from printResults import printResults

parser = argparse.ArgumentParser()
parser.add_argument('--module', '-m', required=True,
                    help='Which module would you like records for?')
parser.add_argument('--begin_date', '-b', required=True,
                    help="[DD-]MM-YYYY at which to begin the query")
parser.add_argument('--end_date', '-e', required=True,
                    help="[DD-]MM-YYYY at which to end the query")
parser.add_argument("--sort_by", '-s', choices=['count', 'version'],
                    default='version',
                    help='sort records by which attribute? (DEFAULT: version)')
parser.add_argument('--sort_order', '-o', choices=['asc', 'desc'],
                    default='DESC',
                    help='order results by ascending or descending?')
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
                            dataAggregation=['module', 'version'],
                            filters={ 'module' : [args.module] },
                            sortBy=args.sort_by,
                            sortOrder=args.sort_order)

dateTabWidth = 7
dataTabWidth = 25
print("PACKAGE VERSIONS FOR PACKAGE: " + args.module + "\nOVER PERIOD: " + args.begin_date + " - " + args.end_date)
printResults(labels, results, dateTabWidth, dataTabWidth)
