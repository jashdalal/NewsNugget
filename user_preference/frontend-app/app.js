const backendLocalUrl = "http://localhost:3000/submit"

document.getElementById('userForm').addEventListener('submit', function(event) {
    const formData = new FormData(this);
    const preferences = formData.getAll('preferences');
    const userData = {
        email: formData.get('email'),
        preferences: preferences
    };
    console.log(userData);

    fetch(backendLocalUrl, {
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
        alert(error);
    });
});
