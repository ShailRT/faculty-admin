/*===At Least One required Validation===*/
$.validator.unobtrusive.adapters.addSingleVal("atleastonerequired", "otherpropertynames");
$.validator.addMethod("atleastonerequired", function (value, element, params) {
    var param = params.toString().split(',');
    var isAllNull = true;
    $.each(param, function (i, val) {
        var valueOfItem = $("#" + val).val().trim();
        if (valueOfItem !== "") {
            isAllNull = false;
            return false;
        }
    });
    if (isAllNull) {
        return false;
    }
    else {
        return true;
    }
});

/**
 * No future date validation.
 */
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

/*date range*/
function GetDate(value) {
    if (value === "") return "";
    var dd = value.substr(0, 2);
    var mm = value.substr(2, 2);
    var yyyy = value.substr(5, 4);
    var fdtDate = dd + "/" + mm + "/" + yyyy;
    var dt = Date.parse(fdtDate);
    if (dt.getTime() === dt.getTime())
        return dt;
    return "";
}
function IsDate(value) {
    
    return dt.getTime() === dt.getTime();
}
$.validator.addMethod('daterange', function (value, element, params) {
    if (value !== "__/__/____" && value !== "") {
        var fromDate = GetDate($('input[name="' + params.fromdate + '"]').val());
        var toDate = new Date();
        var inputDate = GetDate(value);
        if (fromDate !== "" || toDate !== "" || inputDate !== "" || fromDate > inputDate || inputDate > toDate) {
            var message = $(element).attr('data-val-daterange');
            $.validator.messages.dynamicrange = $.validator.format(message, minValue);
            return false;
        }
    }
    return true;
});

$.validator.unobtrusive.adapters.add('daterange', ['fromdate'], function (options)
{
        options.rules['daterange'] = options.params;
        if (options.message !== null) {
            $.validator.messages.dynamicrange = options.message;
        }
    }
);

/*
 * Category required if available
 */
$.validator.addMethod("categoryrequiredifavailable", function (value, element, params) {
    if ($(element).find("option").length > 1 && value === "") {
        return false;
    }
    return true;
});

$.validator.unobtrusive.adapters.add("categoryrequiredifavailable", function(options) {
    if (options.element.tagName.toUpperCase() === "SELECT") {
        options.rules["categoryrequiredifavailable"] = true;
        if (options.message) {
            options.messages["categoryrequiredifavailable"] = options.message;
        }
    }
});