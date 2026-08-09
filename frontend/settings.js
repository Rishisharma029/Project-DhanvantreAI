/**
 * AURAMED AI — APPLICATION SETTINGS CONTROLLER
 */

const API_BASE = '/api/v1';

document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    initDarkModeSwitch();
    initLanguageSelect();
    initNotificationToggles();
    initExportData();
    initDeleteAccountModal();
});

/* 1. Theme Toggle & Dark Mode Switch */
function initThemeToggle() {
    const themeBtn = document.getElementById('themeToggleBtn');
    const themeIcon = document.getElementById('themeIcon');
    const htmlEl = document.documentElement;

    const savedTheme = localStorage.getItem('auramed_theme') || 'dark';
    htmlEl.setAttribute('data-theme', savedTheme);
    if (themeIcon) themeIcon.className = savedTheme === 'light' ? 'fa-solid fa-sun' : 'fa-solid fa-moon';
}

function initDarkModeSwitch() {
    const darkSwitch = document.getElementById('darkModeToggle');
    const themeIcon = document.getElementById('themeIcon');
    const htmlEl = document.documentElement;

    const currentTheme = htmlEl.getAttribute('data-theme') || 'dark';
    if (darkSwitch) darkSwitch.checked = currentTheme === 'dark';

    if (darkSwitch) {
        darkSwitch.addEventListener('change', (e) => {
            const newTheme = e.target.checked ? 'dark' : 'light';
            htmlEl.setAttribute('data-theme', newTheme);
            localStorage.setItem('auramed_theme', newTheme);
            if (themeIcon) themeIcon.className = newTheme === 'light' ? 'fa-solid fa-sun' : 'fa-solid fa-moon';
            showToast(`Switched to ${newTheme.toUpperCase()} theme mode`);
        });
    }
}

/* 2. Language & Regional Settings */
function initLanguageSelect() {
    const langSelect = document.getElementById('languageSelect');
    const unitsSelect = document.getElementById('unitsSelect');

    const savedLang = localStorage.getItem('auramed_lang') || 'en';
    if (langSelect) langSelect.value = savedLang;

    if (langSelect) {
        langSelect.addEventListener('change', (e) => {
            localStorage.setItem('auramed_lang', e.target.value);
            showToast(`Language preference updated to ${e.target.options[e.target.selectedIndex].text}`);
        });
    }

    if (unitsSelect) {
        unitsSelect.addEventListener('change', (e) => {
            showToast(`Measurement units set to ${e.target.options[e.target.selectedIndex].text}`);
        });
    }
}

/* 3. Notification Toggles */
function initNotificationToggles() {
    const emailToggle = document.getElementById('emailNotifToggle');
    const medToggle = document.getElementById('medRemindersToggle');
    const secToggle = document.getElementById('secAlertsToggle');

    const bindToggle = (el, name) => {
        if (el) {
            el.addEventListener('change', (e) => {
                showToast(`${name} ${e.target.checked ? 'ENABLED' : 'DISABLED'}`);
            });
        }
    };

    bindToggle(emailToggle, 'Email Diagnostic Reports');
    bindToggle(medToggle, 'Medication Intake Reminders');
    bindToggle(secToggle, 'Security Alerts');
}

/* 4. Export Patient Data (JSON Blob Download) */
function initExportData() {
    const exportBtn = document.getElementById('exportDataBtn');
    if (exportBtn) {
        exportBtn.addEventListener('click', () => {
            const patientData = {
                export_date: new Date().toISOString(),
                patient: {
                    name: 'Rishi Sharma',
                    id: '#PAT-2026-9941',
                    age: 34,
                    weight_kg: 72.5,
                    blood_type: 'O+'
                },
                allergies: ['Penicillin', 'Sulfonamides'],
                chronic_diseases: ['Hypertension'],
                active_medications: ['Metformin 500mg', 'Amlodipine 5mg'],
                history_count: 3
            };

            const jsonStr = JSON.stringify(patientData, null, 2);
            const blob = new Blob([jsonStr], { type: 'application/json' });
            const url = URL.createObjectURL(blob);

            const a = document.createElement('a');
            a.href = url;
            a.download = `AuraMed_PatientData_Export_${Date.now()}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);

            showToast('Patient data successfully exported as JSON!');
        });
    }
}

/* 5. Delete Account Modal */
function initDeleteAccountModal() {
    const deleteBtn = document.getElementById('deleteAccountBtn');
    const modal = document.getElementById('deleteModal');
    const closeBtn = document.getElementById('closeDeleteModalBtn');
    const confirmBtn = document.getElementById('confirmDeleteBtn');

    if (deleteBtn) deleteBtn.addEventListener('click', () => modal.classList.remove('hidden'));
    if (closeBtn) closeBtn.addEventListener('click', () => modal.classList.add('hidden'));

    if (confirmBtn) {
        confirmBtn.addEventListener('click', () => {
            modal.classList.add('hidden');
            showToast('Account purging requested. Logging out...');
            setTimeout(() => {
                window.location.href = 'auth.html#login';
            }, 1500);
        });
    }
}

function showToast(msg) {
    const existing = document.querySelector('.toast-banner');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = 'toast-banner';
    toast.innerHTML = `<i class="fa-solid fa-circle-check"></i> ${escapeHtml(msg)}`;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 3000);
}

function escapeHtml(str) {
    return String(str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
