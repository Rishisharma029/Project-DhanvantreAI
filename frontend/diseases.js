/**
 * AURAMED AI — DISEASE EXPLORER CONTROLLER
 */

const API_BASE = '/api/v1';

document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    initSearchInput();
    initQuickPills();
    initIndexSidebar();
    initTabSwitcher();
    loadDisease360('Fungal infection');
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

/* 2. Search Input */
function initSearchInput() {
    const searchInput = document.getElementById('diseaseSearchInput');
    let timer = null;

    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            clearTimeout(timer);
            timer = setTimeout(() => {
                const query = e.target.value.trim();
                if (query) loadDisease360(query);
            }, 300);
        });
    }
}

/* 3. Quick Pills */
function initQuickPills() {
    document.querySelectorAll('.disease-quick-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const dis = btn.getAttribute('data-dis');
            document.getElementById('diseaseSearchInput').value = dis;
            loadDisease360(dis);
        });
    });
}

/* 4. Index Sidebar Selector */
function initIndexSidebar() {
    document.querySelectorAll('.index-item').forEach(item => {
        item.addEventListener('click', () => {
            document.querySelectorAll('.index-item').forEach(i => i.classList.remove('active'));
            item.classList.add('active');

            const dis = item.getAttribute('data-dis');
            loadDisease360(dis);
        });
    });
}

/* 5. 7 Section Tab Switcher */
function initTabSwitcher() {
    const tabBtns = document.querySelectorAll('.disease-tab-btn');
    const panels = document.querySelectorAll('.disease-panel');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            panels.forEach(p => p.classList.remove('active'));

            btn.classList.add('active');
            const tabName = btn.getAttribute('data-tab');
            const targetId = `disTab${tabName.charAt(0).toUpperCase() + tabName.slice(1)}`;
            const targetPanel = document.getElementById(targetId);
            if (targetPanel) targetPanel.classList.add('active');
        });
    });
}

/* 6. Fetch & Load Disease 360 Profile */
async function loadDisease360(diseaseName) {
    try {
        const res = await fetch(`${API_BASE}/knowledge/disease/${encodeURIComponent(diseaseName)}`);
        if (res.ok) {
            const data = await res.json();
            renderDisease360(data);
        } else {
            renderFallbackDisease360(diseaseName);
        }
    } catch (e) {
        console.warn('Disease 360 fetch failed:', e);
        renderFallbackDisease360(diseaseName);
    }
}

function renderDisease360(data) {
    document.getElementById('disProfileTitle').innerText = data.disease_name || 'Disease Profile';
    document.getElementById('disProfileSub').innerText = `ICD-11 Code: ${data.icd_code || '1F00'} • Severity: ${data.severity || 'Moderate'}`;

    if (data.description) {
        document.getElementById('textDescription').innerText = data.description;
    }

    if (data.symptoms && data.symptoms.length > 0) {
        document.getElementById('listSymptoms').innerHTML = data.symptoms.map(s => `
            <li><strong>${escapeHtml(s.name || s)}:</strong> Presenting diagnostic indicator</li>
        `).join('');
    }

    if (data.causes) {
        document.getElementById('textCauses').innerText = data.causes;
    }

    if (data.treatments && data.treatments.length > 0) {
        document.getElementById('listTreatments').innerHTML = data.treatments.map(t => `
            <li>${escapeHtml(t.name || t)}</li>
        `).join('');
    }

    if (data.diets && data.diets.length > 0) {
        const rec = data.diets.filter(d => !d.is_avoid);
        const avoid = data.diets.filter(d => d.is_avoid);

        if (rec.length > 0) {
            document.getElementById('listDietRecommended').innerHTML = rec.map(d => `<li>${escapeHtml(d.diet_name || d)}</li>`).join('');
        }
        if (avoid.length > 0) {
            document.getElementById('listDietAvoid').innerHTML = avoid.map(d => `<li>${escapeHtml(d.diet_name || d)}</li>`).join('');
        }
    }

    if (data.workouts && data.workouts.length > 0) {
        document.getElementById('listExercise').innerHTML = data.workouts.map(w => `
            <li><strong>${escapeHtml(w.workout_name || w)}:</strong> ${escapeHtml(w.frequency || 'Light daily exertion')}</li>
        `).join('');
    }

    if (data.precautions && data.precautions.length > 0) {
        document.getElementById('listPrecautions').innerHTML = data.precautions.map(p => `
            <li>${escapeHtml(p.precaution || p)}</li>
        `).join('');
    }
}

function renderFallbackDisease360(diseaseName) {
    renderDisease360({
        disease_name: diseaseName,
        icd_code: '1A00',
        severity: 'Moderate',
        description: `${diseaseName} is a clinical condition involving localized or systemic physiological distress. Proper medical diagnosis and treatment protocols are required.`,
        symptoms: ['Localized pain / discomfort', 'Systemic malaise', 'Inflammation'],
        causes: `Etiology related to physiological stress, environmental vectors, or metabolic dysregulation.`,
        treatments: ['Symptomatic relief therapy', 'Targeted prescription regimen', 'Hydration and rest'],
        diets: [
            { diet_name: 'Nutrient-rich vegetables & fruits', is_avoid: false },
            { diet_name: 'Adequate hydration (2-3L water)', is_avoid: false },
            { diet_name: 'Refined sugars & processed foods', is_avoid: true }
        ],
        workouts: [
            { workout_name: 'Light walking (20-30 mins)', frequency: 'Daily' },
            { workout_name: 'Stretching & flexibility exercises', frequency: 'Daily' }
        ],
        precautions: [
            'Monitor body temperature and vital signs daily',
            'Avoid contact with known environmental allergens',
            'Seek immediate medical care if severe symptoms develop'
        ]
    });
}

function escapeHtml(str) {
    return String(str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
