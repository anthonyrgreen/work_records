#!../flask/bin/python
from sys import path
path.insert(0,'..')

import argparse
from datetime import datetime
from records import *
from records.modelController import getModuleVersionLogsByMonth

parser = argparse.ArgumentParser()
parser.add_argument('--module', '-m',
                    help='Which module would you like records for?')
parser.add_argument('--start_date', '-s', 
                    help="MM-YYYY at which to begin the query")
parser.add_argument('--end_date', '-e', 
                    help="MM-YYYY at which to end the query")
parser.add_argument('--ordering', '-o', choices=['ASC', 'DESC'],
                    default='DESC',
                    help='order results by ascending or descending?')

args = parser.parse_args()
startDate = datetime.strptime('01-' + args.start_date, '%d-%m-%Y')
endDate = datetime.strptime('01-' + args.end_date, '%d-%m-%Y')

results = getModuleVersionLogsByMonth(startDate, endDate, args.module, args.ordering)

#for res in results:
#  print ""
#  print ""
#  print "###################"
#  print "###################"
#  print "###################"
#  print ""
#  print ""
#  print res
for time, result in reversed(results):
  print ""
  print "###################"
  print time
  print "###################"
  print ""
  for res in result:
    print "".join([str(r).ljust(10) for r in res])
