#!/usr/bin/env python
from __future__ import print_function
import argparse
import re
from datetime import datetime, timedelta
from calendar import month_abbr
from records.src.query import getLogs
from records.src.printResults import printResults

###############################################################################
###############################################################################
###############################################################################

abbr = { 'm' : 'module'
       , 'v' : 'version'
       , 'u' : 'user'
       , 'c' : 'count' }

def parseSortBy(sortBy):
  return abbr[sortBy]

def parseAggregation(aggs):
  return [abbr[key] for key in aggs]

def parseFilters(moduleFilter, versionFilter, userFilter, countFilter):
  filters = {}
  if moduleFilter:
    filters['module'] = moduleFilter
  if versionFilter:
    filters['version'] = versionFilter
  if userFilter:
    filters['user'] = userFilter
  if countFilter:
    if countFilter[0] not in ['gt', 'lt']:
      print("error: count filter must be in form '{gt,lt} N'")
      exit(1)
    elif countFilter[0] == 'lt':
      filters['lessThan'] = countFilter[1]
    else:
      filters['greaterThan'] = countFilter[1]
  return filters

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


def makeParser():
  descriptionStr = \
"""Query the database for records based on the following properties:
count   (c)
module  (m)
version (v)
user    (u)\n"""
  exampleStr = \
"""Examples:
-- all records between Jan 1, 2014, and Feb 15, 2014, by day, aggregated by module, version, for modules 'R' or 'openmpi', by user 'grundoon':
./query.py -b 01/02/2014 -e 15/02/2014 -p day -a m v -fm R openmpi -fu grundoon
-- all records between Feb and Apr 2015, by month, aggregated by module and user, sorted by module, displaying only records with count less than 50:
./query.py -b 02/2015 -e 04/2015 -p month -a m u -s m -fc lt 50"""
  parser = argparse.ArgumentParser(description=descriptionStr,
                                   epilog=exampleStr,
                                   formatter_class=argparse.RawTextHelpFormatter)
                                   #formatter_class=argparse.RawDescriptionHelpFormatter)
  
  
  parser.add_argument('--begin_date', '-b', required=True,
                      help="[DD/]MM/YYYY at which to begin the query")
  parser.add_argument('--end_date', '-e', required=True,
                      help="[DD/]MM/YYYY at which to end the query (inclusive)")
  
  
  periodStr = \
"""Into what periods should the query be divided?
Choices: 'timespan', 'year', 'month', 'day'.
Default: month"""
  parser.add_argument('--period', '-p', choices=['day', 'month', 'year', 'timespan'],
                      default='month',
                      help=periodStr)
  
  aggregationStr = \
"""Properties along which data should be aggregated.
Choices: module (m), version (v), user (u).
Default: m"""
  parser.add_argument(
    "--aggregation", "-a", 
    choices=['m', 'v', 'u'], default=['m'], nargs='+',
    help=aggregationStr)
  
  sortStr = \
"""Sort records by which primary attribute?
Choices: module (m), version (v), user (u).
Default: c"""
  parser.add_argument("--sort_by", '-s', choices=['c', 'm', 'v', 'u'],
                      default='c',
                      help=sortStr)
  
  sortOrderStr = \
"""order records by ascending or descending?
Choices: ascending (asc), descending (desc).
Default: desc"""
  parser.add_argument('--sort_order', '-o', choices=['asc', 'desc'],
                      default='desc',
                      help=sortOrderStr)
  
  moduleFilterStr = \
"""The space-separated names of modules you would like to query.
Default: no filter."""
  parser.add_argument('--module_filter', '-fm', nargs='+',
                      default=[],
                      help=moduleFilterStr)
  
  versionFilterStr = \
"""The space-separated names of versions you would like to query.
Default: no filter."""
  parser.add_argument('--version_filter', '-fv', nargs='+',
                      default=[],
                      help=versionFilterStr)
  
  userFilterStr = \
"""The space-separated names of users you would like to query.
Default: no filter."""
  parser.add_argument('--user_filter', '-fu', nargs='+',
                      default=[],
                      help=userFilterStr)
  
  countFilterStr = \
"""You can also filter by count, only including records with\ncounts greater or less than some value.
Format: -fc (lt, gt) N
Default: no filter."""
  parser.add_argument('--count_filter', '-fc', nargs=2,
                      default=[],
                      help=countFilterStr)
  
  consistentColumnsStr = \
"""Normally, information that is redundant over several rows
is omitted. This may make reading easier, but also makes output
unpredictable for tools like awk. Use this flag to generate
consistent information."""
  parser.add_argument('--consistent_columns', '-cc', action='store_true',
                      default=False, help=consistentColumnsStr)

  noHeadersStr = \
"""Normally, results are preceded by headers and column names.
This option turns that off, for ease of text processing."""
  parser.add_argument('--no_headers', '-nh', action='store_true', default=False,
                      help=noHeadersStr)
  tabSeparatorsStr = \
"""This flag separates columns by a single tab"""
  parser.add_argument('--tab_separators', '-ts', action='store_true', default=False,
                      help=tabSeparatorsStr)

  scriptOutputStr = \
"""This is a convenience option which turns on the options:
--consistent_columns
--no_headers
--tab_separators"""
  parser.add_argument('--script_output', '-so', action='store_true', default=False,
                      help=scriptOutputStr)

  return parser


###############################################################################
###############################################################################
###############################################################################

parser = makeParser()
args = parser.parse_args()

startDate = parseDate(args.begin_date)
endDate = parseDate(args.end_date, inclusive=True)
period = args.period
sortBy = parseSortBy(args.sort_by)
sortOrder = args.period
aggregation = parseAggregation(args.aggregation)
filters = parseFilters(args.module_filter, 
                       args.version_filter, 
                       args.user_filter,
                       args.count_filter)
consistentColumns = args.consistent_columns | args.script_output
noHeaders = args.no_headers | args.script_output
tabSeparators = args.tab_separators | args.script_output

def query():
  labels, results = getLogs(startDate, endDate, 
                            dataAggregation=aggregation,
                            timeAggregation=period,
                            filters=filters,
                            sortBy=sortBy,
                            sortOrder=sortOrder)
  return (labels, results)

labels, results = query()

dateTabWidth = 7
dataTabWidth = 30
if not noHeaders:
  print("PACKAGES FOR PERIOD: " + args.begin_date + " - " + args.end_date)
printResults(labels, results, dateTabWidth, dataTabWidth, 
             consistentColumns=consistentColumns,
             noHeaders=noHeaders,
             tabSeparators=tabSeparators)


