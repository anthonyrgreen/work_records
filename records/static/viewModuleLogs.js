$(function () {
  // Grey out and deselect version when package is unchecked
  $("input[value='package']").change( function () {
    if ($(this)[0].checked) {
      $("input[value='version']").prop("disabled", false);
    }
    else {
      $("input[value='version']").prop("checked", false);
      $("input[value='version']").prop("disabled", true);
    }
  });
});

dummyData = [ { 'count' : 123, 'module' : 'R', 'user' : 'wellman'}
            , { 'count' : 100, 'module' : 'R', 'user' : 'carmenal'}
            , { 'count' : 50, 'module' : 'gcc', 'user' : 'bergis'}
            , { 'count' : 30, 'module' : 'gcc', 'user' : 'wellman'} ]
dummyOpts = ['module', 'user']

// ex: aggregationOrdering = ['module', 'user']
// dict = [(123, 'R', 'wellman'), (100, 'R', 'carmenal'),
//         (50, 'gcc', 'bergis'), (30, 'gcc', 'wellman')]
// -> { 'R'   : { 'wellman'   : { 'count' : 123 }
//              , 'carmenal'  : { 'count' : 100 }
//    , 'gcc' : { 'bergis'    : { 'count' : 50  }
//              , 'wellman'   : { 'count' : 30  } } 
//              }
//    }
buildDataTree = function (aggregationOrdering, info) {
  // private utility function:
  // adds insertElt to dict in-place, branching down aggregationOrdering's
  // opts in a tree-like fashion
  var addToDict = function (dict, insertElt) {
    var localDict = dict
    for (var i = 0; i < aggregationOrdering.length; i++) {
      var insertKey = insertElt[aggregationOrdering[i]]
      localDict[insertKey] = localDict[insertKey] || {}
      localDict = localDict[insertKey]
    }
    localDict['count'] = insertElt['count']
    return dict
  }
  return foldl (addToDict, {}, info);
}

// Given a data tree, make a d3 bar graph from it. Should support up to three
// aggregations, with every level being differentiated by a different style
// option. For instance, if aggregationOrdering = ['module', 'user'], then
// every module should have a single color. If aggregationOrdering = ['module',
// 'version', 'user'], then every  module should have it's own color, every 
// version should have it's own shade (or line-based fill?), and the rest will
// be differentiated by height.
// TODO: add ascending/descending option
buildDataGraph = function (aggregationOrdering, dataTree) {
  // NEED: dataTreeMax
  // NEED: dataTreeSize
  var width = 500,
      height = 400

  var numEntries = dataTreeSize(dataTree)
  var maxEntry = dataTreeMax(dataTree)

  // varying parameters: ['stroke/fill', 'fill-opacity', ???]
  

}

foldl = function (fun, acc, list) {
  for (var i = 0; i < list.length; i++)
    acc = fun(acc, list[i])
  return acc
}
