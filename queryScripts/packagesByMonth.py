#!../flask/bin/python
from __future__ import print_function
from sys import path
path.insert(0,'..')

import argparse
import re
from datetime import datetime, timedelta
from records import app
from records.models.query import getLogsByTimespan

parser = argparse.ArgumentParser()
parser.add_argument("--sort_by", '-s', choices=['module', 'count', 'user'],
                    default='count',
                    help='sort records by which attribute? (DEFAULT: count)')
parser.add_argument('--sort_order', '-o', choices=['ASC', 'DESC'],
                    default='DESC',
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
  results = getLogsByTimespan(startDate, endDate, 
                              timeInterval=args.period,
                              filters={ 'module' : args.module_filter },
                              sortBy=args.sort_by,
                              sortOrder=args.sort_order)
#results = getModuleLogsByMonth(startDate, endDate, args.ordering, args.sort_by)

for time, result in reversed(results):
  print("")
  print("###################")
  print(str(time))
  print("###################")
  print("")
  for res in result:
    print("".join([str(r).ljust(10) for r in res]))
