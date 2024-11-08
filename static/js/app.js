$(document).ready(function() {
    $('.like-btn').click(function() {
        var postId = $(this).data('post-id');
        var likeBtn = $(this);

        $.ajax({
            url: "{% url 'like_unlike_post' %}",
            method: "POST",
            data: {
                'post_id': postId,
                'csrfmiddlewaretoken': '{{ csrf_token }}'
            },
            success: function(response) {
                if (response.liked) {
                    likeBtn.html('<i class="fas fa-thumbs-up"></i> (' + response.total_likes + ')');
                } else {
                    likeBtn.html('<i class="far fa-thumbs-up"></i> (' + response.total_likes + ')');
                }
            },
            error: function(xhr, status, error) {
                console.error(error);
            }
        });
    });
});