const users = {
    'admin':        { password: 'password123',   redirect: null },
    'member1':      { password: 'member123',      redirect: null },
    'member2':      { password: 'secure456',      redirect: null },
    'john':         { password: 'john2024',       redirect: null },
    'jane':         { password: 'jane2024',       redirect: null },
    'ORGANIK3311':    { password: 'SE26-Org',   redirect: null },
    'MITRA3311':  { password: 'SE26-ptg',   redirect: 'organik.html' }
};

document.addEventListener('DOMContentLoaded', function() {
    checkSession();
    document.getElementById('loginForm').addEventListener('submit', handleLogin);
});

function checkSession() {
    const currentUser = sessionStorage.getItem('currentUser');
    if (currentUser) {
        showHomePage(currentUser);
    } else {
        showLoginPage();
    }
}

function showLoginPage() {
    document.getElementById('loginPage').classList.remove('hidden');
    document.getElementById('homePage').classList.add('hidden');
}

function showHomePage(username) {
    document.getElementById('loginPage').classList.add('hidden');
    document.getElementById('homePage').classList.remove('hidden');
    document.getElementById('userDisplay').textContent = username;
}

function handleLogin(e) {
    e.preventDefault();

    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;
    const errorElement = document.getElementById('loginError');

    errorElement.textContent = '';
    errorElement.classList.remove('show');

    const user = users[username];

    if (user && user.password === password) {
        sessionStorage.setItem('currentUser', username);
        document.getElementById('loginForm').reset();

        if (user.redirect) {
            window.location.href = user.redirect;
        } else {
            showHomePage(username);
        }
    } else {
        errorElement.textContent = 'Invalid username or password!';
        errorElement.classList.add('show');
    }
}

function logout() {
    sessionStorage.removeItem('currentUser');
    showLoginPage();
    document.getElementById('loginForm').reset();
}
