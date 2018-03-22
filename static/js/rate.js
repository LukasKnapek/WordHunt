$(document).ready(function() {
    $(".rateit").bind('rated', function() {
        var imageId = $(this).attr('id').split("_")[0];
        var rating = $(this).rateit('value');

        console.log("You've given " + rating + " to image " + imageId);

        $.ajax({
            type: "GET",
            data: {
                image_id: imageId,
                rating: rating
            },
            success: updateRating,
            dataType: "json"
        })
    });
});

function updateRating(response) {
    var rating = response["avg_rating"];
    var rounded_rating = rating.toFixed(2);
    console.log(rounded_rating);

    $("#average_rating").text(rounded_rating);
    $("#average_rating").css("font-weight", "Bold");

}