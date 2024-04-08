document.getElementById('userForm').addEventListener('submit', function(event) {
    const formData = new FormData(this);
    const preferences = formData.getAll('preferences');
    const userData = {
        email: formData.get('email'),
        preferences: preferences
    };
    console.log(userData);

    fetch('http://localhost:3000/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Form submitted successfully:', data);
        alert('Form submitted successfully!');
    })
    .catch(error => {
        console.error('Error submitting form:', error);
        alert('Error submitting form. Please try again.');
    });
});
