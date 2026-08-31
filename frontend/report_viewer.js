/**
 * AURAMED AI — MEDICAL REPORT VIEWER CONTROLLER
 */

const API_BASE = '/api/v1';

document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    initViewToggle();
    initReportIndex();
    initDownloadBtn();
    initShareModal();
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

/* 2. HTML vs PDF View Toggle */
function initViewToggle() {
    const btnHtml = document.getElementById('viewHtmlBtn');
    const btnPdf = document.getElementById('viewPdfBtn');
    const htmlSheet = document.getElementById('htmlReportSheet');
    const pdfCanvas = document.getElementById('pdfPreviewCanvas');

    btnHtml.addEventListener('click', () => {
        btnHtml.classList.add('active');
        btnPdf.classList.remove('active');

        htmlSheet.classList.remove('hidden');
        pdfCanvas.classList.add('hidden');
    });

    btnPdf.addEventListener('click', () => {
        btnPdf.classList.add('active');
        btnHtml.classList.remove('active');

        pdfCanvas.classList.remove('hidden');
        htmlSheet.classList.add('hidden');
    });
}

/* 3. Report Sidebar Index */
function initReportIndex() {
    document.querySelectorAll('#reportIndexList .index-item').forEach(item => {
        item.addEventListener('click', () => {
            document.querySelectorAll('#reportIndexList .index-item').forEach(i => i.classList.remove('active'));
            item.classList.add('active');

            const repId = item.getAttribute('data-rep');
            loadReport(repId);
        });
    });
}

function loadReport(repId) {
    if (repId === '102') {
        renderReportData({
            id: '#RPT-2026-8812',
            date: '28-JUL-2026',
            patient: 'Rishi Sharma',
            ageSex: '34 Yrs / Male',
            triage: 'GREEN_STABLE',
            triageColor: 'var(--accent-emerald)',
            bp: '122 / 80 mmHg',
            hr: '78 bpm',
            spo2: '98%',
            complaint: 'Patient presented with 3-day history of dry cough, low-grade fever, and mild right-sided thoracic pleuritic discomfort.',
            diagnoses: [
                'Community-Acquired Pneumonia — 89.1% Diagnostic Certainty',
                'Acute Bronchitis — 9.8% Secondary Match'
            ],
            meds: [
                'Amoxicillin + Clavulanate 625mg (BID for 7 days)',
                'Azithromycin 500mg (QD for 3 days)'
            ],
            doctor: 'Dr. S. Patel, MD (Pulmonology)'
        });
    } else if (repId === '103') {
        renderReportData({
            id: '#RPT-2026-7734',
            date: '15-JUL-2026',
            patient: 'Rishi Sharma',
            ageSex: '34 Yrs / Male',
            triage: 'GREEN_STABLE',
            triageColor: 'var(--accent-emerald)',
            bp: '118 / 76 mmHg',
            hr: '72 bpm',
            spo2: '99%',
            complaint: 'Routine 3-month follow-up evaluation for Type 2 Diabetes Mellitus glycemic control.',
            diagnoses: [
                'Type 2 Diabetes Mellitus — 94.5% Diagnostic Certainty',
                'Impaired Fasting Glucose — 5.1% Secondary Match'
            ],
            meds: [
                'Metformin HCl 500 mg SR (QD with dinner)',
                'Teneligliptin 20 mg (QD in morning)'
            ],
            doctor: 'Dr. M. Roy, MD (Endocrinology)'
        });
    } else {
        renderReportData({
            id: '#RPT-2026-9041',
            date: '01-AUG-2026',
            patient: 'Rishi Sharma',
            ageSex: '34 Yrs / Male',
            triage: 'RED_EMERGENCY',
            triageColor: 'var(--accent-rose)',
            bp: '138 / 88 mmHg',
            hr: '94 bpm',
            spo2: '96%',
            complaint: 'Patient presented with acute retrosternal chest pain, onset 2 hours ago during exertion, accompanied by moderate dyspnea and diaphoresis.',
            diagnoses: [
                'Acute Coronary Syndrome (ACS) — Primary Consideration (Strong Evidence)',
                'Pleurisy / Pericarditis — Secondary Consideration (Limited Evidence)'
            ],
            meds: [
                'Aspirin 325 mg Chewable (STAT) — First-Line Antiplatelet',
                'Clopidogrel 75 mg Oral — Dual Antiplatelet Adjunct'
            ],
            doctor: 'Dr. A. Vance, MD (Cardiology)'
        });
    }
}

function renderReportData(data) {
    const sheet = document.getElementById('htmlReportSheet');
    sheet.querySelector('.report-sheet-header div:last-child').innerHTML = `
        <div>Report ID: ${data.id}</div>
        <div style="color: var(--text-dim);">Date: ${data.date}</div>
    `;

    sheet.querySelector('.report-meta-grid').innerHTML = `
        <div><strong>Patient:</strong> ${data.patient}</div>
        <div><strong>Age / Sex:</strong> ${data.ageSex}</div>
        <div><strong>Triage Level:</strong> <span style="color: ${data.triageColor}; font-weight: 700;">${data.triage}</span></div>
        <div><strong>Blood Pressure:</strong> ${data.bp}</div>
        <div><strong>Heart Rate:</strong> ${data.hr}</div>
        <div><strong>SpO2:</strong> ${data.spo2}</div>
    `;

    const sections = sheet.querySelectorAll('div[style*="margin-bottom: 24px"]');
    sections[0].querySelector('p').innerText = data.complaint;
    sections[1].querySelector('ul').innerHTML = data.diagnoses.map(d => `<li>${d}</li>`).join('');
    sections[2].querySelector('ul').innerHTML = data.meds.map(m => `<li>${m}</li>`).join('');

    sheet.querySelector('div[style*="border-top"]').querySelector('div:first-child').innerHTML = `Physician Signature: <em>${data.doctor}</em>`;
}

/* 4. Download Trigger */
function initDownloadBtn() {
    const dBtn = document.getElementById('downloadReportBtn');
    const pdfBtn = document.getElementById('downloadPdfCanvasBtn');

    const downloadAction = () => {
        const activeSheet = document.getElementById('htmlReportSheet');
        const textContent = activeSheet.innerText;
        const blob = new Blob([textContent], { type: 'application/pdf' });
        const url = URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = url;
        a.download = `AuraMed_Clinical_Report_${Date.now()}.pdf`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };

    if (dBtn) dBtn.addEventListener('click', downloadAction);
    if (pdfBtn) pdfBtn.addEventListener('click', downloadAction);
}

/* 5. Secure Share Modal */
function initShareModal() {
    const shareBtn = document.getElementById('shareReportBtn');
    const modal = document.getElementById('shareModal');
    const closeBtn = document.getElementById('closeShareModalBtn');
    const copyBtn = document.getElementById('copyShareLinkBtn');
    const input = document.getElementById('shareUrlInput');

    if (shareBtn) shareBtn.addEventListener('click', () => modal.classList.remove('hidden'));
    if (closeBtn) closeBtn.addEventListener('click', () => modal.classList.add('hidden'));

    if (copyBtn) {
        copyBtn.addEventListener('click', () => {
            navigator.clipboard.writeText(input.value);
            copyBtn.innerHTML = `<i class="fa-solid fa-check"></i> Copied!`;
            setTimeout(() => {
                copyBtn.innerHTML = `<i class="fa-solid fa-copy"></i> Copy`;
            }, 2000);
        });
    }
}
