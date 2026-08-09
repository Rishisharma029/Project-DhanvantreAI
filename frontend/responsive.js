/**
 * AURAMED AI — RESPONSIVE MOBILE UI SIMULATOR CONTROLLER
 */

document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    initViewportSwitcher();
    initPageSelector();
});

/* 1. Theme Toggle */
function initThemeToggle() {
    const themeBtn = document.getElementById('themeToggleBtn');
    const themeIcon = document.getElementById('themeIcon');
    const htmlEl = document.documentElement;

    const savedTheme = localStorage.getItem('auramed_theme') || 'dark';
    htmlEl.setAttribute('data-theme', savedTheme);
    if (themeIcon) themeIcon.className = savedTheme === 'light' ? 'fa-solid fa-sun' : 'fa-solid fa-moon';

    if (themeBtn) {
        themeBtn.addEventListener('click', () => {
            const currentTheme = htmlEl.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            htmlEl.setAttribute('data-theme', newTheme);
            localStorage.setItem('auramed_theme', newTheme);
            if (themeIcon) themeIcon.className = newTheme === 'light' ? 'fa-solid fa-sun' : 'fa-solid fa-moon';
        });
    }
}

/* 2. Device Viewport Switcher */
function initViewportSwitcher() {
    const btnDesktop = document.getElementById('btnDesktop');
    const btnTablet = document.getElementById('btnTablet');
    const btnMobile = document.getElementById('btnMobile');
    const frame = document.getElementById('deviceFrame');
    const label = document.getElementById('activeViewportLabel');

    const resetActive = () => {
        btnDesktop.classList.remove('active');
        btnTablet.classList.remove('active');
        btnMobile.classList.remove('active');

        frame.className = 'device-frame';
    };

    btnDesktop.addEventListener('click', () => {
        resetActive();
        btnDesktop.classList.add('active');
        frame.classList.add('device-desktop');
        label.innerText = 'Desktop View (1360px × 750px)';
    });

    btnTablet.addEventListener('click', () => {
        resetActive();
        btnTablet.classList.add('active');
        frame.classList.add('device-tablet');
        label.innerText = 'Tablet View (768px × 800px)';
    });

    btnMobile.addEventListener('click', () => {
        resetActive();
        btnMobile.classList.add('active');
        frame.classList.add('device-mobile');
        label.innerText = 'Mobile View (375px × 720px)';
    });
}

/* 3. Page Module Selector */
function initPageSelector() {
    const select = document.getElementById('modulePageSelect');
    const iframe = document.getElementById('simIframe');

    if (select && iframe) {
        select.addEventListener('change', (e) => {
            iframe.src = e.target.value;
        });
    }
}
