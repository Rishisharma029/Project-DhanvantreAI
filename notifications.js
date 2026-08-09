/**
 * AURAMED AI — UNIVERSAL TOAST NOTIFICATION CONTROLLER
 */

document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    initToastTriggers();
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

/* 2. Toast Triggers */
function initToastTriggers() {
    const btnSuccess = document.getElementById('triggerSuccessBtn');
    const btnWarning = document.getElementById('triggerWarningBtn');
    const btnError = document.getElementById('triggerErrorBtn');

    if (btnSuccess) {
        btnSuccess.addEventListener('click', () => {
            showToast('success', 'Profile Updated', 'Patient health profile changes saved to medical database.', 4000);
        });
    }

    if (btnWarning) {
        btnWarning.addEventListener('click', () => {
            showToast('warning', 'Drug Interplay Warning', 'Warfarin + Aspirin co-prescribing increases bleeding risk.', 4000);
        });
    }

    if (btnError) {
        btnError.addEventListener('click', () => {
            showToast('error', '500 Server Error', 'Failed to reach cluster node. Please retry your request.', 4000);
        });
    }
}

/* 3. Universal Toast Dispatcher */
window.showToast = function(type, title, message, duration = 4000) {
    let container = document.getElementById('toastStackContainer');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toastStackContainer';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast-item toast-${type}`;

    let iconClass = 'fa-solid fa-circle-check';
    if (type === 'warning') iconClass = 'fa-solid fa-triangle-exclamation';
    if (type === 'error') iconClass = 'fa-solid fa-circle-xmark';

    toast.innerHTML = `
        <i class="${iconClass} toast-icon" style="font-size: 1.3rem; margin-top: 2px;"></i>
        <div style="flex: 1;">
            <div style="font-weight: 700; font-size: 0.95rem; margin-bottom: 2px;">${escapeHtml(title)}</div>
            <div style="font-size: 0.82rem; color: var(--text-muted);">${escapeHtml(message)}</div>
        </div>
        <button class="toast-close-btn">&times;</button>
    `;

    const closeBtn = toast.querySelector('.toast-close-btn');
    closeBtn.addEventListener('click', () => toast.remove());

    container.appendChild(toast);

    setTimeout(() => {
        if (toast.parentElement) {
            toast.style.animation = 'fadeOut 0.3s forwards';
            setTimeout(() => toast.remove(), 300);
        }
    }, duration);
};

function escapeHtml(str) {
    return String(str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
