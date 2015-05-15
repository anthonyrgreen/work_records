$(function () {
  $("#outputType").submit(function (event) {
    event.preventDefault();
    formdata = $("#outputType").serializeArray();
    if(formdata.length != 0)
      outputType = formdata[0]["value"];
    if(!outputType) {
      console.log("no input");
    }
    else {
      switch (outputType) {
        case 'date':
          console.log("date func");
          $(this).append(timeForm);
          break;
        case 'user':
          console.log("user func");
          break;
        case 'package':
          console.log("package func");
          break;
        default:
          console.log("error func");
          break;
      }
    }
    event.preventDefault();
  });
});

timeForm =  '<p> For which times would you like data?' +
            '<form action="" method="get" id="dateForm">' +
              '<p>Start date: <input type="text" name="startDate">' +
              '<p>End date: <input type="text" name="endDate">' +
              '<p><input type="Submit"/>' +
            '</form>';
