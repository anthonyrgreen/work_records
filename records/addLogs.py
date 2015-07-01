from records.src.maintenance import addModuleLogFile
from argparse import RawTextHelpFormatter

def execAddLogs(args):
  for filename in args.files:
    output = addModuleLogFile(filename)
    if verbose:
      print output

def createAddLogsParser(subParser):
  descriptionStr = \
"""createAddLogsParser descriptionStr
TODO"""
  exampleStr = \
"""createAddLogsParser exampleStr
TODO"""
  verboseStr = \
"""createAddLogsParser verboseStr
TODO"""
  filesStr = \
"""createAddLogsParser filesStr
TODO"""

  addLogsParser = subParser.add_parser("addLogs",
    description=descriptionStr, epilog=exampleStr,
    formatter_class=RawTextHelpFormatter)
  addLogsParser.add_argument("--verbose", "-v",
    action="store_true", default=False, help=verboseStr)
  addLogsParser.add_argument("files",
    nargs="+", help=filesStr)
  addLogsParser.set_defaults(func=execAddLogs)

  return addLogsParser
