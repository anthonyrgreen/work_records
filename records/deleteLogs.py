from records.src.maintenance import deleteModuleLogFile
from argparse import RawTextHelpFormatter

def execDeleteLogs(args):
  for filename in args.files:
    output = deleteModuleLogFile(filename)
    if verbose:
      print output

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
