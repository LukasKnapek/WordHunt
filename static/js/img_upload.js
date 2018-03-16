$(document).ready(function() {
    $("#checkbox_scrap_gps").click(function() {
        var disable_gps_fields = $("#checkbox_scrap_gps").prop("checked");
        $("#latitude_field").prop("disabled", disable_gps_fields);
        $("#longitude_field").prop("disabled", disable_gps_fields);
    })
});