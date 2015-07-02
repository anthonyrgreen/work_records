from records.src.maintenance import deleteModuleLogFile
from argparse import RawTextHelpFormatter

def execDeleteLogs(args):
  recordsDeleted= 0
  for filename in args.files:
    numDeleted, output = deleteModuleLogFile(filename)
    recordsDeleted += numDeleted
    if args.verbose:
      print output
  if args.verbose:
    print "Successfully deleted " + str(recordsDeleted) + " records."

def createDeleteLogsParser(subParser):
  descriptionStr = \
"""createDeleteLogsParser descriptionStr
TODO"""
  exampleStr = \
"""createDeleteLogsParser exampleStr
TODO"""
  verboseStr = \
"""createDeleteLogsParser verboseStr
TODO"""
  filesStr = \
"""createDeleteLogsParser filesStr
TODO"""

  deleteLogsParser = subParser.add_parser("deleteLogs",
    description=descriptionStr, epilog=exampleStr,
    formatter_class=RawTextHelpFormatter)
  deleteLogsParser.add_argument("--verbose", "-v",
    action="store_true", default=False, help=verboseStr)
  deleteLogsParser.add_argument("files",
    nargs="+", help=filesStr)
  deleteLogsParser.set_defaults(func=execDeleteLogs)

  return deleteLogsParser
