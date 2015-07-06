from src.maintenance import deleteModuleLogFile
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
"""This command allows you to delete all records associated with a given
module log. This is useful in case logs from one particular date range
are found to be erroneous or new logs from a given date become available.
This command behaves exactly like the add-logs command, but in reverse."""
  exampleStr = \
"""Examples:
-- Delete a single module log:
$ ./module-query delete-logs ./logs/flux_module_log-2014-02.gz
-- Delete all module logs found in a folder (those not present in the
   database will simply be skipped):
$ ./module-query delete-logs ./logs/*"""
  verboseStr = \
"""Turn on this flag to be informed as logs are deleted / skipped.
NOTE: this functionality is not yet implemented."""
  filesStr = \
"""These are the filenames of those logs to be added. Note that the
whole filepath of a file is ignored in log storage/deletion -- a
file added like "./logs/flux_module_log-2014-02.gz" is stored simply
as "flux_module_log-2014-02.gz", so the following commands will
result in an empty database:
$ ./install.sh
$ cp ./logs/* ./logs_copy1
$ cp ./logs/* ./logs_copy2
$ ./module-query add-logs ./logs_copy1/*
$ ./module-query delete-logs ./logs_copy2/*"""

  deleteLogsParser = subParser.add_parser("delete-logs",
    description=descriptionStr, epilog=exampleStr,
    formatter_class=RawTextHelpFormatter)
  deleteLogsParser.add_argument("--verbose", "-v",
    action="store_true", default=False, help=verboseStr)
  deleteLogsParser.add_argument("files",
    nargs="+", help=filesStr)
  deleteLogsParser.set_defaults(func=execDeleteLogs)

  return deleteLogsParser
