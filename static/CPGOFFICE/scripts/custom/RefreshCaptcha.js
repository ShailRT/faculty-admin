$(document).ready(function () {
    $("#RefreshCaptcha").on("click", function () {
        var randomTime = (new Date()).getTime();
        document.getElementById("CaptchaImage").src = document.getElementById("CaptchaImage").src + "?" + randomTime;
    });
});