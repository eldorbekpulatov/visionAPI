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

            $.ajax({
                type: "POST",
                enctype: 'multipart/form-data',
                url: window.location.pathname,
                data: data,
                processData: false,
                contentType: false,
                cache: false,
                timeout: 600000,
                success: function (data) {   
                    console.log("SUCCESS", data );
                    $('#response').html('<code style="max-width:90%; max-height:60%;">'+JSON.stringify(data)+'</code>');
                },
                error: function (e) {        
                    console.log("ERROR : ", e);  
                }
            });
        });  
    });


