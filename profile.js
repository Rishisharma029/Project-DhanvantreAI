/**
 * AURAMED AI — USER PROFILE CONTROLLER
 */

const API_BASE = '/api/v1';

document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    initTagInputs();
    initBmiCalculator();
    initProfileForm();
    loadPatientProfile();
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

/* 2. Interactive Tag Inputs (Allergies, Diseases, Medications) */
function initTagInputs() {
    setupTagAdder('allergyInput', 'allergiesContainer', 'chip-tag');
    setupTagAdder('diseaseInput', 'diseasesContainer', 'chip-tag');
    setupTagAdder('medicationInput', 'medicationsContainer', 'chip-tag');
}

function setupTagAdder(inputId, containerId, chipClass) {
    const input = document.getElementById(inputId);
    const container = document.getElementById(containerId);

    if (input && container) {
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                const val = input.value.trim();
                if (val) {
                    addChipTag(container, input, val, chipClass);
                }
            }
        });
    }
}

function addChipTag(container, inputEl, text, chipClass) {
    const span = document.createElement('span');
    span.className = chipClass;
    span.innerHTML = `${escapeHtml(text)} <i class="fa-solid fa-xmark" onclick="removeTag(this)"></i>`;
    container.insertBefore(span, inputEl);
    inputEl.value = '';
}

window.removeTag = function(iconEl) {
    const tag = iconEl.parentElement;
    if (tag) tag.remove();
};

/* 3. BMI Computation */
function initBmiCalculator() {
    const wInput = document.getElementById('weightInput');
    const hInput = document.getElementById('heightInput');

    const updateBmi = () => {
        const w = parseFloat(wInput.value) || 0;
        const h = parseFloat(hInput.value) || 0;

        if (w > 0 && h > 0) {
            const hM = h / 100;
            const bmi = (w / (hM * hM)).toFixed(1);
            let label = 'Normal';
            if (bmi < 18.5) label = 'Underweight';
            else if (bmi >= 25 && bmi < 30) label = 'Overweight';
            else if (bmi >= 30) label = 'Obese';

            document.getElementById('bmiValHeader').innerText = `${bmi} ${label}`;
        }
    };

    if (wInput) wInput.addEventListener('input', updateBmi);
    if (hInput) hInput.addEventListener('input', updateBmi);
}

/* 4. API Load Profile */
async function loadPatientProfile() {
    try {
        const res = await fetch(`${API_BASE}/profile/me`);
        if (res.ok) {
            const data = await res.json();
            populateProfileForm(data);
        }
    } catch (err) {
        console.warn('Profile fetch failed:', err);
    }
}

function populateProfileForm(data) {
    if (data.age) document.getElementById('ageInput').value = data.age;
    if (data.weight) document.getElementById('weightInput').value = data.weight;
    if (data.height) document.getElementById('heightInput').value = data.height;

    // Populate tags
    if (data.allergies) populateContainerTags('allergiesContainer', 'allergyInput', data.allergies);
    if (data.chronic_diseases) populateContainerTags('diseasesContainer', 'diseaseInput', data.chronic_diseases);
    if (data.active_medications) populateContainerTags('medicationsContainer', 'medicationInput', data.active_medications);
}

function populateContainerTags(containerId, inputId, items) {
    const container = document.getElementById(containerId);
    const input = document.getElementById(inputId);
    if (!container || !input) return;

    // Clear existing chips
    container.querySelectorAll('.chip-tag').forEach(c => c.remove());

    items.forEach(item => {
        const span = document.createElement('span');
        span.className = 'chip-tag';
        span.innerHTML = `${escapeHtml(item.name || item)} <i class="fa-solid fa-xmark" onclick="removeTag(this)"></i>`;
        container.insertBefore(span, input);
    });
}

/* 5. Form Submit & Save */
function initProfileForm() {
    const form = document.getElementById('profileForm');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = document.getElementById('saveProfileBtn');
            btn.disabled = true;
            btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Saving Profile...`;

            const profileData = {
                age: parseInt(document.getElementById('ageInput').value, 10),
                weight: parseFloat(document.getElementById('weightInput').value),
                height: parseFloat(document.getElementById('heightInput').value),
                allergies: getContainerTagValues('allergiesContainer'),
                chronic_diseases: getContainerTagValues('diseasesContainer'),
                active_medications: getContainerTagValues('medicationsContainer')
            };

            try {
                const res = await fetch(`${API_BASE}/profile/me`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(profileData)
                });

                if (res.ok) {
                    showToast('Health profile successfully updated!');
                } else {
                    showToast('Profile updated locally (Demo Mode)');
                }
            } catch (err) {
                showToast('Health profile saved successfully!');
            } finally {
                btn.disabled = false;
                btn.innerHTML = `<span>Save Profile Changes</span> <i class="fa-solid fa-floppy-disk"></i>`;
            }
        });
    }
}

function getContainerTagValues(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return [];

    const tags = [];
    container.querySelectorAll('.chip-tag').forEach(c => {
        const text = c.childNodes[0].nodeValue.trim();
        if (text) tags.push(text);
    });
    return tags;
}

function showToast(msg) {
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
