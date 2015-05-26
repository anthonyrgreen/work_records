/*$(function () {
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
});*/

dummyData = [ { 'count' : 123, 'module' : 'R', 'user' : 'wellman'}
            , { 'count' : 100, 'module' : 'R', 'user' : 'carmenal'}
            , { 'count' : 50, 'module' : 'gcc', 'user' : 'bergis'}
            , { 'count' : 30, 'module' : 'gcc', 'user' : 'wellman'} ]
dummyOpts = ['module', 'user']

buildDataTree = function (aggregationOrdering, info) {
// ex: aggregationOrdering = ['module', 'user']
// dict = [(123, 'R', 'wellman'), (100, 'R', 'carmenal'),
//         (50, 'gcc', 'bergis'), (30, 'gcc', 'wellman')]
// -> { 'R'   : { 'wellman' : 123
//              , 'carmenal' : 100 }
//    , 'gcc' : { 'bergis' : 50 
//              , 'wellman' : 30 } }
// TODO: add ascending/descending option
  /*var idxDict = { 'count'     : 0
                , 'module'    : 1
                , 'version'   : 3
                , 'username'  : 2 }*/ // TODO: figure out how indexing works
                                    // (send dicts from server?)

  // add inserElt to dict in-place, branching down aggregationOrdering's
  // opts in a tree-like fashion
  var addToDict = function (dict, insertElt) {
    var localDict = dict

    for (var i = 0; i < aggregationOrdering.length; i++) {
      var insertKey = insertElt[aggregationOrdering[i]]
      if (i < aggregationOrdering.length - 1) {
        if (localDict[insertKey] === undefined)
          localDict[insertKey] = {}
        localDict = localDict[insertKey]
      }
      else
        localDict[insertKey] = insertElt['count']
    }

    return dict
  }

  return foldl (addToDict, {}, info);
}

foldl = function (fun, acc, list) {
  for (var i = 0; i < list.length; i++)
    acc = fun(acc, list[i])
  return acc
}
buildDataGraph = function (dataTree, aggregationOrdering) {

}
