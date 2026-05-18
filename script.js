// User database
const users = {
    'admin': 'password123',
    'member1': 'member123',
    'member2': 'secure456',
    'john': 'john2024',
    'jane': 'jane2024'
};

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    checkSession();
    document.getElementById('loginForm').addEventListener('submit', handleLogin);
});

// Check if user has active session
function checkSession() {
    const currentUser = sessionStorage.getItem('currentUser');
    if (currentUser) {
        showHomePage(currentUser);
    } else {
        showLoginPage();
    }
}

// Show login page
function showLoginPage() {
    document.getElementById('loginPage').classList.remove('hidden');
    document.getElementById('homePage').classList.add('hidden');
}

// Show home page
function showHomePage(username) {
    document.getElementById('loginPage').classList.add('hidden');
    document.getElementById('homePage').classList.remove('hidden');
    document.getElementById('userDisplay').textContent = username;
}

// Handle login
function handleLogin(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorElement = document.getElementById('loginError');
    
    // Clear previous error
    errorElement.textContent = '';
    errorElement.classList.remove('show');
    
    // Validate credentials
    if (users[username] && users[username] === password) {
        // Store session
        sessionStorage.setItem('currentUser', username);
        
        // Reset form
        document.getElementById('loginForm').reset();
        
        // Show home page
        showHomePage(username);
    } else {
        // Show error
        errorElement.textContent = 'Invalid username or password!';
        errorElement.classList.add('show');
    }
}

// Logout function
function logout() {
    sessionStorage.removeItem('currentUser');
    showLoginPage();
    document.getElementById('loginForm').reset();
}
