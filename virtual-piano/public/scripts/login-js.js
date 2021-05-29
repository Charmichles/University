const redirectButton1 = document.getElementById('login-to-register-button');
const redirectButton2 = document.getElementById('register-to-login-button');
const logoutButton = document.getElementById('logout-button');
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');
const accountInfo = document.getElementById('account-info');

const loggedin = window.localStorage.getItem('loggedin');

function toggleFormsButton() {
    loginForm.classList.toggle('inactive');
    registerForm.classList.toggle('inactive');
}

function toggleFormsLogin() {
    loginForm.classList.toggle('inactive');
    accountInfo.classList.toggle('inactive');
}

function logout() {
    window.localStorage.removeItem('loggedin');
    toggleFormsLogin();
    loginButton.innerHTML = "Login";
}

const infoUsername = document.getElementById('info-username');
const infoEmail = document.getElementById('info-email');
const infoLevel = document.getElementById('info-level');
const infoPoints = document.getElementById('info-points');
const infoSub = document.getElementById('info-subscribed');

function displayUserInfo(user) {
    infoUsername.innerHTML = "Username: ".concat(user.username);
    infoEmail.innerHTML = "Email: ".concat(user.email);
    infoLevel.innerHTML = "Knowledge level: ".concat(user.level);
    infoPoints.innerHTML = "Points: ".concat(user.points);
    if (user.tips === 'on') {
        infoSub.innerHTML = 'You are subscribed to weekly tips.';
    }
    else {
        infoSub.innerHTML = 'You are not subscribed to weekly tips.';
    }
}

if (loggedin !== null) {
    toggleFormsLogin();
    displayUserInfo(JSON.parse(window.localStorage.getItem("user".concat(loggedin.toString(10)))));
}

redirectButton1.addEventListener('click', () => toggleFormsButton());
redirectButton2.addEventListener('click', () => toggleFormsButton());
logoutButton.addEventListener('click', () => logout());

function findUser(nrOfUsers, username) {
    let flag = false;
    let matching_user = undefined;
    for (let i = 0; i < nrOfUsers && flag === false; i++) {
        const user = JSON.parse(window.localStorage.getItem('user'.concat(i.toString(10))));
        if (user.username == username) {
            flag = true;
            matching_user = user;
        }
    }
    return matching_user;
}

function registerFunc(form) {
    const nrOfUsers = parseInt(window.localStorage.getItem('nrOfUsers'), 10);
    const user = {
        id: nrOfUsers.toString(10),
        username: form.elements["username"].value,
        email: form.elements["email"].value,
        password: form.elements["password"].value,
        level: form.elements["level"].value,
        tips: form.elements["tips"].value,
        points: '0'
    };
    const flag = findUser(nrOfUsers, user.username);
    if (flag !== undefined) {
        Swal.fire("Username is already taken!");
        return;
    }
    window.localStorage.setItem('user'.concat(nrOfUsers.toString(10)), JSON.stringify(user));
    window.localStorage.setItem('nrOfUsers', nrOfUsers + 1);
    toggleFormsButton();
}

function loginFunc(form) {
    const username = form.elements["login-username"].value;
    const password = form.elements["login-password"].value;
    const nrOfUsers = window.localStorage.getItem('nrOfUsers');
    const matching_user = findUser(nrOfUsers, username);
    if (matching_user === undefined) {
        Swal.fire({
            icon: 'error',
            title: 'Error!',
            text: 'Username not found!'
        });
    }
    else if (password != matching_user.password) {
        Swal.fire({
            icon: 'error',
            title: 'Error!',
            text: 'Password does not match!'
        });
    }
    else {
        Swal.fire('Logged in!', 'Credentials matched.' , 'success');
        window.localStorage.setItem('loggedin', matching_user.id);
        toggleFormsLogin();
        displayUserInfo(matching_user);
        loginButton.innerHTML = "Account";
    }
}