function CompareOldAndNewPassword(oldPassword, newPassword)
{
    if (oldPassword === newPassword) {
        swal({
            title: "Password Error !",
            text: "Old and new password must not be equal.",
            type: "error",
            showCancelButton: false,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "Ok",
            allowEscapeKey: false
        }).then((result) => {
            if (result.value) {
                $("input:password").focus("");
                $("input:password").each(function() {
                    $(this).val("");
                });
                var passwordFields = $("input:password");
                document.getElementById("password_strength").className = "strength" + 0;
                $("#password_description").html("");
            }
        });
        return false;
    }
}

function password_strength(password, language) {

    var desc = new Array();

    if (language === "hi") {

        desc[0] = "बहुत कमज़ोर";
        desc[1] = "कमज़ोर";
        desc[2] = "बेहतर";
        desc[3] = "मध्यम";
        desc[4] = "मज़बूत";
        desc[5] = "ताकतवर";
    }
    else {
        desc[0] = "Very Weak";
        desc[1] = "Weak";
        desc[2] = "Better";
        desc[3] = "Medium";
        desc[4] = "Strong";
        desc[5] = "Strongest";
    }

    document.getElementById("password_description").style.display = "block";

    var points = 0;

    //---- if password is bigger than 8 , give 1 point.
    if (password.length > 8) points++;

    //---- if password has both lowercase and uppercase characters , give 1 point.	
    if ((password.match(/[a-z]/)) && (password.match(/[A-Z]/))) points++;

    //---- if password has at least one number , give 1 point.
    if (password.match(/\d+/)) points++;
    //---- if password has at least one special caracther , give 1 point.
    if (password.match(/.[!,@,#,$,%,^,&,*,?,_,~,-,(,)]/)) points++;
    //---- if password is 10 ,  give 1 point.
    //if (password.length >= 10) points++;
    //---- Showing  description for password strength.
    //document.getElementById('password_description').innerHTML = desc[points];
    $("#password_description").html(desc[points]);
    //---- Changeing CSS class.
    document.getElementById("password_strength").className = "strength" + points;
}


function checkPasswordComplexity(pwd) {
    var lowercaseletter = /[a-z]/.test(pwd);
    var uppercaseletter = /[A-Z]/.test(pwd);
    var digit = /\d/.test(pwd);
    var special = /[\W_]/.test(pwd);
    var highSecurity = lowercaseletter && uppercaseletter && digit && special;
    var higherSecurity = highSecurity && (pwd.length >= 8);
    if (higherSecurity)
        return true;
    else
        return false;
}

//$("#ConfirmPassword").blur(function () {
//    var password = $("#Password").val().trim();
//    var confirmPassword = $("#ConfirmPassword").val().trim();
//    if (password === "") {
//        alert("Please enter password.");
//        $("#Password").focus();
//        return false;
//    }
//    if (password !== confirmPassword) {
//        alert("Password and confirm  password are not equal.");
//        $("#Password").val("");
//        $("#ConfirmPassword").val("");
//        $("#Password").focus();
//        return false;
//    }
//    var hashedPassword = sha512(password);
//    var confPassword = $("#ConfirmPassword").val().trim();
//    var hashedConfPassword = sha512(confPassword);
//    $("#Password").val(hashedPassword);
//    $("#ConfirmPassword").val(hashedConfPassword);
//    return true;
//});


function PwdComplexity(password, language) {
    var passwordLength = password.trim().length;
    if ((passwordLength > 0 && (checkPasswordComplexity(password) === false)) || (passwordLength > 15 || (passwordLength < 8 && passwordLength > 0))) {
        var message = (language === "hi")
            ? "<strong>पासवर्ड नीति :</strong><ul><li>लंबाई में 8-15 वर्ण होने चाहिए। </li><li> 1 बड़ा अक्षर रखना आवश्यक है। </li><li> 1 छोटा अक्षर रखना आवश्यक है। </li><li> 1 अंक रखना आवश्यक है। </li><li> 1 विशेष वर्ण रखना आवश्यक है। </li><ul>"
            : "<strong>Password policy :</strong><ul><li> Must be 8-15 characters in length.</li><li>Must contain 1 capital letter</li><li>Must contain 1 small letter</li><li>Must contain 1 digit</li><li>Must contain 1 special character.</li></ul>";
        $("#Password").val("");
        swal({
            title: "Password Error !",
            html: message,
            type: "error",
            showCancelButton: false,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "Ok",
            allowEscapeKey: false
        }).then((result) => {
            if (result.value) {
                $("#Password").focus();
                document.getElementById("password_strength").className = "strength" + 0;
                $("#password_description").html("");
            }
        });
            
        //,function () {
        //    $("#Password").focus();
        //    document.getElementById("password_strength").className = "strength" + 0;
        //    $("#password_description").html("");
        //});
        return false;
    }
    return true;
}

function HashSha(language) {
    var pwd = $("#Password").val().trim();
    var confirmPwd = $("#ConfirmPassword").val().trim();
    var message;
    
    if (confirmPwd.length > 0 && pwd !== confirmPwd) {
        message = (language === "hi") ? "पासवर्ड और पुष्टि पासवर्ड समान नहीं है।" : "Password and confirm password are not equal.";
        swal({
            title: "Password Error !",
            text: message,
            type: "error",
            showCancelButton: false,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "Ok",
            allowEscapeKey : false
        }).then((result) => {
            if (result.value) {
                $("#Password").val("");
                $("#ConfirmPassword").val("");
                $("#Password").focus();
                document.getElementById("password_strength").className = "strength" + 0;
                $("#password_description").html("");
            }
        });
        return false;
    }
    //if (confirmPassword.length > 0) {
    //    var hashedPassword = sha256(password);
    //    var confPassword = $("#ConfirmPassword").val().trim();
    //    var hashedConfPassword = sha256(confPassword);
    //    $("#Password").val(hashedPassword);
    //    $("#ConfirmPassword").val(hashedConfPassword);
    //    return true;
    //}
    return true;
}

function HashMd5(language) {
    var pwdMd5 = $("#Password").val().trim();
    var confirmPwdMd5 = $("#ConfirmPassword").val().trim();
    var message;

    if (confirmPwdMd5.length > 0 && pwdMd5 !== confirmPwdMd5) {
        message = (language === "hi") ? "पासवर्ड और पुष्टि पासवर्ड समान नहीं है।" : "Password and confirm password are not equal.";
        swal({
            title: "Password Error !",
            text: message,
            type: "error",
            showCancelButton: false,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "Ok",
            allowEscapeKey: false
        }).then((result) => {
            if (result.value) {
                $("#Password").val("");
                $("#ConfirmPassword").val("");
                $("#Password").focus();
                document.getElementById("password_strength").className = "strength" + 0;
                $("#password_description").html("");
            }
        });
        //,function () {
        //    $("#Password").val("");
        //    $("#ConfirmPassword").val("");
        //    $("#Password").focus();
        //    document.getElementById("password_strength").className = "strength" + 0;
        //    $("#password_description").html("");
        //});
        return false;
    }
    if (confirmPwdMd5.length > 0) {
        var hashedPasswordMd5 = md5(pwdMd5);
        var hashedConfirmPasswordMd5 = md5(confirmPwdMd5);
        $("#Password").val(hashedPasswordMd5);
        $("#ConfirmPassword").val(hashedConfirmPasswordMd5);
        return true;
    }
    return true;
}