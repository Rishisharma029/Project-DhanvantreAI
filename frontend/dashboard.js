/**
 * AURAMED AI — DASHBOARD CONTROLLER
 */

const API_BASE = '/api/v1';

document.addEventListener('DOMContentLoaded', async () => {
    initThemeToggle();
    initNotificationsDrawer();
    initModals();
    initLogout();
    
    // Auth Check & Load Dashboard Data
    const token = localStorage.getItem('auramed_access_token');
    if (!token) {
        // Render demo state if unauthenticated or redirect to login
        console.warn('No access token found. Operating in demo mode.');
        setupDemoUser();
    } else {
        await loadUserProfile(token);
        await loadReports(token);
        await loadMedicines(token);
        await loadNotifications(token);
    }

    initRecentSearches();
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

/* 2. User Profile Loading */
async function loadUserProfile(token) {
    try {
        const res = await fetch(`${API_BASE}/auth/me`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!res.ok) throw new Error('Token expired');

        const user = await res.json();
        const initials = user.full_name ? user.full_name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2) : 'US';

        document.getElementById('sidebarAvatar').innerText = initials;
        document.getElementById('sidebarUserName').innerText = user.full_name || user.email;
        document.getElementById('sidebarUserRole').innerText = user.role || 'Patient';
        document.getElementById('welcomeGreeting').innerText = `Welcome Back, ${user.full_name || 'User'}`;
    } catch (err) {
        console.warn('User auth check failed:', err);
        setupDemoUser();
    }
}

function setupDemoUser() {
    document.getElementById('sidebarAvatar').innerText = 'SJ';
    document.getElementById('sidebarUserName').innerText = 'Dr. Sarah Jenkins';
    document.getElementById('sidebarUserRole').innerText = 'Clinician';
    document.getElementById('welcomeGreeting').innerText = 'Welcome Back, Dr. Sarah';
}

/* 3. Reports Service */
async function loadReports(token) {
    try {
        const res = await fetch(`${API_BASE}/history/reports`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!res.ok) return;

        const reports = await res.json();
        const tableBody = document.getElementById('reportsTableBody');

        if (reports && reports.length > 0) {
            document.getElementById('valTotalReports').innerText = reports.length;
            tableBody.innerHTML = reports.map(r => `
                <tr>
                    <td><strong>${escapeHtml(r.report_title)}</strong></td>
                    <td>${escapeHtml(r.category || 'Diagnostic')}</td>
                    <td>${r.created_at ? r.created_at.slice(0, 10) : '2026-08-01'}</td>
                    <td><span class="status-pill status-ready"><i class="fa-solid fa-circle-check"></i> Ready</span></td>
                    <td>${escapeHtml(r.summary_text || 'No findings entered')}</td>
                </tr>
            `).join('');
        }
    } catch (err) {
        console.error('Failed to load reports:', err);
    }
}

/* 4. Medicines Service */
async function loadMedicines(token) {
    try {
        const res = await fetch(`${API_BASE}/history/medicines`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!res.ok) return;

        const meds = await res.json();
        const grid = document.getElementById('medsGrid');

        if (meds && meds.length > 0) {
            document.getElementById('valActiveMeds').innerText = meds.length;
            grid.innerHTML = meds.map(m => `
                <div class="glass-card med-card">
                    <div class="med-header">
                        <div class="med-name">${escapeHtml(m.medicine_name)}</div>
                        <div class="med-dosage">${escapeHtml(m.dosage || 'Standard')}</div>
                    </div>
                    <div class="med-purpose">${escapeHtml(m.purpose || 'Prescribed therapy')}</div>
                    <div class="med-footer">
                        <span>Frequency: ${escapeHtml(m.frequency || 'Daily')}</span>
                        <span style="color: var(--accent-emerald);"><i class="fa-solid fa-check"></i> Refill Active</span>
                    </div>
                </div>
            `).join('');
        }
    } catch (err) {
        console.error('Failed to load medicines:', err);
    }
}

/* 5. Notifications Service */
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
            badge.innerText = notifs.length;
            list.innerHTML = notifs.map(n => `
                <div class="notif-item">
                    <div class="notif-icon"><i class="fa-solid fa-bell"></i></div>
                    <div>
                        <div class="notif-title">${escapeHtml(n.title || 'System Notification')}</div>
                        <div class="notif-body">${escapeHtml(n.body || n.message || '')}</div>
                        <div class="notif-time">${n.created_at ? n.created_at.slice(0, 16) : 'Just now'}</div>
                    </div>
                </div>
            `).join('');
        } else {
            badge.innerText = '0';
        }
    } catch (err) {
        console.error('Failed to load notifications:', err);
    }
}

/* 6. Notifications Slide-out Drawer */
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

/* 7. Modals (Log Report & Save Medicine) */
function initModals() {
    const token = localStorage.getItem('auramed_access_token');

    // Report Modal
    const reportModal = document.getElementById('reportModal');
    const openReportBtn = document.getElementById('openAddReportModalBtn');
    const closeReportBtn = document.getElementById('closeReportModalBtn');
    const addReportForm = document.getElementById('addReportForm');

    if (openReportBtn) openReportBtn.addEventListener('click', () => reportModal.classList.remove('hidden'));
    if (closeReportBtn) closeReportBtn.addEventListener('click', () => reportModal.classList.add('hidden'));

    if (addReportForm) {
        addReportForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const title = document.getElementById('reportTitleInput').value.trim();
            const category = document.getElementById('reportCategorySelect').value;
            const summary = document.getElementById('reportSummaryInput').value.trim();

            if (!title) return;

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
                    await loadReports(token);
                } catch (err) {
                    console.error('Failed to post report:', err);
                }
            } else {
                // Local UI append for demo
                const tableBody = document.getElementById('reportsTableBody');
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td><strong>${escapeHtml(title)}</strong></td>
                    <td>${escapeHtml(category)}</td>
                    <td>${new Date().toISOString().slice(0, 10)}</td>
                    <td><span class="status-pill status-ready"><i class="fa-solid fa-circle-check"></i> Ready</span></td>
                    <td>${escapeHtml(summary || 'User logged entry')}</td>
                `;
                tableBody.prepend(row);
                const currentVal = parseInt(document.getElementById('valTotalReports').innerText) || 0;
                document.getElementById('valTotalReports').innerText = currentVal + 1;
            }

            reportModal.classList.add('hidden');
            addReportForm.reset();
        });
    }

    // Medicine Modal
    const medModal = document.getElementById('medModal');
    const openMedBtn = document.getElementById('openAddMedModalBtn');
    const closeMedBtn = document.getElementById('closeMedModalBtn');
    const addMedForm = document.getElementById('addMedForm');

    if (openMedBtn) openMedBtn.addEventListener('click', () => medModal.classList.remove('hidden'));
    if (closeMedBtn) closeMedBtn.addEventListener('click', () => medModal.classList.add('hidden'));

    if (addMedForm) {
        addMedForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const name = document.getElementById('medNameInput').value.trim();
            const dosage = document.getElementById('medDosageInput').value.trim();
            const purpose = document.getElementById('medPurposeInput').value.trim();
            const freq = document.getElementById('medFrequencyInput').value.trim();

            if (!name || !dosage) return;

            if (token) {
                try {
                    await fetch(`${API_BASE}/history/medicines`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${token}`
                        },
                        body: JSON.stringify({
                            medicine_name: name,
                            dosage: dosage,
                            purpose: purpose,
                            frequency: freq
                        })
                    });
                    await loadMedicines(token);
                } catch (err) {
                    console.error('Failed to post medicine:', err);
                }
            } else {
                const grid = document.getElementById('medsGrid');
                const card = document.createElement('div');
                card.className = 'glass-card med-card';
                card.innerHTML = `
                    <div class="med-header">
                        <div class="med-name">${escapeHtml(name)}</div>
                        <div class="med-dosage">${escapeHtml(dosage)}</div>
                    </div>
                    <div class="med-purpose">${escapeHtml(purpose || 'Prescribed medication')}</div>
                    <div class="med-footer">
                        <span>Frequency: ${escapeHtml(freq || 'Daily')}</span>
                        <span style="color: var(--accent-emerald);"><i class="fa-solid fa-check"></i> Active</span>
                    </div>
                `;
                grid.prepend(card);
                const currentVal = parseInt(document.getElementById('valActiveMeds').innerText) || 0;
                document.getElementById('valActiveMeds').innerText = currentVal + 1;
            }

            medModal.classList.add('hidden');
            addMedForm.reset();
        });
    }
}

/* 8. Recent Searches Interaction */
function initRecentSearches() {
    const chips = document.querySelectorAll('.search-chip');
    chips.forEach(chip => {
        chip.addEventListener('click', () => {
            const query = chip.innerText.trim();
            window.location.href = `index.html#hero-demo`;
        });
    });
}

/* 9. Logout Handler */
function initLogout() {
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            localStorage.removeItem('auramed_access_token');
            localStorage.removeItem('auramed_refresh_token');
            window.location.href = 'auth.html#login';
        });
    }
}

/* Security Helper */
function escapeHtml(str) {
    return String(str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
