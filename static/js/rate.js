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
    $("#average_rating").text(response["avg_rating"]);
}