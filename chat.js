/**
 * DHANVANTRE — CASE WORKSPACE CONTROLLER
 * Case Record Management & Multi-tab Navigation
 */

document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    initCaseTabs();
    initExportSummary();
});

/* 1. Theme Toggle */
function initThemeToggle() {
    const themeBtn = document.getElementById('themeToggleBtn');
    const themeIcon = document.getElementById('themeIcon');
    const htmlEl = document.documentElement;

    const savedTheme = localStorage.getItem('dhanvantre_theme') || 'light';
    htmlEl.setAttribute('data-theme', savedTheme);
    if (themeIcon) themeIcon.className = savedTheme === 'light' ? 'fa-solid fa-moon' : 'fa-solid fa-sun';

    if (themeBtn) {
        themeBtn.addEventListener('click', () => {
            const currentTheme = htmlEl.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            htmlEl.setAttribute('data-theme', newTheme);
            localStorage.setItem('dhanvantre_theme', newTheme);
            if (themeIcon) themeIcon.className = newTheme === 'light' ? 'fa-solid fa-moon' : 'fa-solid fa-sun';
        });
    }
}

/* 2. Case Workspace Tab Switching */
function initCaseTabs() {
    const tabButtons = document.querySelectorAll('.case-nav-tab-btn');
    const tabPanes = document.querySelectorAll('.case-tab-pane');

    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.getAttribute('data-target');
            if (!targetId) return;

            // Deactivate all buttons & panes
            tabButtons.forEach(b => {
                b.classList.remove('active');
                b.setAttribute('aria-selected', 'false');
            });
            tabPanes.forEach(pane => pane.classList.remove('active'));

            // Activate chosen tab & pane
            btn.classList.add('active');
            btn.setAttribute('aria-selected', 'true');
            const targetPane = document.getElementById(targetId);
            if (targetPane) {
                targetPane.classList.add('active');
            }
        });
    });
}

/* 3. Export Case Summary */
function initExportSummary() {
    const exportBtn = document.getElementById('exportCaseBtn');
    if (exportBtn) {
        exportBtn.addEventListener('click', () => {
            window.print();
        });
    }
}
