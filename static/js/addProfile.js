$(document).ready(function() {
    $("#keyPhrases").tagit(
        {
            allowSpaces: true,
            placeholderText: "add key phrases..",
            availableTags: ["c++", "java", "php", "javascript", "ruby", "python", "c"],
        }
    );

    $("#add-button").click(function (event) {
        
        // Get Name
        var name = document.getElementById("inputName").value;
        // Get Path
        var path = document.getElementById("inputPath").value;
        // Get Phrases
        var phrases = $("#keyPhrases").tagit("assignedTags");
        // Get Samples
        var sampleSet = [];
        var entries = jQuery('#sampleFields .form-row');
        for (i=0; i<entries.length; i++){
            var id = entries[i].querySelectorAll("input")[0].value;
            var page = entries[i].querySelectorAll("input")[1].value;
            sampleSet.push(String(id)+";"+String(page));  
        };

        // Create a FormData object 
        var data = new FormData();
        // add to the formData
        data.append("name", String(name));
        data.append("path", String(path));
        data.append("sampleSet", Array(sampleSet));
        data.append("phrases", Array(phrases))

        $.ajax({
            type: "POST",
            enctype: 'multipart/form-data',
            url: "{% url 'addProfile' %}",
            data: data,
            processData: false,
            contentType: false,
            cache: false,
            timeout: 600000,
            success: function (mssg) {    
                mySnackbar(mssg);
                alert(mssg);
            },
            error: function (e) {        
                console.log("ERROR : ", e);  
            }
        });
    });  
});


var num = 1;
function addSampleField() {
    num++;
    event.preventDefault()
    var objTo = document.getElementById('sampleFields');
    var divtest = document.createElement("div");

    divtest.setAttribute("class", "form-row align-items-center removeClass"+num);
    var rdiv = 'removeclass'+num;

    divtest.innerHTML = '<div class="col-auto"><label class="sr-only" for="inputID">id</label><div class="input-group mb-2"><div class="input-group-prepend"><div class="input-group-text">id</div></div><input type="number" step=1 class="form-control" id="inputID" placeholder="sample id.." required></div></div><div class="col-auto"><label class="sr-only" for="inputPage">page</label><div class="input-group mb-2"><div class="input-group-prepend"><div class="input-group-text">page</div></div><input type="number" step=1 class="form-control" id="inputPage" placeholder="page number.." required></div></div><div class="col-auto"><button class="btn btn-primary mb-2" id="'+num+'"onclick="addSampleField()">add more...</button></div>';
    objTo.appendChild(divtest);

    var button = document.getElementById(String(num-1));
    button.setAttribute('onclick', 'removeSampleField('+String(num-1)+')');
    button.setAttribute('class', 'btn btn-danger');
    button.innerHTML= 'remove..';
};

function mySnackbar(text) {
    // Get the snackbar DIV
    var x = document.getElementById("snackbar");
    x.innerHTML=text

    // Add the "show" class to DIV
    x.className = "show";

    // After 3 seconds, remove the show class from DIV
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
}

function removeSampleField(num) {
    var sample = document.getElementsByClassName('removeClass'+String(num));
    sample[0].remove();  
};

function stopRKey(evt) { 
    var evt = (evt) ? evt : ((event) ? event : null); 
    var node = (evt.target) ? evt.target : ((evt.srcElement) ? evt.srcElement : null); 
    if ((evt.keyCode == 13) && (node.type=="text"))  {return false;} 
    }; 
    
document.onkeypress = stopRKey; 