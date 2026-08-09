/**
 * AURAMED AI — ACCESSIBILITY PORTAL CONTROLLER
 */

document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    initKeyboardShortcuts();
    initScreenReaderAnnouncer();
    initHighContrastToggle();
    initFontScaleButtons();
    applySavedFontScale();
});

/* 1. Theme Toggle */
function initThemeToggle() {
    const themeBtn = document.getElementById('themeToggleBtn');
    const themeIcon = document.getElementById('themeIcon');
    const htmlEl = document.documentElement;

    const savedTheme = localStorage.getItem('auramed_theme') || 'dark';
    htmlEl.setAttribute('data-theme', savedTheme);
    if (themeIcon) themeIcon.className = savedTheme === 'light' ? 'fa-solid fa-sun' : 'fa-solid fa-moon';
}

/* 2. Global Keyboard Shortcuts */
function initKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        if (e.altKey && e.key.toLowerCase() === 's') {
            e.preventDefault();
            const searchInput = document.querySelector('input[type="text"]');
            if (searchInput) {
                searchInput.focus();
                announceToScreenReader('Focused search input.');
            }
        }

        if (e.altKey && e.key.toLowerCase() === 'e') {
            e.preventDefault();
            window.location.href = 'emergency.html';
        }

        if (e.altKey && e.key.toLowerCase() === 'h') {
            e.preventDefault();
            toggleHighContrast();
        }
    });
}

/* 3. Screen Reader WAI-ARIA Announcer */
function initScreenReaderAnnouncer() {
    const testBtn = document.getElementById('testSrAnnounceBtn');
    if (testBtn) {
        testBtn.addEventListener('click', () => {
            announceToScreenReader('Screen Reader Alert: Diagnostic report analysis completed successfully.');
        });
    }
}

function announceToScreenReader(message) {
    const srBox = document.getElementById('srLiveAnnouncer');
    if (srBox) {
        srBox.innerText = message;
    }
}

/* 4. High Contrast Theme Mode */
function initHighContrastToggle() {
    const btn = document.getElementById('toggleHighContrastBtn');
    if (btn) {
        btn.addEventListener('click', () => {
            toggleHighContrast();
        });
    }
}

function toggleHighContrast() {
    const htmlEl = document.documentElement;
    const current = htmlEl.getAttribute('data-theme');

    if (current === 'high-contrast') {
        htmlEl.setAttribute('data-theme', 'dark');
        localStorage.setItem('auramed_theme', 'dark');
        announceToScreenReader('High Contrast theme disabled. Dark theme restored.');
    } else {
        htmlEl.setAttribute('data-theme', 'high-contrast');
        localStorage.setItem('auramed_theme', 'high-contrast');
        announceToScreenReader('High Contrast theme enabled.');
    }
}

/* 5. Font Scale Buttons */
function initFontScaleButtons() {
    const btns = document.querySelectorAll('.font-scale-btn');
    btns.forEach(btn => {
        btn.addEventListener('click', () => {
            btns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const scale = btn.getAttribute('data-scale');
            setFontScale(scale);
        });
    });
}

function setFontScale(scale) {
    const htmlEl = document.documentElement;
    htmlEl.classList.remove('font-scale-sm', 'font-scale-md', 'font-scale-lg', 'font-scale-xl');
    htmlEl.classList.add(`font-scale-${scale}`);
    localStorage.setItem('auramed_font_scale', scale);
    announceToScreenReader(`Font size scaled to ${scale.toUpperCase()}`);
}

function applySavedFontScale() {
    const saved = localStorage.getItem('auramed_font_scale') || 'md';
    setFontScale(saved);

    const activeBtn = document.querySelector(`.font-scale-btn[data-scale="${saved}"]`);
    if (activeBtn) {
        document.querySelectorAll('.font-scale-btn').forEach(b => b.classList.remove('active'));
        activeBtn.classList.add('active');
    }
}
