/**
 * DHANVANTRE CLINICAL INTELLIGENCE PLATFORM
 * Clinical Knowledge Base Controller
 */

const DISEASE_KNOWLEDGE = {
    acs: {
        title: "Acute Coronary Syndrome",
        meta: "Cardiovascular Medicine • ICD-11: BA41 • Emergency Specialty Focus",
        overview: "Acute Coronary Syndrome (ACS) encompasses a spectrum of clinical conditions ranging from unstable angina (UA) to non-ST-segment elevation myocardial infarction (NSTEMI) and ST-segment elevation myocardial infarction (STEMI). It is almost universally caused by atherosclerotic plaque rupture or erosion, leading to platelet activation, thrombosis, and acute reduction of myocardial perfusion.",
        presentation: `
            <ul class="clinical-bullet-list">
                <li><strong>Retrosternal Chest Discomfort:</strong> Pressure, fullness, heaviness, or crushing pain lasting &gt;20 minutes, frequently radiating to left arm, neck, jaw, or epigastrium.</li>
                <li><strong>Associated Symptoms:</strong> Diaphoresis (cold sweats), dyspnea, nausea, lightheadedness, and profound fatigue.</li>
                <li><strong>Atypical Presentations:</strong> Commonly seen in elderly patients, females, and individuals with diabetes mellitus (presenting as isolated dyspnea, unexplained weakness, or delirium).</li>
            </ul>
        `,
        differential: `
            <table class="clinical-evidence-table">
                <thead>
                    <tr>
                        <th>Condition</th>
                        <th>Key Distinguishing Features</th>
                        <th>Certainty Tier</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Pulmonary Embolism</strong></td>
                        <td>Pleuritic chest pain, prominent dyspnea, tachypnea, tachycardia; D-dimer elevated, CT-PA diagnostic.</td>
                        <td><span class="evidence-quality-pill quality-moderate">Moderate ●</span></td>
                    </tr>
                    <tr>
                        <td><strong>Aortic Dissection</strong></td>
                        <td>Sudden onset tearing interscapular back pain, asymmetric peripheral pulses or BP differential &gt;20 mmHg.</td>
                        <td><span class="evidence-quality-pill quality-limited">Limited ●</span></td>
                    </tr>
                    <tr>
                        <td><strong>Acute Pericarditis</strong></td>
                        <td>Sharp chest pain relieved by sitting forward; diffuse concave ST elevation with PR depression on ECG.</td>
                        <td><span class="evidence-quality-pill quality-limited">Limited ●</span></td>
                    </tr>
                    <tr>
                        <td><strong>Esophageal Spasm / GERD</strong></td>
                        <td>Retrosternal burning or pain relieved by antacids; unrelated to physical exertion; normal cardiac biomarkers.</td>
                        <td><span class="evidence-quality-pill quality-limited">Limited ●</span></td>
                    </tr>
                </tbody>
            </table>
        `,
        risk_factors: `
            <ul class="clinical-bullet-list">
                <li><strong>Non-modifiable:</strong> Age (males &ge;45, females &ge;55), male biological sex, family history of premature CAD (first-degree male relative &lt;55y, female &lt;65y).</li>
                <li><strong>Modifiable:</strong> Systemic arterial hypertension, Type 2 diabetes mellitus, dyslipidemia (elevated LDL-C, low HDL-C, elevated ApoB), active tobacco smoking, central adiposity, chronic kidney disease (eGFR &lt;60 mL/min).</li>
            </ul>
        `,
        investigations: `
            <ul class="clinical-bullet-list">
                <li><strong>12-Lead ECG:</strong> Acquired and interpreted within 10 minutes of arrival. Evaluate for ST elevation (&ge;1mm in &ge;2 contiguous leads), horizontal/downsloping ST depression, T-wave inversion, or new LBBB.</li>
                <li><strong>High-Sensitivity Cardiac Troponin (hs-cTnI / hs-cTnT):</strong> STAT testing with validated 0h/1h or 0h/2h serial algorithm.</li>
                <li><strong>Transthoracic Echocardiography (TTE):</strong> Bedside evaluation for regional wall motion abnormalities, left ventricular ejection fraction (LVEF), and rule-out of mechanical complications.</li>
                <li><strong>Coronary Angiography:</strong> Immediate catheterization for STEMI (door-to-balloon &lt;90 min) or high-risk NSTE-ACS (&lt;24 hours).</li>
            </ul>
        `,
        management: `
            <ul class="clinical-bullet-list">
                <li><strong>Dual Antiplatelet Therapy (DAPT):</strong> Aspirin 162–325 mg chewed immediately + P2Y12 inhibitor loading (Ticagrelor 180 mg, Prasugrel 60 mg, or Clopidogrel 300–600 mg).</li>
                <li><strong>Anticoagulation:</strong> Unfractionated Heparin (weight-adjusted bolus + infusion) or Enoxaparin (1 mg/kg SC Q12H).</li>
                <li><strong>Anti-ischemic Therapy:</strong> Sublingual nitroglycerin 0.4 mg Q5min x3 for active chest pain; oral beta-blocker (Metoprolol tartrate) within 24 hours if hemodynamically stable.</li>
                <li><strong>High-Intensity Statin:</strong> Atorvastatin 80 mg PO QD initiated regardless of baseline lipid levels.</li>
            </ul>
        `,
        references: `
            <div class="reference-citation-item">
                <strong>ACC/AHA Joint Committee Clinical Practice Guidelines (2025):</strong> Guideline for the Management of Patients with Non-ST-Elevation Acute Coronary Syndromes. <em>Circulation</em>.
            </div>
            <div class="reference-citation-item">
                <strong>ESC Guidelines for the Management of Acute Coronary Syndromes (2023):</strong> European Heart Journal, 44(38):3720–3826.
            </div>
            <div class="reference-citation-item">
                <strong>Fourth Universal Definition of Myocardial Infarction (2018):</strong> Joint ESC/ACC/AHA/WHF Expert Consensus Document. <em>J Am Coll Cardiol</em>, 72(18):2231–2264.
            </div>
        `
    },
    pe: {
        title: "Pulmonary Embolism",
        meta: "Pulmonology & Vascular Medicine • ICD-11: BD10",
        overview: "Pulmonary Embolism (PE) is the acute occlusion of the pulmonary arterial bed by a thrombus originating from the deep venous system of the lower extremities (DVT). It impairs gas exchange and increases right ventricular afterload, with potential for acute right ventricular failure and cardiogenic shock.",
        presentation: `
            <ul class="clinical-bullet-list">
                <li><strong>Acute Dyspnea:</strong> Sudden onset unexplained shortness of breath at rest or exertion (75–85% of cases).</li>
                <li><strong>Pleuritic Chest Pain:</strong> Sharp pain aggravated by inspiration (65–75%).</li>
                <li><strong>Tachypnea & Tachycardia:</strong> Respiratory rate &gt;20 bpm and heart rate &gt;100 bpm.</li>
                <li><strong>Hemoptysis:</strong> Associated with pulmonary infarction.</li>
            </ul>
        `,
        differential: `
            <ul class="clinical-bullet-list">
                <li>Acute Coronary Syndrome (ACS)</li>
                <li>Aortic Dissection</li>
                <li>Community-Acquired Pneumonia</li>
                <li>Pneumothorax</li>
            </ul>
        `,
        risk_factors: `
            <ul class="clinical-bullet-list">
                <li>Virchow's Triad: Venous stasis (prolonged immobilization, long flights), endothelial injury (trauma, orthopedic surgery), hypercoagulability (malignancy, Factor V Leiden, antiphospholipid syndrome).</li>
                <li>Estrogen-containing medications, prior DVT/PE history, obesity, active malignancy.</li>
            </ul>
        `,
        investigations: `
            <ul class="clinical-bullet-list">
                <li><strong>Wells Score / Geneva Score:</strong> Pre-test clinical probability stratification.</li>
                <li><strong>D-Dimer:</strong> High sensitivity test used to rule out PE in low/intermediate risk patients (age-adjusted cut-off).</li>
                <li><strong>CT Pulmonary Angiography (CTPA):</strong> Gold standard diagnostic modality.</li>
                <li><strong>Bedside Echocardiography:</strong> Assess for RV dilation, McConnell's sign, or pulmonary hypertension in hemodynamically unstable patients.</li>
            </ul>
        `,
        management: `
            <ul class="clinical-bullet-list">
                <li><strong>Anticoagulation:</strong> Direct Oral Anticoagulant (Apixaban, Rivaroxaban) or LMWH bridging to Warfarin.</li>
                <li><strong>Systemic Thrombolysis:</strong> Intravenous Alteplase (tPA 100 mg over 2 hours) indicated for high-risk massive PE with systemic hypotension.</li>
            </ul>
        `,
        references: `
            <div class="reference-citation-item">
                <strong>ESC/ERS Guidelines for the diagnosis and management of acute pulmonary embolism (2019):</strong> <em>European Heart Journal</em>, 41(4):543–603.
            </div>
        `
    },
    aortic_dissection: {
        title: "Aortic Dissection",
        meta: "Cardiothoracic & Vascular Emergency • ICD-11: BD50",
        overview: "Aortic dissection occurs when a tear in the aortic intima allows blood to surge into the media layer, propagating along the vessel length and creating a false lumen. Categorized into Stanford Type A (ascending aorta involvement, surgical emergency) and Stanford Type B (descending aorta only).",
        presentation: `
            <ul class="clinical-bullet-list">
                <li><strong>Abrupt Tearing / Ripping Pain:</strong> Sudden maximal intensity pain in anterior chest (Type A) or interscapular back (Type B).</li>
                <li><strong>Pulse Deficit:</strong> Asymmetric radial or femoral pulses with &gt;20 mmHg SBP variation between arms.</li>
                <li><strong>New Aortic Regurgitation Murmur:</strong> Early diastolic decrescendo murmur at right sternal border.</li>
                <li><strong>Neurological Deficits:</strong> Syncope, stroke symptoms, or paraplegia due to spinal cord ischemia.</li>
            </ul>
        `,
        differential: `
            <ul class="clinical-bullet-list">
                <li>Acute Myocardial Infarction</li>
                <li>Pulmonary Embolism</li>
                <li>Pericardial Tamponade</li>
                <li>Musculoskeletal chest wall strain</li>
            </ul>
        `,
        risk_factors: `
            <ul class="clinical-bullet-list">
                <li>Chronic poorly controlled hypertension (present in &gt;70% of cases).</li>
                <li>Connective tissue disorders (Marfan syndrome, Loeys-Dietz, vascular Ehlers-Danlos).</li>
                <li>Bicuspid aortic valve, aortic coarctation, prior cardiac surgery, cocaine abuse.</li>
            </ul>
        `,
        investigations: `
            <ul class="clinical-bullet-list">
                <li><strong>CT Angiography of Chest/Abdomen/Pelvis:</strong> Definitive diagnostic test of choice.</li>
                <li><strong>Transesophageal Echocardiography (TEE):</strong> Rapid bedside modality for unstable patients in resuscitation bay or OR.</li>
            </ul>
        `,
        management: `
            <ul class="clinical-bullet-list">
                <li><strong>Immediate Blood Pressure & Heart Rate Control:</strong> IV Beta-blockers (Esmolol or Labetalol) to target HR &lt;60 bpm and SBP &lt;100–120 mmHg.</li>
                <li><strong>Stanford Type A:</strong> Emergent surgical repair / graft replacement.</li>
                <li><strong>Stanford Type B:</strong> Medical management in ICU; Thoracic Endovascular Aortic Repair (TEVAR) for complicated cases.</li>
            </ul>
        `,
        references: `
            <div class="reference-citation-item">
                <strong>ACC/AHA Guideline for the Diagnosis and Management of Aortic Disease (2022):</strong> <em>J Am Coll Cardiol</em>, 80(24):e223–e393.
            </div>
        `
    },
    pneumonia: {
        title: "Community-Acquired Pneumonia",
        meta: "Pulmonology & Infectious Disease • ICD-11: CA40",
        overview: "Community-Acquired Pneumonia (CAP) is an acute infection of the pulmonary parenchyma acquired outside of hospital or long-term care settings. Common bacterial etiologies include Streptococcus pneumoniae, Haemophilus influenzae, and atypical pathogens (Mycoplasma pneumoniae, Legionella).",
        presentation: `
            <ul class="clinical-bullet-list">
                <li><strong>Productive Cough:</strong> Purulent or rust-colored sputum production.</li>
                <li><strong>Fever & Chills:</strong> Core body temperature &gt;38.0°C with rigors.</li>
                <li><strong>Pleuritic Chest Pain:</strong> Pain localized to the affected hemithorax.</li>
                <li><strong>Physical Signs:</strong> Dullness to percussion, bronchial breath sounds, inspiratory crackles/crepitations.</li>
            </ul>
        `,
        differential: `
            <ul class="clinical-bullet-list">
                <li>Acute Bronchitis</li>
                <li>Congestive Heart Failure exacerbation</li>
                <li>Pulmonary Embolism</li>
                <li>Bronchiectasis with acute superinfection</li>
            </ul>
        `,
        risk_factors: `
            <ul class="clinical-bullet-list">
                <li>Advanced age (&ge;65 years), chronic obstructive pulmonary disease (COPD), structural lung disease, immunocompromise, tobacco smoking, aspiration risk.</li>
            </ul>
        `,
        investigations: `
            <ul class="clinical-bullet-list">
                <li><strong>Chest Radiography (PA & Lateral):</strong> Demonstration of lobar consolidation, patchy alveolar infiltrates, or air bronchograms.</li>
                <li><strong>CURB-65 / PSI Score:</strong> Objective risk stratification for inpatient vs. outpatient disposition.</li>
                <li><strong>Microbiological Studies:</strong> Sputum gram stain and culture, blood cultures, urinary Legionella/Pneumococcal antigens in severe cases.</li>
            </ul>
        `,
        management: `
            <ul class="clinical-bullet-list">
                <li><strong>Outpatient:</strong> High-dose Amoxicillin 1g PO TID or Amoxicillin/Clavulanate 875/125 mg PO BID + Macrolide / Doxycycline.</li>
                <li><strong>Inpatient (Non-ICU):</strong> IV Ceftriaxone 1–2g QD + Azithromycin 500mg QD or respiratory fluoroquinolone (Levofloxacin).</li>
            </ul>
        `,
        references: `
            <div class="reference-citation-item">
                <strong>ATS/IDSA Clinical Practice Guideline on Community-Acquired Pneumonia (2019):</strong> <em>Am J Respir Crit Care Med</em>, 200(7):e45–e67.
            </div>
        `
    },
    stroke: {
        title: "Acute Ischemic Stroke",
        meta: "Neurology & Neurovascular Emergency • ICD-11: 8B11",
        overview: "Acute ischemic stroke results from focal cerebral ischemia caused by arterial occlusion (thromboembolism or large artery atherosclerosis), causing neuronal cell death within the core infarct and surrounding salvageable ischemic penumbra.",
        presentation: `
            <ul class="clinical-bullet-list">
                <li><strong>FAST Signs:</strong> Facial droop, unilateral arm/leg weakness or numbness, speech difficulty (aphasia or dysarthria).</li>
                <li><strong>Additional Deficits:</strong> Visual field cuts (hemianopia), acute vertigo, ataxia, or gaze deviation.</li>
            </ul>
        `,
        differential: `
            <ul class="clinical-bullet-list">
                <li>Intracranial Hemorrhage (ICH)</li>
                <li>Transient Ischemic Attack (TIA)</li>
                <li>Hypoglycemia (mimicking stroke deficits)</li>
                <li>Seizure with Todd's Paresis</li>
            </ul>
        `,
        risk_factors: `
            <ul class="clinical-bullet-list">
                <li>Hypertension, Atrial Fibrillation (cardioembolic risk), Diabetes Mellitus, Dyslipidemia, Carotid stenosis, Smoking.</li>
            </ul>
        `,
        investigations: `
            <ul class="clinical-bullet-list">
                <li><strong>Emergency Non-Contrast Brain CT:</strong> Rule out hemorrhage immediately.</li>
                <li><strong>CT Angiography (CTA) + CT Perfusion:</strong> Identify Large Vessel Occlusion (LVO) and ischemic core vs penumbra volume.</li>
                <li><strong>Point-of-care Blood Glucose:</strong> Rule out hypoglycemia prior to thrombolysis.</li>
            </ul>
        `,
        management: `
            <ul class="clinical-bullet-list">
                <li><strong>Intravenous Thrombolysis (IV Alteplase / Tenecteplase):</strong> Administer within 4.5 hours of symptom onset if eligible.</li>
                <li><strong>Endovascular Thrombectomy (EVT):</strong> Indicated for anterior circulation large vessel occlusion (ICA, MCA M1) within 6 to 24 hours.</li>
            </ul>
        `,
        references: `
            <div class="reference-citation-item">
                <strong>AHA/ASA Guidelines for the Early Management of Patients With Acute Ischemic Stroke (2019/2024 update):</strong> <em>Stroke</em>.
            </div>
        `
    },
    diabetes_t2: {
        title: "Type 2 Diabetes Mellitus",
        meta: "Endocrinology & Metabolic Disease • ICD-11: 5A11",
        overview: "Type 2 Diabetes Mellitus is a progressive metabolic disorder characterized by peripheral insulin resistance, inadequate compensatory insulin secretion by pancreatic beta cells, and chronic hyperglycemia leading to micro- and macrovascular complications.",
        presentation: `
            <ul class="clinical-bullet-list">
                <li><strong>Classical Osmotic Symptoms:</strong> Polyuria, polydipsia, polyphagia, unexplained weight loss.</li>
                <li><strong>Insidious Findings:</strong> Recurrent fungal infections, delayed wound healing, visual blurring, peripheral neuropathy (paresthesias).</li>
            </ul>
        `,
        differential: `
            <ul class="clinical-bullet-list">
                <li>Type 1 Diabetes Mellitus / LADA</li>
                <li>Secondary Diabetes (Corticosteroid-induced, Pancreatitis)</li>
                <li>Impaired Fasting Glucose / Pre-diabetes</li>
            </ul>
        `,
        risk_factors: `
            <ul class="clinical-bullet-list">
                <li>Overweight / Obesity (BMI &ge;25 kg/m²), physical inactivity, first-degree family history of T2D, high-risk ethnicity, history of gestational diabetes.</li>
            </ul>
        `,
        investigations: `
            <ul class="clinical-bullet-list">
                <li><strong>Diagnostic Criteria:</strong> HbA1c &ge;6.5%, Fasting Plasma Glucose &ge;126 mg/dL (7.0 mmol/L), or 2-hr 75g OGTT &ge;200 mg/dL.</li>
                <li><strong>Baseline Complication Screening:</strong> Urine albumin-to-creatinine ratio (UACR), serum creatinine/eGFR, dilated eye examination, comprehensive foot exam.</li>
            </ul>
        `,
        management: `
            <ul class="clinical-bullet-list">
                <li><strong>First-Line Pharmacotherapy:</strong> Metformin 500–2,000 mg/day with lifestyle modification.</li>
                <li><strong>Organ-Protective Second-Line Agents:</strong> SGLT2 inhibitors (Empagliflozin, Dapagliflozin) and GLP-1 receptor agonists (Semaglutide) prioritized for patients with established ASCVD, heart failure, or CKD.</li>
            </ul>
        `,
        references: `
            <div class="reference-citation-item">
                <strong>ADA Standards of Care in Diabetes (2025):</strong> <em>Diabetes Care</em>, 48(Suppl 1):S1–S320.
            </div>
        `
    }
};

document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initIndexSelection();
    initSearch();
    initModuleTabs();
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
            const disKey = item.getAttribute('data-dis');
            loadDiseaseKnowledge(disKey);
        });
    });
}

function loadDiseaseKnowledge(key) {
    const data = DISEASE_KNOWLEDGE[key];
    if (!data) return;

    document.getElementById('disTitle').innerText = data.title;
    document.getElementById('disMeta').innerText = data.meta;
    document.getElementById('disOverview').innerHTML = data.overview;
    document.getElementById('disPresentation').innerHTML = data.presentation;
    document.getElementById('disDifferential').innerHTML = data.differential;
    document.getElementById('disRiskFactors').innerHTML = data.risk_factors;
    document.getElementById('disInvestigations').innerHTML = data.investigations;
    document.getElementById('disManagement').innerHTML = data.management;
    document.getElementById('disReferences').innerHTML = data.references;

    document.getElementById('diseaseSearchInput').value = data.title;
}

function initSearch() {
    const searchInput = document.getElementById('diseaseSearchInput');
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
            loadDiseaseKnowledge(matchedFirst.getAttribute('data-dis'));
        }
    });
}

function initModuleTabs() {
    const tabBtns = document.querySelectorAll('.disease-ref-tab-btn');
    const panes = document.querySelectorAll('.disease-ref-pane');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => {
                b.classList.remove('active');
                b.setAttribute('aria-selected', 'false');
            });
            panes.forEach(p => p.classList.remove('active'));

            btn.classList.add('active');
            btn.setAttribute('aria-selected', 'true');
            const paneName = btn.getAttribute('data-pane');
            const targetPane = document.getElementById(`pane-${paneName}`);
            if (targetPane) targetPane.classList.add('active');
        });
    });
}
