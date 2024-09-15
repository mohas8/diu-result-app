// static/js/script.js

document.addEventListener('DOMContentLoaded', function () {
    const themeToggleIcon = document.getElementById('theme-toggle-icon');
    const body = document.body;

    // Check local storage for theme preference
    let theme = localStorage.getItem('theme');

    // If no preference, adapt based on Bangladesh time
    if (!theme) {
        const bdTime = new Date().toLocaleString('en-US', { timeZone: 'Asia/Dhaka' });
        const hour = new Date(bdTime).getHours();
        theme = (hour >= 18 || hour < 6) ? 'dark' : 'light';
        localStorage.setItem('theme', theme);
    }

    // Apply theme
    if (theme === 'dark') {
        body.classList.add('dark-mode');
    }

    // Function to toggle theme
    function toggleTheme() {
        body.classList.toggle('dark-mode');
        let theme = body.classList.contains('dark-mode') ? 'dark' : 'light';
        localStorage.setItem('theme', theme);
        updateIcon();
    }

    // Update the icon based on the theme
    function updateIcon() {
        if (body.classList.contains('dark-mode')) {
            themeToggleIcon.src = "https://img.icons8.com/external-flat-papa-vector/78/external-Light-Mode-interface-flat-papa-vector.png";
        } else {
            themeToggleIcon.src = "https://img.icons8.com/external-glyph-silhouettes-icons-papa-vector/78/external-Light-Mode-interface-glyph-silhouettes-icons-papa-vector.png";
        }
    }

    // Handle icon click
    if (themeToggleIcon) {
        themeToggleIcon.addEventListener('click', toggleTheme);

        // Initialize icon
        updateIcon();
    }
});
