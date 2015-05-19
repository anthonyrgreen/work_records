$(function () {
  /*$("#outputType").submit(function (event) {
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
  });*/
  $("input[value='package']").change( function () {
    console.log("fired.");
    if ($(this)[0].checked) {
      $("input[value='version']").prop("disabled", false);
      console.log("should be enabled");
    }
    else {
      console.log("should be disabled");
      $("input[value='version']").prop("checked", false);
      $("input[value='version']").prop("disabled", true);
    }
  });
  
});
