/**
 * AURAMED AI — LOADING & ERROR STATES CONTROLLER
 */

document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    initNetworkStatusListener();
    initRetryHandler();
    initOfflineSimulator();
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

/* 2. Network Status Listener (navigator.onLine) */
function initNetworkStatusListener() {
    const banner = document.getElementById('offlineBanner');
    const label = document.getElementById('networkStatusLabel');

    const updateStatus = () => {
        if (!navigator.onLine) {
            banner.classList.remove('hidden');
            if (label) label.innerHTML = `Network Status: <span style="color: var(--accent-rose);">OFFLINE 🚫</span>`;
        } else {
            banner.classList.add('hidden');
            if (label) label.innerHTML = `Network Status: <span style="color: var(--accent-emerald);">ONLINE 📶</span>`;
        }
    };

    window.addEventListener('online', updateStatus);
    window.addEventListener('offline', updateStatus);
    updateStatus();
}

/* 3. API Failure Retry Handler */
function initRetryHandler() {
    const retryBtn = document.getElementById('retryActionBtn');
    const statusText = document.getElementById('retryStatusText');

    if (retryBtn) {
        retryBtn.addEventListener('click', () => {
            retryBtn.disabled = true;
            retryBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Retrying Request...`;
            statusText.innerText = 'Connecting to backup cluster node...';

            setTimeout(() => {
                retryBtn.disabled = false;
                retryBtn.innerHTML = `<i class="fa-solid fa-check"></i> Connection Restored!`;
                retryBtn.style.background = 'var(--accent-emerald)';
                statusText.innerHTML = `<span style="color: var(--accent-emerald); font-weight: 700;">API Request Succeeded (200 OK)</span>`;
            }, 1800);
        });
    }
}

/* 4. Offline Simulator Toggle */
function initOfflineSimulator() {
    const toggleBtn = document.getElementById('toggleOfflineSimBtn');
    const banner = document.getElementById('offlineBanner');
    let simulatedOffline = false;

    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            simulatedOffline = !simulatedOffline;
            if (simulatedOffline) {
                banner.classList.remove('hidden');
                toggleBtn.innerHTML = `<i class="fa-solid fa-toggle-off"></i> Restore Online State`;
            } else {
                banner.classList.add('hidden');
                toggleBtn.innerHTML = `<i class="fa-solid fa-toggle-on"></i> Toggle Offline Alert`;
            }
        });
    }
}
