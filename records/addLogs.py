from src.maintenance import addModuleLogFile
from argparse import RawTextHelpFormatter

def execAddLogs(args):
  recordsAdded = 0
  for filename in args.files:
    numAdded, output = addModuleLogFile(filename)
    recordsAdded += numAdded
    if args.verbose:
      print output
  if args.verbose:
    print "Successfully added " + str(recordsAdded) + " records."

def createAddLogsParser(subParser):
  descriptionStr = \
"""Add one or more cumulative logs to the database. Log filenames must
be in the form "^flux_module_log-.*\.gz$". Logs whose filenames 
do not match that regular expression, or which have already been 
added, will be skipped."""
  exampleStr = \
"""Examples:
-- Add a single module log:
$ ./module-query add-logs ./logs/flux_module_log-2014-02.gz
-- Add an entire folder of module logs (those already added and those
   with improper filenames will be skipped)
$ ./module-query add-logs ./logs/*"""
  verboseStr = \
"""Turn on this flag to be informed as logs are added / skipped."""
  filesStr = \
"""These are the filenames of those logs to be added."""

  addLogsParser = subParser.add_parser("add-logs",
    description=descriptionStr, epilog=exampleStr,
    formatter_class=RawTextHelpFormatter)
  addLogsParser.add_argument("--verbose", "-v",
    action="store_true", default=False, help=verboseStr)
  addLogsParser.add_argument("files",
    nargs="+", help=filesStr)
  addLogsParser.set_defaults(func=execAddLogs)

  return addLogsParser
