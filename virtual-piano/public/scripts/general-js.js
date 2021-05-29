const loginButton = document.getElementById('login-button');

if (window.localStorage.getItem('loggedin') !== null) {
    loginButton.innerHTML = "Account";
}

if (window.localStorage.getItem('nrOfUsers') === null) {
    window.localStorage.setItem('nrOfUsers', 0);
}