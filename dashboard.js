/**
 * DHANVANTRE — CLINICAL WORKSPACE CONTROLLER
 */

const API_BASE = '/api/v1';

document.addEventListener('DOMContentLoaded', async () => {
    initThemeToggle();
    initClinicianMenu();
    initContextualGreeting();
    initSearchShortcut();
    initCaseFilters();
    initNotificationsDrawer();
    initModals();
    initLogout();
    
    // Auth Check & Load Workspace Data
    const token = localStorage.getItem('auramed_access_token');
    if (!token) {
        setupDemoUser();
    } else {
        await loadUserProfile(token);
        await loadReports(token);
        await loadNotifications(token);
    }
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

/* 2. Clinician Dropdown Menu */
function initClinicianMenu() {
    const menuTrigger = document.getElementById('clinicianMenu');
    const dropdown = document.getElementById('clinicianDropdown');

    if (menuTrigger && dropdown) {
        menuTrigger.addEventListener('click', (e) => {
            e.stopPropagation();
            dropdown.classList.toggle('show');
            const isExpanded = dropdown.classList.contains('show');
            menuTrigger.setAttribute('aria-expanded', isExpanded);
        });

        document.addEventListener('click', (e) => {
            if (!menuTrigger.contains(e.target)) {
                dropdown.classList.remove('show');
                menuTrigger.setAttribute('aria-expanded', 'false');
            }
        });
    }
}

/* 3. Contextual Time-of-Day Greeting */
function initContextualGreeting() {
    const greetingEl = document.getElementById('welcomeGreeting');
    if (!greetingEl) return;

    const hour = new Date().getHours();
    let timeGreeting = 'Good evening';
    if (hour < 12) {
        timeGreeting = 'Good morning';
    } else if (hour < 17) {
        timeGreeting = 'Good afternoon';
    }

    const userName = document.getElementById('sidebarUserName')?.innerText.split(' ')[1] || 'Rishi';
    greetingEl.innerText = `${timeGreeting}, Dr. ${userName}`;
}

/* 4. Global Search Keyboard Shortcut (/) */
function initSearchShortcut() {
    const searchInput = document.getElementById('dashGlobalSearch');
    if (!searchInput) return;

    document.addEventListener('keydown', (e) => {
        if (e.key === '/' && document.activeElement !== searchInput && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
            e.preventDefault();
            searchInput.focus();
        } else if (e.key === 'Escape' && document.activeElement === searchInput) {
            searchInput.blur();
        }
    });

    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase().trim();
        const rows = document.querySelectorAll('#reportsTableBody tr');
        rows.forEach(row => {
            const text = row.innerText.toLowerCase();
            row.style.display = text.includes(query) ? '' : 'none';
        });
    });
}

/* 5. Case Table Filter Pills */
function initCaseFilters() {
    const filterButtons = document.querySelectorAll('#casesSection .filter-mode-btn');
    const tableRows = document.querySelectorAll('#reportsTableBody tr');

    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            filterButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const filter = btn.innerText.trim();
            tableRows.forEach(row => {
                if (filter === 'All Cases') {
                    row.style.display = '';
                } else if (filter === 'Reviewing') {
                    const hasReviewing = row.querySelector('.status-reviewing');
                    row.style.display = hasReviewing ? '' : 'none';
                } else if (filter === 'Attention') {
                    const hasAttention = row.querySelector('.status-attention');
                    row.style.display = hasAttention ? '' : 'none';
                }
            });
        });
    });
}

/* 6. User Profile Loading */
async function loadUserProfile(token) {
    try {
        const res = await fetch(`${API_BASE}/auth/me`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!res.ok) throw new Error('Token expired');

        const user = await res.json();
        const initials = user.full_name ? user.full_name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2) : 'DR';

        const avatar = document.getElementById('sidebarAvatar');
        const nameEl = document.getElementById('sidebarUserName');
        const roleEl = document.getElementById('sidebarUserRole');

        if (avatar) avatar.innerText = initials;
        if (nameEl) nameEl.innerHTML = `${user.full_name || 'Dr. Rishi'} <i class="fa-solid fa-chevron-down clinician-chevron"></i>`;
        if (roleEl) roleEl.innerText = user.role || 'Attending Physician';
        
        initContextualGreeting();
    } catch (err) {
        setupDemoUser();
    }
}

function setupDemoUser() {
    const avatar = document.getElementById('sidebarAvatar');
    const nameEl = document.getElementById('sidebarUserName');
    const roleEl = document.getElementById('sidebarUserRole');

    if (avatar) avatar.innerText = 'DR';
    if (nameEl) nameEl.innerHTML = `Dr. Rishi <i class="fa-solid fa-chevron-down clinician-chevron"></i>`;
    if (roleEl) roleEl.innerText = 'Attending Physician';
    
    initContextualGreeting();
}

/* 7. Reports Service */
async function loadReports(token) {
    try {
        const res = await fetch(`${API_BASE}/history/reports`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!res.ok) return;

        const reports = await res.json();
        if (reports && reports.length > 0) {
            const countEl = document.getElementById('valTotalReports');
            if (countEl) countEl.innerText = reports.length;
        }
    } catch (err) {
        console.error('Failed to load reports:', err);
    }
}

/* 8. Notifications Service */
async function loadNotifications(token) {
    try {
        const res = await fetch(`${API_BASE}/notifications/my-notifications`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!res.ok) return;

        const notifs = await res.json();
        const list = document.getElementById('notifList');
        const badge = document.getElementById('notifCountBadge');

        if (notifs && notifs.length > 0) {
            if (badge) badge.innerText = notifs.length;
            if (list) {
                list.innerHTML = notifs.map(n => `
                    <div class="notif-item">
                        <div class="notif-icon"><i class="fa-regular fa-bell" style="color: var(--primary);"></i></div>
                        <div>
                            <div class="notif-title">${escapeHtml(n.title || 'Clinical Notification')}</div>
                            <div class="notif-body">${escapeHtml(n.body || n.message || 'Diagnostic status updated.')}</div>
                            <div class="notif-time">${n.created_at ? n.created_at.slice(0, 10) : 'Today'}</div>
                        </div>
                    </div>
                `).join('');
            }
        }
    } catch (err) {
        console.error('Failed to load notifications:', err);
    }
}

/* 9. Notifications Drawer Controls */
function initNotificationsDrawer() {
    const openBtn = document.getElementById('openNotifBtn');
    const closeBtn = document.getElementById('closeNotifBtn');
    const drawer = document.getElementById('notifDrawer');

    if (openBtn && drawer) {
        openBtn.addEventListener('click', () => drawer.classList.add('open'));
    }
    if (closeBtn && drawer) {
        closeBtn.addEventListener('click', () => drawer.classList.remove('open'));
    }
}

/* 10. Modals Management */
function initModals() {
    const openReportBtn = document.getElementById('openAddReportModalBtn');
    const closeReportBtn = document.getElementById('closeReportModalBtn');
    const reportModal = document.getElementById('reportModal');
    const addReportForm = document.getElementById('addReportForm');

    if (openReportBtn && reportModal) {
        openReportBtn.addEventListener('click', () => reportModal.classList.remove('hidden'));
    }
    if (closeReportBtn && reportModal) {
        closeReportBtn.addEventListener('click', () => reportModal.classList.add('hidden'));
    }

    if (addReportForm) {
        addReportForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const title = document.getElementById('reportTitleInput').value;
            const category = document.getElementById('reportCategorySelect').value;
            const summary = document.getElementById('reportSummaryInput').value;

            const token = localStorage.getItem('auramed_access_token');
            if (token) {
                try {
                    await fetch(`${API_BASE}/history/reports`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${token}`
                        },
                        body: JSON.stringify({
                            report_title: title,
                            category: category,
                            summary_text: summary
                        })
                    });
                } catch (err) {
                    console.error('Save report failed:', err);
                }
            }

            reportModal.classList.add('hidden');
            addReportForm.reset();
        });
    }
}

/* 11. Logout */
function initLogout() {
    const logoutBtn = document.getElementById('sidebarLogoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            localStorage.removeItem('auramed_access_token');
            window.location.href = 'auth.html#login';
        });
    }
}

function escapeHtml(str) {
    if (!str) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

/* ==========================================================================
   10. Live Operational Telemetry Sync
   ========================================================================== */
function initOperationalTelemetry() {
    const timeElements = document.querySelectorAll('.operational-tag-item');
    if (!timeElements.length) return;

    function updateLiveTelemetry() {
        const now = new Date();
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        
        timeElements.forEach(el => {
            if (el.textContent.includes('Last updated') || el.textContent.includes('Database updated')) {
                el.textContent = `Last updated ${hours}:${minutes}`;
            }
        });
    }

    // Refresh every 30 seconds
    setInterval(updateLiveTelemetry, 30000);
}
