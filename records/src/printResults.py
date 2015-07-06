from __future__ import print_function
from calendar import month_abbr

def span(pred, xs):
  fst = []
  snd = list(xs)
  for i in range(len(xs)):
    if pred(xs[i]):
      fst.append(snd[0])
      snd.pop(0)
    else:
      break
  return (fst, snd)

def split(idx, xs):
  return (xs[:idx], xs[idx:])

def printResults(labels, results, dateTabWidth, dataTabWidth,
                 consistentColumns=False, noHeaders=False, tabSeparators=False):
  dateNames = ['timespan', 'year', 'month', 'day']
  dateColumns, dataColumns = span(lambda x: x in dateNames, labels)
  if 'timespan' in dateColumns:
    dateColumns = []
  if 'month' in dateColumns:
    monthIdx = dateColumns.index('month')
  else:
    monthIdx = None

  ### CONSTRUCT THE LABEL
  dateIdx = 0
  dataIdx = len(dateColumns)
  if not tabSeparators:
    labelStr = "".join([str(l).ljust(dateTabWidth) for l in dateColumns])
    labelStr += "".join([str(l).ljust(dataTabWidth) for l in dataColumns])
    labelStr += "\n" + "="*len(labelStr)
  else:
    labelStr = "\t".join(map(str, dateColumns + dataColumns))
    labelStr += "\n" + "="*len(labelStr)

  ### FORMAT THE DATA
  resultStr = ""
  dateDelta = [None] * len(dateColumns)
  dataDelta = [None] * len(dataColumns)
  delta = [None] * (len(dateColumns) + len(dataColumns))
  for result in results:
    result = list(result)
    if monthIdx:
      result[monthIdx] = month_abbr[result[monthIdx]]
    if not consistentColumns:
      for i in range(len(result)):
        if delta[i] != result[i]:
          deltaIdx = i
          break
      delta = result
    else:
      deltaIdx = 0
    # Whitespace
    if not tabSeparators:
        resultStr += "".join(["".ljust(dateTabWidth) 
                              for i in range(dateIdx, min(deltaIdx, dataIdx))])
        resultStr += "".join(["".ljust(dataTabWidth) 
                              for i in range(min(deltaIdx, dataIdx), deltaIdx)])
        # Content
        resultStr += "".join([str(r).ljust(dateTabWidth)
                              for r in result[deltaIdx:max(deltaIdx, dataIdx)]])
        resultStr += "".join([str(r).ljust(dataTabWidth)
                              for r in result[max(deltaIdx, dataIdx):]])
    else:
        resultStr += "\t"*(min(deltaIdx, dataIdx) - dateIdx)
        resultStr += "\t"*(deltaIdx - min(deltaIdx, dataIdx))
        # Content
        resultStr += "\t".join(map(str, result[deltaIdx:]))
    resultStr += "\n"
  if not noHeaders:
    print(labelStr)
  print(resultStr)
