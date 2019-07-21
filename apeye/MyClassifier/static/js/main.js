
$("#button2").click(function () {
    $.ajax({
        url: "http://127.0.0.1:8000/MyClassifier/login/",
        type: "POST",
        dataType: "json",
        data: {
            "username": document.getElementById('username').value,
            "password": document.getElementById('password').value
        },
        success: function (data) {
            var json = JSON.parse(data);
            console.log(json);
        },
        done: function (result) {
            console.log(result)
        },
        error: function (jqXHR, exception) {
            if (jqXHR.status === 0) {
                alert('Not connect.\n Verify Network.');
            } else if (jqXHR.status == 404) {
                alert('Requested page not found. [404]');
            } else if (jqXHR.status == 500) {
                alert('Internal Server Error [500].');
            } else if (exception === 'parsererror') {
                alert('Requested JSON parse failed.');
            } else if (exception === 'timeout') {
                alert('Time out error.');
            } else if (exception === 'abort') {
                alert('Ajax request aborted.');
            } else {
                alert('Uncaught Error.\n' + jqXHR.responseText);
            }
        }
    });

});