$.validator.addMethod("isfuturedate", function (value, element, params) {
    if (value !== "__/__/____" && value !== "") {
        var dd = value.substr(0, 2);
        var mm = value.substr(2, 2);
        var yyyy = value.substr(5, 4);
        var fdtDate = dd + "/" + mm + "/" + yyyy;
        fdtDate = Date.parse(fdtDate);      // console.log(fdtDate);       
        var ldtCurrentDate = new Date();
        if (fdtDate > ldtCurrentDate) {
            return false;
        }
    }
    return true;
});

$.validator.unobtrusive.adapters.add("isfuturedate", function (options) {
    if (options.element.tagName.toUpperCase() === "INPUT" && options.element.type.toUpperCase() === "TEXT") {
        options.rules["isfuturedate"] = true;
        if (options.message) {
            options.messages["isfuturedate"] = options.message;
        }
    }
});

$.validator.addMethod("onlywhitespace", function (value, element, params) {
    if (value.trim() === "") {
        return false;
    }
    return true;
});

$.validator.unobtrusive.adapters.add("onlywhitespace", function (options) {
    if (
        (options.element.tagName.toUpperCase() === "INPUT" && options.element.type.toUpperCase() === "TEXT")
        || (options.element.tagName.toUpperCase() === "TEXTAREA")
        ) {
        options.rules["onlywhitespace"] = true;
        if (options.message) {
            options.messages["onlywhitespace"] = options.message;
        }
    }
});

$.validator.addMethod("servicenumber", function (value, element, params) {

    if (value.trim() !== "") {
        var a = value.split("");
        var countDash = 0;
        var countChar = 0;
        for (var index = 0; index < a.length; index++) {
            console.log(a[index]);
            if (a[index] === '-') {
                countDash = countDash + 1;
            }
            if (a[index] >= 'A' && a[index] <= 'Z') {
                countChar = countChar + 1;
            }
            if (a[index] >= 'a' && a[index] <= 'z') {
                countChar = countChar + 1;
            }
            if (countDash > 1 || countChar > 2)
                return false;

        }

    }
    return true;
});

$.validator.unobtrusive.adapters.add("servicenumber", function (options) {
    if (
        (options.element.tagName.toUpperCase() === "INPUT" && options.element.type.toUpperCase() === "TEXT")
    ) {
        options.rules["servicenumber"] = true;
        if (options.message) {
            options.messages["servicenumber"] = options.message;
        }
    }
});

(function ($) {
    if ($.validator) {
        //get the reference to the original function into a local variable
        var _getLength = $.validator.prototype.getLength;

        //overwrite existing getLength of validator
        $.validator.prototype.getLength = function (value, element) {

            //double count line breaks for textareas only
            if (element.nodeName.toLowerCase() === 'textarea') {

                //Counts all the newline characters (\r = return for macs, \r\n for Windows, \n for Linux/unix)
                var newLineCharacterRegexMatch = /\r?\n|\r/g;

                //use [element.value] rather than [value] since I found that the value passed in does cut off leading and trailing line breaks.
                if (element.value) {

                    //count newline characters
                    var regexResult = element.value.match(newLineCharacterRegexMatch);
                    var newLineCount = regexResult ? regexResult.length : 0;

                    //replace newline characters with nothing
                    var replacedValue = element.value.replace(newLineCharacterRegexMatch, "");

                    //return the length of text without newline characters + doubled newline character count
                    return replacedValue.length + (newLineCount * 2);
                } else {
                    return 0;
                }
            }
            //call the original function reference with apply
            return _getLength.apply(this, arguments);
        };
    }
})(jQuery);