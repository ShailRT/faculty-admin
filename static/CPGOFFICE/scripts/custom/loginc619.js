/// <reference path="../Hashing/md5.js" />
/// <reference path="../Hashing/sha512.min.js" />


$(function () {
    $("#UsernameOffice").focus();
    //$("#Username").val("");
    //$("#TempPassword").val("");
    $("#PasswordOffice").val("");
});

$(document).keypress(function (e) {
    //if (e.which === 13) {
    //    e.preventDefault();
    //}
});

function hashPassword(randomString) {
    var password = $("#TempPasswordOffice").val();
    if (password !== "") {
        var md5Password = md5(password).toLowerCase();
        var hashedPassword = sha512(md5Password).toUpperCase();
        var saltedPassword = hashedPassword + randomString;
        var doubleHashedPassword = sha512(saltedPassword).toUpperCase();
        $("#PasswordOffice").val(doubleHashedPassword);
        $("#TempPasswordOffice").val("********");
    }
}