from query import createQueryParser
from addLogs import createAddLogsParser
from deleteLogs import createDeleteLogsParser
from argparse import ArgumentParser

examplesStr = \
"""mainParser examplesStr
TODO"""
mainParser = ArgumentParser(description="Store and query module load records.",
  epilog=examplesStr)
subParser = mainParser.add_subparsers(help="This program can be run in one of three modes")

### QUERY PARSER ###
queryParser = createQueryParser(subParser)
### ADDLOGS PARSER ###
addLogsParser = createAddLogsParser(subParser)
### DELETELOGS PARSER ###
deleteLogsParser = createDeleteLogsParser(subParser)

### RUN THAT BUSINESS
args = mainParser.parse_args()
args.func(args)
