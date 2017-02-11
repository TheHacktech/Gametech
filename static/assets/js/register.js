$("body").backstretch("/assets/img/moles-01-01.png");
function updatePage(data) {
    if(data.split(" ")[0] === "Thank") { // register success
        document.getElementById("form").innerHTML = '<div id="success" class="label" style="border: 2px; width: 95%">'+data+'</div>';
        $("html, body").animate({ scrollTop: 0 }, "slow");
    } else { // register failure
        document.getElementById("formMessage").innerHTML = data;
        document.getElementById("formMessage").style = "border: 2px; width: 95%;";
        $("html, body").animate({ scrollTop: 0 }, "slow");
        $("#form_message").addClass("failure_flash");
    }
}

function constrain(amt, low, high){
    if(amt < low || amt === null){
        amt = low;
    } else if(amt > high){
        amt = high;
    }
    return amt;
}

function nonneg(amt){
    if(amt < 0 || amt === null){
        amt = 0;
    }
    return amt;
}

function validateEmail(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}

function validate_form() {
    var fname = document.getElementById("fname").value;
    if(fname.length < 1) {
        updatePage("First name is required. Check your input and try again.");
        return false;
    }
    if(fname.length > 64) {
        updatePage("Your first name is too long. Check your input and try again.");
        return false;
    }


    var lname = document.getElementById("lname").value;
    if(lname.length < 1) {
        updatePage("Your last name is required. Check your input and try again.");
        return false;
    } 
    if (lname.length > 64) {
        updatePage("Your last name is too long. Check your input and try again.");
        return false;
    }


    var email = document.getElementById("email").value;
    if (email.length < 6) {
        updatePage("Your email address is required. Check your input and try again.");
        return false;
    }
    if (email.length > 64) {
        updatePage("Your email address is too long. Check your input and try again.");
        return false;
    }
    if (validateEmail(email) === false) {
        updatePage("Your email address is invalid. Check your input and try again.");
        return false;
    }


    var gradeDrop = document.getElementById("gradeDrop").value;
    if(gradeDrop === "default" || (gradeDrop === "other" && (document.getElementById("formTextGrade").value.length < 1 || document.getElementById("formTextGrade").value.length > 32))) {
        updatePage("Your grade is invalid. Check your input and try again.");
        return false;
    }


    if(document.getElementById("school").value.length < 1 || document.getElementById("school").value.length > 64) {
        updatePage("Your school is invalid. Check your input and try again.");
        return false;
    }

    if(document.getElementById("major").value.length < 1 || document.getElementById("major").value.length > 80) {
        updatePage("Your major is invalid. Check your input and try again.");
        return false;
    }

    var buses = ["no", "tech", "stan", "ucb", "uci", "ucla", "ucsd", "usc"]
    if(buses.indexOf(document.getElementById("formSelectBus").value) == -1) {
        updatePage("Your selected bus is invalid. Check your input and try again.\nIf you don't need or want a bus, select 'No Bus Needed'.");
        return false;
    }


    var website = document.getElementById("website").value;
    if (website.length > 80) {
        updatePage("Your personal website url is too long. Check your input and try again.");
        return false;
    }


    var github = document.getElementById("github").value;
    if (github.length > 80) {
        updatePage("Your github url is too long. Check your input and try again.");
        return false;
    }


    var linkedin = document.getElementById("linkedin").value;
    if (linkedin.length > 80) {
        updatePage("Your linkedin url is too long. Check your input and try again.");
        return false;
    }

    if(document.getElementById("poem").value.length < 1) {
        updatePage("Your acrostic poem is invalid. Check your input and try again.");
        return false;
    }
    if(document.getElementById("techsimplify").value.length < 1) {
        updatePage("Your response to the second free-response question is invalid. Check your input and try again.");
        return false;
    }
    if(document.getElementById("hacktechsuggest").value.length < 1) {
        updatePage("Your input for what you'd like to see at Hacktech is invalid. Check your input and try again.");
        return false;
    }
    if(document.getElementById("accept_tos").checked === false) {
        updatePage("You must accept the MLH Code of Conduct to participate at Hacktech.");
        return false;
    }
    var file = document.getElementById("resumefileinput").files[0];
    if(file === undefined) {
        updatePage("You did not upload a resume. Check your input and try again.");
        return false;
    }
    return true;
}

var frm = $('#registerForm');
frm.submit(function (ev) {
    if(validate_form() === true) {
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: new FormData(this),
            //data: frm.serialize(),
            cache: false,
            contentType: false,
            processData: false,
            success: function (data) {
                updatePage(data);
            }
        });
    }
    ev.preventDefault();
});

function checkOther() {
    if(document.getElementById('gradeDrop').value==="other") {
        document.getElementById('gradeDrop').name = "gradeSelect";
        document.getElementById('formTextGrade').name = "grade";
        document.getElementById('formTextGrade').style="width: 30%";
        document.getElementById('gradeDrop').style="width: 30%";
        document.getElementById('gradeExplain').style="border: 2px; width: 30%";
    } else {
        document.getElementById('gradeDrop').name = "grade";
        document.getElementById('formTextGrade').name = "gradeOther";
        document.getElementById('formTextGrade').style="display: none;";
        document.getElementById('gradeDrop').style="width: 50%";
        document.getElementById('gradeExplain').style="border: 2px; width: 40%";
    }
}

function uploadResume() {
    document.getElementById("resumefileinput").click();
}

// Bit of a misnomer. updateBtnTxt also does clientside validation on the resume
function updateBtnTxt() {
    var file = document.getElementById("resumefileinput").files[0];
    MAXFILESIZE = 1048576; // 1MB

    // If they remove the resume, file will be undefined
    if(file == undefined) {
        document.getElementById("resumeUploadBtn").innerHTML = 'Click to Upload'
    } else if (file.size > MAXFILESIZE) {
        updatePage("Your resume is larger than 1MB. Please reduce the size and try again.");
    } else {
        document.getElementById("resumeUploadBtn").innerHTML = file.name;
    }
}

function personalUpdate(id) {
    if(document.getElementById(id).value.length <= 0) {
        document.getElementById(id).value = 'http://';
    }
}

function personalRemove(id) {
    if(document.getElementById(id).value === 'http://') {
        document.getElementById(id).value = "";
    }
}
