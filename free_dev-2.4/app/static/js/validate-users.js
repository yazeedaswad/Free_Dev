

document.addEventListener('DOMContentLoaded', function() {
    var employerForm = document.getElementById('employer-registration-form');
    var freelancerForm = document.getElementById('freelancer-registration-form');

    if (employerForm) {
        employerForm.addEventListener('submit', validateRegistration);
    }

    if (freelancerForm) {
        freelancerForm.addEventListener('submit', validateRegistration);
    }
});

function validateRegistration(event) {
    event.preventDefault(); // Prevent default form submission

    var form = event.target; // Get the form that triggered the event
    var email = form.elements['email-address'].value;

    axios.post('/validate-registration', { email: email })
        .then((response) => {
            console.log('Response received:', response.data);
            if (response.data.user_exists) {
                alert('User with provided email already exists. Please login instead.');
            } else {
                console.log('User does not exist. Proceeding with form submission.');
                form.submit(); // Submit the form
            }
        })
        .catch((error) => {
            console.error('Error validating registration:', error);
        });
}



function submitRole() {
    event.preventDefault();  // Prevent the default form submission
    const roleForm = document.getElementById('role-form');  // Assuming your form has an ID
    const formData = new FormData(roleForm);

    fetch('/add-role', {
        method: 'POST',
        body: formData  // Send the form data
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log('Role added successfully');
            alert('Role added successfully');  // Provide user feedback
        } else {
            console.error('Failed to add role:', data.message);
            alert('Failed to add role: ' + data.message);  // Provide user feedback
        }
    })
    .catch(error => {
        console.error('Error adding role:', error);
        alert('Error adding role: ' + error);  // Provide user feedback
    });
}

