$(document).ready(function() {
    /*For checkbox and radio button customization*/
    $('input[type="radio"]').iCheck({
        radioClass: 'iradio_square-blue'
    });

    $('input[name=ExService]').on('ifChecked', function () {
        //var radioValue = $(this).val();
        if ($(this).val() === "Y") {
            $("#DefenceServiceAndServiceNo").removeClass("hidden");
            
        } else {
            $("#DefenceServiceAndServiceNo").addClass("hidden");
        }
    });

    /* Bind country */
    $.ajax({
        method: "GET",
        url: "BindData/GetCountry"
    })
        .done(function (country) {
            $.each(country, function () {
                $("#country").append($("<option></option>").val(this.code).text(this.name));
            });
            $("#country").val("001").trigger("change");
        });

    /* Bind state */
    $("#country").change(function () {
        var countryCode = $("#country").val();
        showHideStateDistPin(countryCode);
        $("#state").empty().append($("<option></option>").val("").text("--Select a country first--"));
        if (countryCode === "001") {
            $.ajax({
                method: "GET",
                url: "BindData/GetStates"
            })
                .done(function (states) {
                    $("#state").empty();
                    $("#state").append($("<option></option>").val("").text("--Select a state--"));
                    $.each(states, function () {
                        $("#state").append($("<option></option>").val(this.code).text(this.name));
                    });
                });
        }
    });
    /* Bind district */
    $("#state").change(function () {
        $("#district").html("");
        //$("#district").append($("<option></option>").val("").text("--Select district--"));
        var stateCode = $("#state").val();
        $.ajax({
            method: "GET",
            url: "BindData/GetDistricts",
            data: { stateCode: stateCode },
            dataType: "Json"
        })
            .done(function (states) {
                $.each(states, function () {
                    $("#district").append($("<option></option>").val(this.code).text(this.name));
                });
            });
    });

    /* Bind complainantType */
    $.ajax({
        method: "GET",
        url: "BindData/GetComplainantType"
    })
        .done(function (complainantType) {
            $.each(complainantType, function () {
                $("#DefenceServices").append($("<option></option>").val(this.code).text(this.name));
            });
        });

});

function showHideStateDistPin(countryCode) {
    if (countryCode === "001") {
        $("#stateAndDistrict").show();
        $("#divDistrict").show();
        $("#pincodeAndMobile").show();
    }
    else {
        $("#state").find("option").not(":first").remove();
        //$("#district").empty().append($("<option></option>").val("").text("---Select a state first---"));
        $("#district").find("option").not(":first").remove();
        $("#pincode").val = "";
        $("#stateAndDistrict").hide();
        $("#pincodeAndMobile").hide();
    }

}