from __future__ import print_function
import re
from datetime import datetime, timedelta
from calendar import month_abbr
from src.query import getLogs
from src.printResults import printResults
from argparse import RawTextHelpFormatter

###############################################################################
########################### BEGIN PARSING FUNCTIONS ###########################
###############################################################################

def parseDate(dateStr, inclusive=False):
  dayPattern = re.compile("^[0-3][1-9]/[0-1][0-9]/[0-9]{4}$")
  monthPattern = re.compile("^[0-1][0-9]/[0-9]{4}$")
  if monthPattern.match(dateStr):
    date = datetime.strptime('01/' + dateStr, '%d/%m/%Y')
    if inclusive:
      if date.month < 12:
        date = datetime(date.year, date.month + 1, 1)
      else:
        date = datetime(date.year + 1, date.month, 1)
  elif dayPattern.match(dateStr):
    date = datetime.strptime(dateStr, '%d/%m/%Y')
    if inclusive:
      date = date + timedelta(days = 1)
  else:
    print("Please give dates in the form 'DD/MM/YYYY or MM/YYYY'.")
    exit(1)
  return date

def parseFilters(moduleFilter):
  filters = { 'module' : moduleFilter }
  return filters

###############################################################################
############################ END PARSING FUNCTIONS ############################
###############################################################################

#-*-*-*-# #-*-*-*-#                                         #-*-*-*-# #-*-*-*-#

###############################################################################
############################ BEGIN QUERY FUNCTIONS ############################
###############################################################################

def execQuery(args):
  startDate = parseDate(args.begin_date)
  endDate = parseDate(args.end_date, inclusive=True)
  period = 'month'
  sortBy = 'module'
  sortOrder = 'asc'
  count = 'numUsers'
  aggregation = ['module']
  filters = parseFilters(args.module)
  consistentColumns = args.consistent_columns | args.script_output
  noHeaders = args.no_headers | args.script_output
  tabSeparators = args.tab_separators | args.script_output

  labels, results = getLogs(startDate, endDate, 
                            count=count,
                            dataAggregation=aggregation,
                            timeAggregation=period,
                            filters=filters,
                            sortBy=sortBy,
                            sortOrder=sortOrder)
  if not noHeaders:
    print("MONTHLY USER COUNTS FOR PERIOD: " + args.begin_date + " - " + args.end_date)
  printResults(labels, results, fillInMonths=True,
               startYear = startDate.year, startMonth = startDate.month,
               endYear = endDate.year, endMonth = endDate.month,
               consistentColumns=consistentColumns,
               noHeaders=noHeaders,
               tabSeparators=tabSeparators)
  return (labels, results)

###############################################################################
############################# END QUERY FUNCTIONS #############################
###############################################################################

#-*-*-*-# #-*-*-*-#                                         #-*-*-*-# #-*-*-*-#

###############################################################################
########################## BEGIN INTERFACE FUNCTIONS ##########################
###############################################################################

def createMonthlyUserCountsParser(subParser):
  descriptionStr = \
"""Print the number of unique monthly users for a given package in the given date range"""
  exampleStr = \
"""Examples:
-- number of unique users of R from January to February, 2015:
   ./module-query monthly-user-counts -b 01/2015 -e 02/2015 --module R"""
  consistentColumnsStr = \
"""Normally, information that is redundant over several rows
is omitted. This may make reading easier, but also makes output
unpredictable for tools like awk. Use this flag to generate
consistent information."""
  moduleStr = \
"""The name of module for which you would like a report."""
  noHeadersStr = \
"""Normally, results are preceded by headers and column names.
This option turns that off, for ease of text processing."""
  tabSeparatorsStr = \
"""This flag separates columns by a single tab"""
  scriptOutputStr = \
"""This is a convenience option which turns on the options:
--consistent_columns
--no_headers
--tab_separators"""

  # the queryParser itself
  queryParser = subParser.add_parser("monthly-user-counts",
    description=descriptionStr, epilog=exampleStr,
    formatter_class=RawTextHelpFormatter)
  # adding queryParser options
  queryParser.add_argument('--begin_date', '-b',
    required=True, help="[DD/]MM/YYYY at which to begin the query")
  queryParser.add_argument('--end_date', '-e',
    required=True, help="[DD/]MM/YYYY at which to end the query (inclusive)")
  queryParser.add_argument('--module', '-m',
    nargs=1, required=True)
  queryParser.add_argument('--consistent_columns', '-cc',
    action='store_true', default=False, help=consistentColumnsStr)
  queryParser.add_argument('--no_headers', '-nh',
    action='store_true', default=False, help=noHeadersStr)
  queryParser.add_argument('--tab_separators', '-ts',
    action='store_true', default=False, help=tabSeparatorsStr)
  queryParser.add_argument('--script_output', '-so',
    action='store_true', default=False, help=scriptOutputStr)
  # The default function to be called
  queryParser.set_defaults(func=execQuery)

  return queryParser

###############################################################################
########################### END INTERFACE FUNCTIONS ###########################
###############################################################################
