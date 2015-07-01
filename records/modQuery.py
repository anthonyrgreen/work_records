#!/usr/bin/env python
from query import queryCommand
from addLogs import addLogsCommand
from deleteLogs import deleteLogsCommand

import argparse

mainParser = ArgumentParser(description="Store and query module load records.",
                            epilog=examplesStr,
                            formatter_class=RawTextHelpFormatter)
subParser = mainParser.add_subparsers(help="This program has three available commands:")
### QUERY PARSER ###
queryParser = subParser.add_parser("query", help=)

### ADDLOGS PARSER ###
addLogsParser = subParser.add_parser("addLogs", help=)
### DELETELOGS PARSER ###
deleteLogsParser = subParser.add_parser("deleteLogs", help=)

