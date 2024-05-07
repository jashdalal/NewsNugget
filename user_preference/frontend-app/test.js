document
  .getElementById("userForm")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent default form submission

    // Get email input value
    const email = document.getElementById("email").value;
    console.log("Email:", email);

    // Get selected preferences
    const preferences = [];
    const checkboxes = document.getElementsByName("preferences");
    checkboxes.forEach(function (checkbox) {
      if (checkbox.checked) {
        preferences.push(checkbox.value);
      }
    });
    console.log("Selected Preferences:", preferences);

    // Perform validation
    if (email.trim() === "") {
      alert("Please enter your email.");
      return;
    }

    if (preferences.length === 0) {
      alert("Please select at least one preference.");
      return;
    }

    // If all validations pass, you can proceed with form submission or further processing
    // For now, let's just log a success message
    console.log("Form submitted successfully!");
  });