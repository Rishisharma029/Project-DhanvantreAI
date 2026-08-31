/**
 * DHANVANTRE CLINICAL INTELLIGENCE PLATFORM
 * Professional Medication Reference Notebook Controller
 */

const MONOGRAPHS = {
    metformin: {
        title: "METFORMIN",
        meta: "Biguanide • Rx information • ATC: A10BA02",
        indications: "Type 2 diabetes mellitus (first-line pharmacotherapy as monotherapy or in combination with other oral anti-hyperglycemic agents or insulin).",
        dosing: `
            <ul class="clinical-bullet-list">
                <li><strong>Immediate-Release (IR):</strong> Initial 500 mg PO BID or 850 mg PO QD with meals. Titrate by 500 mg weekly or 850 mg every 2 weeks as tolerated. Maintenance: 1,500 to 2,000 mg/day in divided doses. Maximum dose: 2,550 mg/day.</li>
                <li><strong>Extended-Release (XR):</strong> Initial 500 to 1,000 mg PO QD with evening meal. Titrate by 500 mg weekly to maximum 2,000 mg QD.</li>
            </ul>
        `,
        contraindications: `
            <ul class="clinical-bullet-list">
                <li>Severe renal impairment (eGFR &lt; 30 mL/min/1.73 m²).</li>
                <li>Acute or chronic metabolic acidosis, including diabetic ketoacidosis (DKA) with or without coma.</li>
                <li>Severe hepatic impairment or conditions associated with hypoxemia (e.g., acute heart failure, shock, acute myocardial infarction, severe sepsis).</li>
                <li>Known hypersensitivity to metformin hydrochloride.</li>
            </ul>
        `,
        renal: `
            <ul class="clinical-bullet-list">
                <li><strong>eGFR &ge; 60 mL/min/1.73 m²:</strong> No dosage adjustment required. Monitor renal function annually.</li>
                <li><strong>eGFR 45 to &lt; 60 mL/min/1.73 m²:</strong> Maximum recommended dose is 1,500 mg/day; monitor renal function every 3–6 months.</li>
                <li><strong>eGFR 30 to &lt; 45 mL/min/1.73 m²:</strong> Maximum dose 1,000 mg/day. Initiation of therapy is not recommended; assess risk/benefit if continuing.</li>
                <li><strong>eGFR &lt; 30 mL/min/1.73 m²:</strong> Contraindicated due to risk of metformin-associated lactic acidosis (MALA).</li>
            </ul>
        `,
        hepatic: "Avoid use in patients with hepatic impairment due to impaired lactate clearance and substantially elevated risk of lactic acidosis.",
        interactions: `
            <div style="font-weight: 700; color: var(--text-main); margin-bottom: 6px;">3 clinically relevant interactions</div>
            <ul class="clinical-bullet-list">
                <li><strong>Iodinated Contrast Agents:</strong> Withhold metformin prior to or at time of iodinated contrast imaging in patients with eGFR 30–60 mL/min; re-evaluate renal function 48 hours post-procedure before restarting.</li>
                <li><strong>Carbonic Anhydrase Inhibitors (Topiramate, Acetazolamide):</strong> Concomitant use may increase serum lactate and potentiate metabolic acidosis risk.</li>
                <li><strong>Cimetidine / OCT2 Inhibitors:</strong> Increases metformin plasma concentrations (AUC +50%) via competition for renal tubular excretion.</li>
            </ul>
        `
    },
    aspirin: {
        title: "ASPIRIN (ACETYLSALICYLIC ACID)",
        meta: "Salicylate • Antiplatelet / NSAID • ATC: B01AC06",
        indications: "Secondary prevention of cardiovascular events, Acute Coronary Syndrome (NSTEMI / STEMI), acute ischemic stroke or TIA, mild-to-moderate analgesia and antipyresis.",
        dosing: `
            <ul class="clinical-bullet-list">
                <li><strong>Acute Coronary Syndrome (Loading):</strong> 162 to 325 mg PO non-enteric coated, chewed immediately.</li>
                <li><strong>Chronic Secondary Prevention:</strong> 75 to 100 mg PO QD.</li>
                <li><strong>Acute Ischemic Stroke:</strong> 160 to 325 mg PO QD initiated within 24 to 48 hours of onset.</li>
            </ul>
        `,
        contraindications: `
            <ul class="clinical-bullet-list">
                <li>Active peptic ulcer disease or gastrointestinal bleeding.</li>
                <li>Aspirin-induced asthma or severe bronchospasm with NSAIDs.</li>
                <li>Bleeding diathesis (e.g., hemophilia, severe thrombocytopenia).</li>
                <li>Children and adolescents with viral illness (risk of Reye's syndrome).</li>
            </ul>
        `,
        renal: `
            <ul class="clinical-bullet-list">
                <li><strong>Mild to Moderate:</strong> Use with caution; monitor for acute renal decompensation.</li>
                <li><strong>Severe (eGFR &lt; 10 mL/min):</strong> Avoid use due to fluid retention and platelet dysfunction.</li>
            </ul>
        `,
        hepatic: "Avoid in severe hepatic failure due to impaired coagulation factor synthesis and heightened bleeding risk.",
        interactions: `
            <div style="font-weight: 700; color: var(--text-main); margin-bottom: 6px;">4 clinically relevant interactions</div>
            <ul class="clinical-bullet-list">
                <li><strong>Anticoagulants (Heparin, Warfarin, DOACs):</strong> Synergistic enhancement of major bleeding risk; co-prescribe only with strict indication.</li>
                <li><strong>NSAIDs (Ibuprofen, Naproxen):</strong> Competitive inhibition of aspirin's irreversible COX-1 platelet inhibition; administer aspirin &ge;30 min prior to NSAID.</li>
                <li><strong>Methotrexate:</strong> Decreases renal clearance of methotrexate, leading to elevated toxicity risk.</li>
            </ul>
        `
    },
    amlodipine: {
        title: "AMLODIPINE",
        meta: "Dihydropyridine Calcium Channel Blocker • ATC: C08CA01",
        indications: "Essential hypertension, chronic stable angina pectoris, vasospastic (Prinzmetal's) angina.",
        dosing: `
            <ul class="clinical-bullet-list">
                <li><strong>Hypertension:</strong> Initial 5 mg PO QD; may titrate to maximum 10 mg PO QD after 7 to 14 days.</li>
                <li><strong>Geriatric / Hepatic Start:</strong> 2.5 mg PO QD.</li>
            </ul>
        `,
        contraindications: `
            <ul class="clinical-bullet-list">
                <li>Severe hypotension (systolic BP &lt; 90 mmHg).</li>
                <li>Cardiogenic shock or severe aortic stenosis.</li>
                <li>Known hypersensitivity to amlodipine.</li>
            </ul>
        `,
        renal: "No dosage adjustment required in renal impairment. Not dialyzable.",
        hepatic: "Extensively metabolized by the liver. Initiate therapy at 2.5 mg QD and titrate slowly.",
        interactions: `
            <div style="font-weight: 700; color: var(--text-main); margin-bottom: 6px;">2 clinically relevant interactions</div>
            <ul class="clinical-bullet-list">
                <li><strong>Simvastatin:</strong> Amlodipine increases simvastatin exposure; limit simvastatin dose to 20 mg/day when co-administered.</li>
                <li><strong>CYP3A4 Inhibitors (Ketoconazole, Clarithromycin):</strong> Increases amlodipine serum concentrations.</li>
            </ul>
        `
    },
    clopidogrel: {
        title: "CLOPIDOGREL",
        meta: "Thienopyridine P2Y12 Platelet Inhibitor • ATC: B01AC04",
        indications: "Acute Coronary Syndrome (NSTEMI / STEMI), recent MI, recent ischemic stroke, established peripheral arterial disease.",
        dosing: `
            <ul class="clinical-bullet-list">
                <li><strong>ACS Loading:</strong> 300 to 600 mg PO STAT loading dose.</li>
                <li><strong>Maintenance:</strong> 75 mg PO QD in combination with aspirin (DAPT).</li>
            </ul>
        `,
        contraindications: `
            <ul class="clinical-bullet-list">
                <li>Active pathological bleeding (e.g., peptic ulcer or intracranial hemorrhage).</li>
                <li>Hypersensitivity to clopidogrel.</li>
            </ul>
        `,
        renal: "No dosage adjustment necessary in mild to moderate renal insufficiency. Experience is limited in severe renal impairment.",
        hepatic: "Avoid in severe hepatic impairment where bleeding diathesis is present.",
        interactions: `
            <div style="font-weight: 700; color: var(--text-main); margin-bottom: 6px;">3 clinically relevant interactions</div>
            <ul class="clinical-bullet-list">
                <li><strong>Omeprazole / Esomeprazole:</strong> Inhibits CYP2C19 bioactivation of clopidogrel; prefer pantoprazole if PPI is clinically indicated.</li>
                <li><strong>Oral Anticoagulants (DOACs / Warfarin):</strong> Substantially increases major bleeding risk.</li>
            </ul>
        `
    },
    atorvastatin: {
        title: "ATORVASTATIN",
        meta: "HMG-CoA Reductase Inhibitor • High-Intensity Statin • ATC: C10AA05",
        indications: "Primary and secondary prevention of atherosclerotic cardiovascular disease (ASCVD), hypercholesterolemia, mixed dyslipidemia.",
        dosing: `
            <ul class="clinical-bullet-list">
                <li><strong>High-Intensity (Post-ACS):</strong> 80 mg PO QD (or 40 mg PO QD if intolerant).</li>
                <li><strong>Moderate-Intensity:</strong> 10 to 20 mg PO QD.</li>
            </ul>
        `,
        contraindications: `
            <ul class="clinical-bullet-list">
                <li>Active liver disease or unexplained persistent elevations of serum transaminases (>3x ULN).</li>
                <li>Pregnancy and breastfeeding.</li>
            </ul>
        `,
        renal: "No dosage adjustment needed across any stage of renal impairment.",
        hepatic: "Contraindicated in active liver disease. Use caution in patients consuming substantial quantities of alcohol.",
        interactions: `
            <div style="font-weight: 700; color: var(--text-main); margin-bottom: 6px;">3 clinically relevant interactions</div>
            <ul class="clinical-bullet-list">
                <li><strong>Strong CYP3A4 Inhibitors (Clarithromycin, Itraconazole, Protease Inhibitors):</strong> Elevates atorvastatin plasma levels; titrate or temporarily withhold.</li>
                <li><strong>Cyclosporine / Gemfibrozil:</strong> Marked increase in myopathy and rhabdomyolysis risk.</li>
            </ul>
        `
    },
    augmentin: {
        title: "AMOXICILLIN / CLAVULANATE",
        meta: "Aminopenicillin + Beta-Lactamase Inhibitor • ATC: J01CR02",
        indications: "Community-acquired pneumonia, acute bacterial sinusitis, otitis media, skin and soft tissue infections, animal/human bites.",
        dosing: `
            <ul class="clinical-bullet-list">
                <li><strong>Standard Infection:</strong> 625 mg (500/125) PO TID or 1,000 mg (875/125) PO BID with start of meal.</li>
                <li><strong>Severe Respiratory Infection:</strong> 1,000 mg PO BID for 7 to 10 days.</li>
            </ul>
        `,
        contraindications: `
            <ul class="clinical-bullet-list">
                <li>History of severe immediate hypersensitivity (anaphylaxis) to beta-lactam antibacterials.</li>
                <li>Previous history of amoxicillin/clavulanate-associated cholestatic jaundice or hepatic dysfunction.</li>
            </ul>
        `,
        renal: `
            <ul class="clinical-bullet-list">
                <li><strong>eGFR 10 to 30 mL/min:</strong> Dose adjustment to 500/125 mg PO BID.</li>
                <li><strong>eGFR &lt; 10 mL/min:</strong> 500/125 mg PO QD.</li>
            </ul>
        `,
        hepatic: "Monitor hepatic function in prolonged treatment. Cholestatic jaundice risk is higher in elderly males.",
        interactions: `
            <div style="font-weight: 700; color: var(--text-main); margin-bottom: 6px;">2 clinically relevant interactions</div>
            <ul class="clinical-bullet-list">
                <li><strong>Allopurinol:</strong> Increases incidence of maculopapular rash.</li>
                <li><strong>Oral Anticoagulants (Warfarin):</strong> May prolong prothrombin time / INR; monitor closely.</li>
            </ul>
        `
    }
};

document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initIndexSelection();
    initSearch();
    initFilterTags();
});

function initTheme() {
    const themeBtn = document.getElementById('themeToggleBtn');
    const themeIcon = document.getElementById('themeIcon');
    const htmlEl = document.documentElement;

    const savedTheme = localStorage.getItem('dhanvantre_theme') || 'light';
    htmlEl.setAttribute('data-theme', savedTheme);
    if (themeIcon) themeIcon.className = savedTheme === 'dark' ? 'fa-solid fa-sun' : 'fa-solid fa-moon';

    if (themeBtn) {
        themeBtn.addEventListener('click', () => {
            const currentTheme = htmlEl.getAttribute('data-theme');
            const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
            htmlEl.setAttribute('data-theme', nextTheme);
            localStorage.setItem('dhanvantre_theme', nextTheme);
            if (themeIcon) themeIcon.className = nextTheme === 'dark' ? 'fa-solid fa-sun' : 'fa-solid fa-moon';
        });
    }
}

function initIndexSelection() {
    const items = document.querySelectorAll('.med-index-item');
    items.forEach(item => {
        item.addEventListener('click', () => {
            items.forEach(i => i.classList.remove('active'));
            item.classList.add('active');
            const medKey = item.getAttribute('data-med');
            loadMonograph(medKey);
        });
    });
}

function loadMonograph(key) {
    const data = MONOGRAPHS[key];
    if (!data) return;

    document.getElementById('monoDrugTitle').innerText = data.title;
    document.getElementById('monoDrugMeta').innerText = data.meta;
    document.getElementById('monoIndications').innerHTML = data.indications;
    document.getElementById('monoDosing').innerHTML = data.dosing;
    document.getElementById('monoContraindications').innerHTML = data.contraindications;
    document.getElementById('monoRenal').innerHTML = data.renal;
    document.getElementById('monoHepatic').innerHTML = data.hepatic;
    document.getElementById('monoInteractions').innerHTML = data.interactions;

    document.getElementById('medSearchInput').value = data.title.split(' ')[0];
}

function initSearch() {
    const searchInput = document.getElementById('medSearchInput');
    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.trim().toLowerCase();
        const items = document.querySelectorAll('.med-index-item');
        let matchedFirst = null;

        items.forEach(item => {
            const text = item.innerText.toLowerCase();
            if (text.includes(query)) {
                item.style.display = 'block';
                if (!matchedFirst) matchedFirst = item;
            } else {
                item.style.display = 'none';
            }
        });

        if (matchedFirst && query.length > 2) {
            items.forEach(i => i.classList.remove('active'));
            matchedFirst.classList.add('active');
            loadMonograph(matchedFirst.getAttribute('data-med'));
        }
    });
}

function initFilterTags() {
    const tags = document.querySelectorAll('.med-filter-tag');
    const sections = {
        class: document.getElementById('secIndications'),
        contraindications: document.getElementById('secContraindications'),
        interactions: document.getElementById('secInteractions'),
        renal: document.getElementById('secRenal'),
        hepatic: document.getElementById('secHepatic')
    };

    tags.forEach(tag => {
        tag.addEventListener('click', () => {
            tags.forEach(t => t.classList.remove('active'));
            tag.classList.add('active');
            const filter = tag.getAttribute('data-filter');

            if (filter === 'all') {
                Object.values(sections).forEach(sec => {
                    if (sec) sec.style.display = 'block';
                });
            } else {
                Object.keys(sections).forEach(key => {
                    if (sections[key]) {
                        sections[key].style.display = key === filter ? 'block' : 'none';
                    }
                });
            }
        });
    });
}
