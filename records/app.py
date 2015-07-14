from query import createQueryParser
from queryMonthlyUserCounts import createMonthlyUserCountsParser
from queryMonthlyUserLists import createMonthlyUserListsParser
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
### MONTHLYUSERCOUNTS PARSER ###
monthlyUserCountsParser = createMonthlyUserCountsParser(subParser)
### MONTHLYUSERLISTS PARSER ###
monthlyUserListsParser = createMonthlyUserListsParser(subParser)

### RUN THAT BUSINESS
if __name__ == '__main__':
  args = mainParser.parse_args()
  args.func(args)
