const updateProfile = async () => {
    const formData = new FormData();
    formData.append('username', document.getElementById('username').value);
    formData.append('first_name', document.getElementById('first_name').value);
    formData.append('last_name', document.getElementById('last_name').value);
    formData.append('email', document.getElementById('email').value);
    formData.append('image', document.getElementById('profile_image').files[0]);

    const response = await fetch('/api/profile/update/', {
        method: 'PUT',
        body: formData,
        headers: {
            'X-CSRFToken': getCSRFToken(),  // If using Django’s CSRF protection
        }
    });

    if (response.ok) {
        alert('Profile updated successfully');
    } else {
        const data = await response.json();
        console.error(data);
        alert('Failed to update profile');
    }
}
