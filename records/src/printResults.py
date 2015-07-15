from __future__ import print_function
from calendar import month_abbr
import pandas as pd

def fillMonths(labels, results, startYear, startMonth, endYear, endMonth):
  # Assumes year is results[0], month is results[1]
  def getYear(result):
    return result[0]
  def getMonth(result):
    return result[1]
  def dateExistsAtIdx(year, month, results, idx):
    if idx < len(results):
      return getYear(results[idx]) == year and getMonth(results[idx]) == month
    else:
      return False
  def emptyRecord(year, month):
    emptyRecord = [year, month] + ['-']*(len(labels) - 2)
    for label in ['uniqueUsers', 'numLoads']:
      try:
        emptyRecord[labels.index(label)] = 0
      except:
        pass
    return tuple(emptyRecord)

  resultsIdx = 0
  year = startYear
  month = startMonth
  while year <= endYear:
    while (year < endYear and month <= 12) or (year == endYear and month < endMonth):
      # Add in empty records if the given year / month combo does not exist
      if not dateExistsAtIdx(year, month, results, resultsIdx):
        results.insert(resultsIdx, emptyRecord(year, month))
        resultsIdx = resultsIdx + 1
      # If it does exist, increment the resultsIdx until we get to a different
      # year / month
      else:
        while dateExistsAtIdx(year, month, results, resultsIdx):
          resultsIdx = resultsIdx + 1
      month = month + 1
    month = 1
    year = year + 1

def labelMonths(labels, results):
  try:
    monthIdx = labels.index('month')
    for i in range(len(results)):
      result1 = list(results[i])
      result1[monthIdx] = month_abbr[result1[monthIdx]]
      results[i] = tuple(result1)
  finally:
    return results

def printResults(labels, results, fillInMonths=False,
                 startYear=None, startMonth=None, endYear=None, endMonth=None,
                 consistentColumns=False, noHeaders=False, tabSeparators=False):
  if(fillInMonths):
    fillMonths(labels, results, startYear, startMonth, endYear, endMonth)
  labelMonths(labels, results)
  indices = labels[:-1]
  table = pd.DataFrame(results, columns=labels) \
            .set_index(indices)
  if table.empty:
    table = "No records in database"
  else:
    table = table.to_string(sparsify=not consistentColumns,
                            header=not noHeaders,
                            index_names= not noHeaders)
  print(table)
  return table
