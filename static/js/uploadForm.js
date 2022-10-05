var form = document.getElementById("file-upload-form");
var data = new FormData(form);

$(document).ready(function () {

        $("#upload-button").click(function (event) {
    
            //stop submit the form, we will post it manually.
            event.preventDefault();
    
            // Get form
            var form = $('#file-upload-form')[0];
    
            // Create an FormData object 
            var data = new FormData(form);

            // Get user choice
            var choice = $("input[type='radio'][name='choiceApi']:checked").val()

            // If you want to add an extra field for the FormData
            data.append("api_choice", choice);
            // console.log(data)
    
            $.ajax({
                type: "POST",
                enctype: 'multipart/form-data',
                url: "{% url 'faceExtract' %}",
                data: data,
                processData: false,
                contentType: false,
                cache: false,
                timeout: 600000,
                success: function (data) {           
                    console.log("SUCCESS : ", data);
                    document.getElementById('response').innerHTML=JSON.stringify(data);
                },
                error: function (e) {        
                    console.log("ERROR : ", e);  
                }
            });
        });  
    });


