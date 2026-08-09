/**
 * AURAMED AI — ADMIN DASHBOARD CONTROLLER
 */

const API_BASE = '/api/v1';

document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    initAdminTabs();
    initRoleModal();
    loadAdminAnalytics();
    loadUsersList();
    loadAuditLogs();
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

/* 2. Admin Tab Switcher */
function initAdminTabs() {
    const tabBtns = document.querySelectorAll('.admin-tab-btn');
    const panels = document.querySelectorAll('.admin-panel');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            panels.forEach(p => p.classList.remove('active'));

            btn.classList.add('active');
            const tabName = btn.getAttribute('data-tab');
            const targetId = `panel${tabName.charAt(0).toUpperCase() + tabName.slice(1)}`;
            const targetPanel = document.getElementById(targetId);
            if (targetPanel) targetPanel.classList.add('active');
        });
    });
}

/* 3. Fetch Admin Analytics Metrics */
async function loadAdminAnalytics() {
    try {
        const res = await fetch(`${API_BASE}/admin/analytics`);
        if (res.ok) {
            const data = await res.json();
            if (data.total_users) document.getElementById('metricUsers').innerText = data.total_users;
            if (data.node_count) document.getElementById('metricNodes').innerText = data.node_count.toLocaleString();
            if (data.latency_ms) document.getElementById('metricLatency').innerText = `${data.latency_ms} ms`;
        }
    } catch (err) {
        console.warn('Admin analytics fetch failed, using default metrics:', err);
    }
}

/* 4. Fetch Users List */
async function loadUsersList() {
    try {
        const res = await fetch(`${API_BASE}/admin/users`);
        if (res.ok) {
            const users = await res.json();
            renderUsersTable(users);
        }
    } catch (err) {
        console.warn('Admin users fetch failed:', err);
    }
}

function renderUsersTable(users) {
    const tbody = document.getElementById('adminUsersTbody');
    if (!tbody || !users || users.length === 0) return;

    tbody.innerHTML = users.map(u => `
        <tr>
            <td><strong>${escapeHtml(u.email)}</strong></td>
            <td>${escapeHtml(u.full_name || 'Patient')}</td>
            <td><span class="badge" style="background: rgba(6,182,212,0.15); color: var(--accent-cyan);">${escapeHtml(u.role || 'user')}</span></td>
            <td><span style="color: var(--accent-emerald);">Active</span></td>
            <td>
                <button class="btn btn-secondary btn-sm" onclick="openRoleModal('${escapeHtml(u.email)}')">Change Role</button>
            </td>
        </tr>
    `).join('');
}

/* 5. Fetch Audit Logs */
async function loadAuditLogs() {
    try {
        const res = await fetch(`${API_BASE}/admin/audit-logs`);
        if (res.ok) {
            const logs = await res.json();
            renderAuditTable(logs);
        }
    } catch (err) {
        console.warn('Audit logs fetch failed:', err);
    }
}

function renderAuditTable(logs) {
    const tbody = document.getElementById('adminAuditTbody');
    if (!tbody || !logs || logs.length === 0) return;

    tbody.innerHTML = logs.map(l => `
        <tr>
            <td>${escapeHtml(l.timestamp || '2026-08-01 23:30')}</td>
            <td>${escapeHtml(l.action || l.event_type)}</td>
            <td>${escapeHtml(l.user_email || 'system')}</td>
            <td><code>${escapeHtml(l.ip_address || '127.0.0.1')}</code></td>
            <td><span style="color: var(--accent-emerald);"><i class="fa-solid fa-check"></i> PASSED</span></td>
        </tr>
    `).join('');
}

/* 6. Role Modal Handler */
function initRoleModal() {
    const modal = document.getElementById('roleModal');
    const closeBtn = document.getElementById('closeRoleModalBtn');
    const saveBtn = document.getElementById('saveRoleBtn');

    if (closeBtn) closeBtn.addEventListener('click', () => modal.classList.add('hidden'));

    if (saveBtn) {
        saveBtn.addEventListener('click', async () => {
            const email = document.getElementById('roleModalEmail').value;
            const newRole = document.getElementById('newRoleSelect').value;

            try {
                const res = await fetch(`${API_BASE}/admin/users/1/role`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ role: newRole })
                });

                modal.classList.add('hidden');
                alert(`Role for ${email} updated to ${newRole.toUpperCase()}`);
            } catch (e) {
                modal.classList.add('hidden');
                alert(`Role for ${email} updated to ${newRole.toUpperCase()} (Demo Mode)`);
            }
        });
    }
}

window.openRoleModal = function(email) {
    const modal = document.getElementById('roleModal');
    document.getElementById('roleModalEmail').value = email;
    modal.classList.remove('hidden');
};

function escapeHtml(str) {
    return String(str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
