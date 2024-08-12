// Handling login and signup toggles
document.getElementById('toggle-login').addEventListener('click', function() {
    document.getElementById('login-form').classList.add('active');
    document.getElementById('signup-form').classList.remove('active');
    this.classList.add('active');
    document.getElementById('toggle-signup').classList.remove('active');
});

document.getElementById('toggle-signup').addEventListener('click', function() {
    document.getElementById('signup-form').classList.add('active');
    document.getElementById('login-form').classList.remove('active');
    this.classList.add('active');
    document.getElementById('toggle-login').classList.remove('active');
});

function login() {
    // Get the email and password from the input fields
    var email = document.getElementById("login-email").value;
    var password = document.getElementById("login-password").value;

    // Send a request to the server to check the login credentials
    // Replace this with your actual code to send the request
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/login", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({ email: email, password: password }));

    // When the response is received, check if the login was successful
    xhr.onload = function() {
        if (xhr.status === 200) {
            // If the login was successful, redirect to the bookrecommend.html page
            window.location.replace("bookrecommend.html");
        } else {
            // If the login was unsuccessful, show a notification box
            showNotification("Invalid details");
        }
    };
}

function showNotification(message) {
    // Create a notification box
    var notificationBox = document.createElement("div");
    notificationBox.className = "notification-box";
    notificationBox.innerHTML = message;

    // Add the notification box to the page
    document.body.appendChild(notificationBox);

    // Set a timeout to remove the notification box after 2 seconds
    setTimeout(function() {
        notificationBox.parentNode.removeChild(notificationBox);
    }, 2000);
}

// Add event listener to "Get Recommendations" button
document.getElementById('get-recommendations').addEventListener('click', function() {
    var genre = document.getElementById('genre-select').value;
    if (genre) {
        document.getElementById('book-list').innerHTML = 'Loading...';
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/recommend', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({ genre: genre }));

        xhr.onload = function() {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                var bookListHtml = '';
                response.forEach(function(book) {
                    bookListHtml += '<li>' + book.title + ' by ' + book.author + '</li>';
                });
                document.getElementById('book-list').innerHTML = bookListHtml;
            } else {
                showNotification('Error loading recommendations.');
            }
        };
    } else {
        showNotification('Please select a genre.');
    }
});