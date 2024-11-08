// Function to handle profile update via API
async function updateProfile() {
    const formData = new FormData();
    formData.append('username', document.getElementById('username').value);
    formData.append('first_name', document.getElementById('first_name').value);
    formData.append('last_name', document.getElementById('last_name').value);
    formData.append('email', document.getElementById('email').value);
    formData.append('image', document.getElementById('profile_image').files[0]);

    const response = await fetch('update/', {
        method: 'PUT',
        body: formData,
        headers: {
            'X-CSRFToken': csrftoken,  // Use global CSRF token
        }
    });

    if (response.ok) {
        alert('Profile updated successfully');
    } else {
        const data = await response.json();
        alert('Failed to update profile');
        console.error(data);
    }
}

// Function to fetch follow count via API
async function fetchFollowCount() {
    const response = await fetch('follow-count/');
    if (response.ok) {
        const data = await response.json();
        document.getElementById('follow-count').innerText = data.follow_count;
    }
}

// Load follow count on page load
window.onload = fetchFollowCount;

$(document).ready(function() {
    $('.like-btn').click(function() {
        var postId = $(this).data('post-id');
        var likeBtn = $(this);

        $.ajax({
            url: likeUnlikeUrl,  // Define in your template as a variable
            method: "POST",
            data: {
                'post_id': postId,
                'csrfmiddlewaretoken': csrftoken
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

// CSRF token setup
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

// Submit a comment
function submitComment(postId) {
    const content = document.getElementById(`comment-input-${postId}`).value;

    fetch(`/api/posts/${postId}/comment/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ content: content })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            document.getElementById(`comments-list-${postId}`).innerHTML += `
                <li>${content} - by You</li>
            `;
            document.getElementById(`comment-input-${postId}`).value = '';
        } else {
            alert('Error: ' + data.error);
        }
    });
}

// Submit a reply
function submitReply(commentId) {
    const content = document.getElementById(`reply-input-${commentId}`).value;

    fetch(`/api/comments/${commentId}/reply/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ content: content })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            document.getElementById(`replies-list-${commentId}`).innerHTML += `
                <li>${content} - by You</li>
            `;
            document.getElementById(`reply-input-${commentId}`).value = '';
        } else {
            alert('Error: ' + data.error);
        }
    });
}

// Handle post deletion
document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('.delete-button');

    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.getAttribute('data-id');
            const postElement = document.getElementById(`post-${postId}`);

            if (confirm('Are you sure you want to delete this post?')) {
                fetch(`/posts/${postId}/`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.message === 'Post deleted successfully') {
                        postElement.remove();
                        alert(data.message);
                    } else {
                        alert('Failed to delete the post.');
                    }
                });
            }
        });
    });
});
