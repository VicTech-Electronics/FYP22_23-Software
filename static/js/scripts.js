// script.js

// Add any JavaScript code or functionality you need for your web pages

// Example: Handle form submission for customer registration/login
const form = document.getElementById('login-form');

form.addEventListener('submit', (event) => {
  event.preventDefault();

  // Perform form validation and submit data to the server
  // You can use AJAX or fetch API to send data to the server and handle the response
  // Example:
  // const formData = new FormData(form);
  // const data = Object.fromEntries(formData.entries());
  // fetch('/login', {
  //   method: 'POST',
  //   body: JSON.stringify(data),
  //   headers: {
  //     'Content-Type': 'application/json'
  //   }
  // })
  // .then(response => response.json())
  // .then(data => {
  //   // Handle the server response
  // })
  // .catch(error => {
  //   // Handle any errors that occurred during the request
  // });
});
