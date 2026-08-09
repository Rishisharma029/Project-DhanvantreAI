/**
 * AURAMED AI — RECOMMENDATION RESULTS CONTROLLER
 */

const API_BASE = '/api/v1';

document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    initScenarios();
    loadScenario('acs');
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

/* 2. Quick Scenario Switcher */
function initScenarios() {
    document.querySelectorAll('.scenario-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.scenario-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const scen = btn.getAttribute('data-scen');
            loadScenario(scen);
        });
    });
}

function loadScenario(scen) {
    if (scen === 'fungal') {
        renderCardData({
            conditions: [
                { name: 'Fungal Infection (Tinea Corporis)', match: 92.4, color: 'var(--accent-cyan)' },
                { name: 'Contact Dermatitis', match: 7.2, color: 'var(--accent-amber)' }
            ],
            confidence: '94.8%',
            confDesc: 'High precision match against dermatological fungal ontology.',
            medicines: [
                { name: 'Clotrimazole 1% Cream', desc: 'Topical Antifungal • Apply BID for 14 days', price: '₹42.00' },
                { name: 'Fluconazole 150 mg', desc: 'Oral Systemic Antifungal • Single Dose', price: '₹28.50' }
            ],
            safetyScore: '99 / 100',
            safetyDesc: 'Zero drug-drug contraindications. Topically safe profile.',
            precautions: [
                'Keep affected skin dry and well-ventilated',
                'Avoid sharing personal towels or garments',
                'Shower immediately after physical workout sessions'
            ],
            docRec: 'Prescribe Clotrimazole 1% cream BID for 2 weeks. Advise patient to maintain dry skin fold hygiene and return if pruritus persists.'
        });
    } else if (scen === 'pneumonia') {
        renderCardData({
            conditions: [
                { name: 'Community-Acquired Pneumonia', match: 89.1, color: 'var(--accent-rose)' },
                { name: 'Acute Bronchitis', match: 9.8, color: 'var(--accent-amber)' }
            ],
            confidence: '95.2%',
            confDesc: 'High certainty match from fever, productive cough, and infiltrate signs.',
            medicines: [
                { name: 'Amoxicillin + Clavulanate 625mg', desc: 'Broad-Spectrum Antibiotic • BID for 7 days', price: '₹204.00' },
                { name: 'Azithromycin 500 mg', desc: 'Macrolide Antibiotic Adjunct • QD for 3 days', price: '₹115.00' }
            ],
            safetyScore: '96 / 100',
            safetyDesc: 'No hepatic impairment warnings. Normal renal clearance.',
            precautions: [
                'Monitor body temperature and SpO2 levels every 4 hours',
                'Complete full antibiotic course even if feeling better',
                'Seek emergency care if severe shortness of breath develops'
            ],
            docRec: 'Order STAT Chest X-Ray (PA View) and Sputum Culture. Initiate empiric oral Amoxicillin-Clavulanate 625mg BID and monitor SpO2.'
        });
    } else if (scen === 'diabetes') {
        renderCardData({
            conditions: [
                { name: 'Type 2 Diabetes Mellitus', match: 94.5, color: 'var(--accent-cyan)' },
                { name: 'Impaired Fasting Glucose', match: 5.1, color: 'var(--accent-amber)' }
            ],
            confidence: '97.6%',
            confDesc: 'Exceptional diagnostic precision based on glycemic triad.',
            medicines: [
                { name: 'Metformin HCl 500 mg SR', desc: 'Biguanide Anti-hyperglycemic • QD with meals', price: '₹48.00' },
                { name: 'Teneligliptin 20 mg', desc: 'DPP-4 Inhibitor • QD in morning', price: '₹130.00' }
            ],
            safetyScore: '97 / 100',
            safetyDesc: 'eGFR > 60 mL/min confirmed. Low risk of hypoglycemia.',
            precautions: [
                'Adhere to low-glycemic high-fiber dietary plan',
                'Engage in 30 minutes of daily moderate walking',
                'Log blood glucose readings before meals'
            ],
            docRec: 'Order Fasting Blood Glucose, HbA1c, and Serum Creatinine. Start Metformin SR 500mg once daily with dinner.'
        });
    } else {
        // ACS Default
        renderCardData({
            conditions: [
                { name: 'Acute Coronary Syndrome (ACS)', match: 86.4, color: 'var(--accent-rose)' },
                { name: 'Pleurisy / Pericarditis', match: 11.2, color: 'var(--accent-amber)' }
            ],
            confidence: '96.4%',
            confDesc: 'Evaluated against 250,000 biomedical graph nodes. Sensitivity score 0.94, diagnostic precision 0.96.',
            medicines: [
                { name: 'Aspirin 325 mg (Chewable)', desc: 'First-Line Antiplatelet Therapy • STAT Administration', price: '₹18.50' },
                { name: 'Clopidogrel 75 mg', desc: 'Dual Antiplatelet Adjunct • Oral Tablet', price: '₹64.00' }
            ],
            safetyScore: '98 / 100',
            safetyDesc: 'Renal & hepatic clearance parameters normal. Allergy clearance verified against patient profile.',
            precautions: [
                'Do not delay emergency transport if chest discomfort persists',
                'Avoid physical exertion or strenuous exercise',
                'Monitor oxygen saturation (keep SpO2 > 94%)'
            ],
            docRec: 'Immediate 12-lead ECG, STAT Cardiac Troponin I assays, supplemental oxygen if SpO2 < 94%, and transfer to CCU.'
        });
    }
}

function renderCardData(data) {
    // 1. Conditions
    document.getElementById('condsList').innerHTML = data.conditions.map(c => `
        <div class="cond-bar-row">
            <div class="cond-bar-meta">
                <span>${escapeHtml(c.name)}</span>
                <span style="color: ${c.color};">${c.match}% Match</span>
            </div>
            <div class="strength-bar-bg">
                <div class="strength-bar-fill" style="width: ${c.match}%; background: ${c.color};"></div>
            </div>
        </div>
    `).join('');

    // 2. Confidence
    document.getElementById('confValText').innerText = data.confidence;
    document.getElementById('confDescText').innerText = data.confDesc;

    // 3. Medicines Reviewed
    document.getElementById('medsList').innerHTML = data.medicines.map(m => `
        <div class="med-item-row">
            <div>
                <strong>${escapeHtml(m.name)}</strong>
                <div style="font-size: 0.8rem; color: var(--text-muted);">${escapeHtml(m.desc)}</div>
            </div>
            <div style="font-weight: 800; color: var(--accent-emerald); font-family: 'JetBrains Mono', monospace;">${escapeHtml(m.price)}</div>
        </div>
    `).join('');

    // 4. Safety Score
    document.getElementById('safetyScoreVal').innerText = data.safetyScore;
    document.getElementById('safetyDescText').innerText = data.safetyDesc;

    // 5. Precautions
    document.getElementById('precautionsList').innerHTML = data.precautions.map(p => `
        <li>${escapeHtml(p)}</li>
    `).join('');

    // 6. Doctor Recommendation
    document.getElementById('docRecText').innerHTML = `
        <strong style="color: var(--accent-cyan); font-size: 0.95rem; display: block; margin-bottom: 6px;">STAT Clinical Workup:</strong>
        ${escapeHtml(data.docRec)}
    `;
}

function escapeHtml(str) {
    return String(str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
