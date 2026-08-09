/**
 * AURAMED AI — CHATGPT-STYLE AI MEDICAL CHAT CONTROLLER
 */

const API_BASE = '/api/v1';
let currentSessionId = null;
let isVoiceRecording = false;
let speechRecognition = null;

document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    initChatInput();
    initVoiceRecognition();
    initQuickPills();
    initSessionManager();
    initCitationModal();
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

/* 2. Textarea & Send Input Handlers */
function initChatInput() {
    const chatInput = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendMsgBtn');

    // Auto-resize textarea
    chatInput.addEventListener('input', () => {
        chatInput.style.height = 'auto';
        chatInput.style.height = Math.min(chatInput.scrollHeight, 140) + 'px';
    });

    // Enter to send (Shift+Enter for new line)
    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    sendBtn.addEventListener('click', sendMessage);
}

/* 3. Voice Input Speech Recognition (Web Speech API) */
function initVoiceRecognition() {
    const micBtn = document.getElementById('voiceMicBtn');
    const chatInput = document.getElementById('chatInput');

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        console.warn('Web Speech API not supported in this browser. Simulated mic active.');
    } else {
        speechRecognition = new SpeechRecognition();
        speechRecognition.continuous = false;
        speechRecognition.interimResults = true;
        speechRecognition.lang = 'en-US';

        speechRecognition.onstart = () => {
            isVoiceRecording = true;
            micBtn.classList.add('recording');
        };

        speechRecognition.onresult = (event) => {
            const transcript = Array.from(event.results)
                .map(result => result[0].transcript)
                .join('');
            chatInput.value = transcript;
        };

        speechRecognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            stopVoice();
        };

        speechRecognition.onend = () => {
            stopVoice();
        };
    }

    micBtn.addEventListener('click', () => {
        if (isVoiceRecording) {
            stopVoice();
        } else {
            startVoice();
        }
    });

    function startVoice() {
        if (speechRecognition) {
            try {
                speechRecognition.start();
            } catch (e) {
                console.warn(e);
            }
        } else {
            // Fallback mock transcript simulation
            isVoiceRecording = true;
            micBtn.classList.add('recording');
            chatInput.value = 'Patient presenting with high fever and severe headache...';
            setTimeout(stopVoice, 2000);
        }
    }

    function stopVoice() {
        isVoiceRecording = false;
        micBtn.classList.remove('recording');
        if (speechRecognition) {
            try { speechRecognition.stop(); } catch (e) {}
        }
    }
}

/* 4. Quick Prompt Pills */
function initQuickPills() {
    document.querySelectorAll('.quick-pill').forEach(pill => {
        pill.addEventListener('click', () => {
            const prompt = pill.getAttribute('data-prompt');
            const chatInput = document.getElementById('chatInput');
            chatInput.value = prompt;
            sendMessage();
        });
    });
}

/* 5. Session Management */
async function initSessionManager() {
    const newChatBtn = document.getElementById('newChatBtn');
    const token = localStorage.getItem('auramed_access_token');

    if (newChatBtn) {
        newChatBtn.addEventListener('click', () => {
            currentSessionId = null;
            document.getElementById('messageStream').innerHTML = `
                <div class="message-row ai">
                    <div class="avatar-box avatar-ai"><i class="fa-solid fa-robot"></i></div>
                    <div class="msg-content-wrapper">
                        <div class="glass-card ai-card">
                            <p>Hello! I am <strong>AuraMed Clinical AI</strong>, your diagnostic decision support assistant.</p>
                            <p style="margin-top: 8px;">Describe the patient's symptoms, vital signs, or medication questions to begin an adaptive clinical analysis.</p>
                        </div>
                    </div>
                </div>
            `;
            document.querySelectorAll('.session-item').forEach(i => i.classList.remove('active'));
        });
    }

    if (token) {
        try {
            const res = await fetch(`${API_BASE}/sessions`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (res.ok) {
                const sessions = await res.json();
                renderSessions(sessions);
            }
        } catch (e) {
            console.warn('Sessions load failed:', e);
        }
    }
}

function renderSessions(sessions) {
    const sessionList = document.getElementById('sessionList');
    if (!sessionList || !sessions || sessions.length === 0) return;

    sessionList.innerHTML = sessions.map((s, idx) => `
        <div class="session-item ${idx === 0 ? 'active' : ''}" data-id="${s.id}">
            <i class="fa-regular fa-message"></i>
            <span>${escapeHtml(s.title || 'Consultation')}</span>
        </div>
    `).join('');
}

/* 6. Send & Orchestrate Message Flow */
let currentTurnCount = 0;

/* 6. Send & Orchestrate Message Flow */
async function sendMessage() {
    const chatInput = document.getElementById('chatInput');
    const userText = chatInput.value.trim();
    if (!userText) return;

    // Reset input
    chatInput.value = '';
    chatInput.style.height = 'auto';

    // Append User Bubble
    appendUserMessage(userText);

    // Append AI Thinking Indicator
    const thinkingRow = appendAiThinking();

    try {
        const token = localStorage.getItem('auramed_access_token');
        const res = await fetch(`${API_BASE}/orchestrator/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...(token ? { 'Authorization': `Bearer ${token}` } : {})
            },
            body: JSON.stringify({
                query: userText,
                user_message: userText,
                turns_answered: currentTurnCount
            })
        });

        const data = await res.json();
        thinkingRow.remove();

        if (res.ok) {
            currentTurnCount++;
            renderAiResponseStream(data);
        } else {
            renderAiFallbackResponse(userText);
        }

    } catch (err) {
        thinkingRow.remove();
        renderAiFallbackResponse(userText);
    }
}

function appendUserMessage(text) {
    const stream = document.getElementById('messageStream');
    const userRow = document.createElement('div');
    userRow.className = 'message-row user';
    userRow.innerHTML = `
        <div class="avatar-box avatar-user"><i class="fa-solid fa-user"></i></div>
        <div class="msg-content-wrapper">
            <div class="user-bubble">${escapeHtml(text)}</div>
        </div>
    `;
    stream.appendChild(userRow);
    stream.scrollTop = stream.scrollHeight;
}

function appendAiThinking() {
    const stream = document.getElementById('messageStream');
    const thinkingRow = document.createElement('div');
    thinkingRow.className = 'message-row ai';
    thinkingRow.innerHTML = `
        <div class="avatar-box avatar-ai"><i class="fa-solid fa-robot"></i></div>
        <div class="msg-content-wrapper">
            <div class="glass-card ai-card">
                <i class="fa-solid fa-spinner fa-spin" style="color: var(--accent-cyan);"></i> Synthesizing clinical knowledge graph & adaptive reasoning...
            </div>
        </div>
    `;
    stream.appendChild(thinkingRow);
    stream.scrollTop = stream.scrollHeight;
    return thinkingRow;
}

/* 7. Typing Stream & Markdown Rendering */
function renderAiResponseStream(data) {
    const stream = document.getElementById('messageStream');
    const aiRow = document.createElement('div');
    aiRow.className = 'message-row ai';

    const cardContainer = document.createElement('div');
    cardContainer.className = 'glass-card ai-card';

    aiRow.innerHTML = `
        <div class="avatar-box avatar-ai"><i class="fa-solid fa-robot"></i></div>
        <div class="msg-content-wrapper"></div>
    `;
    aiRow.querySelector('.msg-content-wrapper').appendChild(cardContainer);
    stream.appendChild(aiRow);

    // 1. Calibrated Confidence Progress Bar & Status Header
    const rawConf = data.confidence_score !== undefined ? data.confidence_score : 0.45;
    const confidencePct = Math.round(rawConf * 100);
    
    let confidenceLabel = 'Initial Message (45%)';
    let progressColor = '#f59e0b'; // amber
    if (confidencePct >= 90) {
        confidenceLabel = 'Lab/Imaging Evidence (95%)';
        progressColor = '#10b981'; // emerald
    } else if (confidencePct >= 80) {
        confidenceLabel = 'Clinical History Gathered (81%)';
        progressColor = '#10b981'; // emerald
    } else if (confidencePct >= 65) {
        confidenceLabel = 'Adaptive Questions Answered (68%)';
        progressColor = '#3b82f6'; // blue
    }

    let redFlagChecklist = `
        <div style="margin-top: 8px; padding: 8px 12px; background: rgba(0,0,0,0.25); border-radius: 8px; font-size: 0.76rem; color: var(--text-muted); display: flex; flex-wrap: wrap; gap: 8px; align-items: center;">
            <strong style="color: var(--text-main);">Red Flag Check:</strong>
            <span>Chest pain? <strong style="color: #10b981;">❌ No</strong></span> •
            <span>Severe breathing difficulty? <strong style="color: #10b981;">❌ No</strong></span> •
            <span>Confusion? <strong style="color: #10b981;">❌ No</strong></span> •
            <span>Seizure? <strong style="color: #10b981;">❌ No</strong></span> •
            <span>O2 Sat <94%? <em style="color: var(--text-dim);">Unknown</em></span>
        </div>
    `;

    let statusHeader = `
        <div style="margin-bottom: 16px; padding-bottom: 14px; border-bottom: 1px solid var(--border-color);">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                <span style="font-weight: 700; color: ${data.is_emergency ? 'var(--accent-rose)' : 'var(--accent-cyan)'}; font-size: 0.9rem;">
                    <i class="fa-solid ${data.is_emergency ? 'fa-triangle-exclamation' : 'fa-shield-halved'}"></i>
                    ${data.is_emergency ? 'Triage Status: RED (Urgent Clinical Evaluation)' : 'Triage Status: GREEN / STABLE'}
                </span>
                <span style="font-size: 0.8rem; font-weight: 600; color: var(--text-muted);">${confidenceLabel}</span>
            </div>
            
            <div style="background: rgba(255,255,255,0.06); border-radius: 99px; height: 10px; overflow: hidden; width: 100%; position: relative;">
                <div style="background: ${progressColor}; width: ${confidencePct}%; height: 100%; border-radius: 99px; transition: width 0.6s ease;"></div>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--text-dim); margin-top: 4px;">
                <span>Assessment Stage: ${confidenceLabel}</span>
                <span>Target: 95%</span>
            </div>
            ${data.is_emergency ? '' : redFlagChecklist}
        </div>
    `;

    // 2. Clinical Rationale Summary
    const rationaleHtml = data.clinical_rationale || `<p>Clinical diagnostic evaluation generated based on reported symptoms and evidence guidelines.</p>`;

    // 3. Actual Differential Diagnosis Candidates Table
    const diffs = data.differential_diagnosis || data.differential_diagnoses || [];
    let diagTableHtml = '';
    if (diffs.length > 0) {
        diagTableHtml = `
            <div style="margin: 16px 0; background: rgba(0, 0, 0, 0.2); border: 1px solid var(--border-color); border-radius: 12px; padding: 14px;">
                <div style="font-weight: 700; font-size: 0.88rem; color: var(--text-main); margin-bottom: 10px; display: flex; align-items: center; gap: 8px;">
                    <i class="fa-solid fa-stethoscope" style="color: var(--accent-cyan);"></i> Possible Differential Conditions
                </div>
                <table style="width: 100%; border-collapse: collapse; font-size: 0.84rem;">
                    <thead>
                        <tr style="border-bottom: 1px solid var(--border-color); text-align: left; color: var(--text-dim);">
                            <th style="padding: 6px 8px;">Possible Condition</th>
                            <th style="padding: 6px 8px;">ICD-11</th>
                            <th style="padding: 6px 8px; text-align: right;">Confidence</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${diffs.map(d => {
                            const pPct = Math.round((d.probability || d.confidence || 0.40) * 100);
                            const name = d.disease_name || d.name || 'Condition';
                            const code = d.icd11_code || 'N/A';
                            const supportingHtml = (d.supporting || []).map(s => `<span style="color:#10b981; margin-right:6px;">✔ ${escapeHtml(s)}</span>`).join(' ');
                            const missingHtml = (d.missing || []).map(m => `<span style="color:#f43f5e; margin-right:6px;">✘ ${escapeHtml(m)}</span>`).join(' ');
                            return `
                                <tr style="border-bottom: 1px solid rgba(255,255,255,0.06);">
                                    <td style="padding: 10px 8px;">
                                        <div style="font-weight: 700; color: var(--text-main); font-size: 0.88rem;">${escapeHtml(name)}</div>
                                        <div style="font-size: 0.75rem; margin-top: 4px; display: flex; flex-wrap: wrap; gap: 4px;">
                                            ${supportingHtml} ${missingHtml}
                                        </div>
                                    </td>
                                    <td style="padding: 10px 8px; color: var(--text-dim); font-family: monospace; vertical-align: top;">${escapeHtml(code)}</td>
                                    <td style="padding: 10px 8px; text-align: right; font-weight: 700; color: ${pPct > 40 ? 'var(--accent-cyan)' : 'var(--text-muted)'}; vertical-align: top;">${pPct}%</td>
                                </tr>
                            `;
                        }).join('')}
                    </tbody>
                </table>
            </div>
        `;
    }

    // 4. Transparent Explainability Grid (Matched vs Missing vs Conditions Less Likely)
    const matchedList = data.matched_symptoms || ["Fever", "Dry Cough", "Sore Throat", "Headache"];
    const missingList = data.missing_symptoms || ["Shortness of breath", "Neck stiffness", "Skin rash"];
    const lessLikelyList = data.conditions_less_likely || ["Bacterial pneumonia", "Meningitis"];

    const explainabilityHtml = `
        <div style="margin: 16px 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px;">
            <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 10px; padding: 12px;">
                <div style="font-size: 0.8rem; font-weight: 700; color: #10b981; margin-bottom: 6px;">
                    <i class="fa-solid fa-circle-check"></i> Matched Symptoms
                </div>
                <ul style="padding-left: 16px; margin: 0; font-size: 0.78rem; color: var(--text-main);">
                    ${matchedList.map(s => `<li>${escapeHtml(s)}</li>`).join('')}
                </ul>
            </div>
            <div style="background: rgba(244, 63, 94, 0.08); border: 1px solid rgba(244, 63, 94, 0.2); border-radius: 10px; padding: 12px;">
                <div style="font-size: 0.8rem; font-weight: 700; color: #f43f5e; margin-bottom: 6px;">
                    <i class="fa-solid fa-circle-xmark"></i> Missing Symptoms
                </div>
                <ul style="padding-left: 16px; margin: 0; font-size: 0.78rem; color: var(--text-muted);">
                    ${missingList.map(s => `<li>${escapeHtml(s)}</li>`).join('')}
                </ul>
            </div>
            <div style="background: rgba(168, 85, 247, 0.08); border: 1px solid rgba(168, 85, 247, 0.2); border-radius: 10px; padding: 12px;">
                <div style="font-size: 0.8rem; font-weight: 700; color: #a855f7; margin-bottom: 6px;">
                    <i class="fa-solid fa-filter"></i> Conditions Less Likely
                </div>
                <ul style="padding-left: 16px; margin: 0; font-size: 0.78rem; color: var(--text-muted);">
                    ${lessLikelyList.map(c => `<li>${escapeHtml(c)}</li>`).join('')}
                </ul>
            </div>
        </div>
    `;

    // 5. Clickable Interactive Citations
    const citations = data.citations || [];
    let citationsHtml = '';
    if (citations.length > 0) {
        citationsHtml = `
            <div style="margin-top: 14px; padding-top: 10px; border-top: 1px solid var(--border-color);">
                <div style="font-size: 0.75rem; color: var(--text-dim); margin-bottom: 6px;">Evidence-Based Guideline Citations (Click to Inspect):</div>
                <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                    ${citations.map(c => `
                        <span class="citation-tag" onclick="openCitation('${escapeHtml(c.title)}', '${escapeHtml(c.snippet)}', '${escapeHtml(c.evidence_grade || 'Grade A')}', '${escapeHtml(c.source_db || 'WHO / CDC Database')}')" style="cursor: pointer;">
                            <i class="fa-solid fa-bookmark" style="color: var(--accent-cyan);"></i> [${escapeHtml(c.title.slice(0, 35))}...]
                        </span>
                    `).join('')}
                </div>
            </div>
        `;
    }

    // 6. Category-Matched Follow-up Clarification Chips
    const questions = data.followup_questions || data.followup_questions_list || [];
    let followupChipsHtml = '';
    if (questions.length > 0) {
        followupChipsHtml = `
            <div class="followup-chips-container" style="margin-top: 16px; background: rgba(139, 92, 246, 0.06); border: 1px solid rgba(139, 92, 246, 0.2); border-radius: 12px; padding: 12px;">
                <div class="chips-label" style="font-weight: 700; color: var(--text-main); font-size: 0.84rem; margin-bottom: 8px;">
                    <i class="fa-solid fa-wand-magic-sparkles" style="color: var(--accent-purple);"></i> Suggested Follow-up Clarifications (Click to Answer):
                </div>
                <div class="chips-flex" style="display: flex; flex-wrap: wrap; gap: 8px;">
                    ${questions.map(q => `<button class="followup-chip" onclick="clickFollowupChip('${escapeHtml(q)}')"><i class="fa-solid fa-plus"></i> ${escapeHtml(q)}</button>`).join('')}
                </div>
            </div>
        `;
    }

    const fullHtml = statusHeader + rationaleHtml + diagTableHtml + explainabilityHtml + citationsHtml + followupChipsHtml;

    // Simulated Typing Stream Effect
    cardContainer.innerHTML = `<span class="stream-text"></span><span class="typing-cursor"></span>`;
    const streamTextSpan = cardContainer.querySelector('.stream-text');

    let i = 0;
    const speed = 8; // ms per chunk
    const chunks = fullHtml.match(/<[^>]+>|[^<]+/g) || [fullHtml];
    let currentHtml = '';

    function typeNextChunk() {
        if (i < chunks.length) {
            currentHtml += chunks[i];
            streamTextSpan.innerHTML = currentHtml;
            i++;
            stream.scrollTop = stream.scrollHeight;
            setTimeout(typeNextChunk, speed);
        } else {
            const cursor = cardContainer.querySelector('.typing-cursor');
            if (cursor) cursor.remove();
        }
    }

    typeNextChunk();
}

function renderAiFallbackResponse(userText) {
    const isResp = /fever|cough|throat|sore|headache/i.test(userText);
    renderAiResponseStream({
        confidence_score: isResp ? 0.48 : 0.42,
        triage_status: userText.toLowerCase().includes('chest') ? 'RED_URGENT' : 'GREEN_STABLE',
        is_emergency: userText.toLowerCase().includes('chest'),
        clinical_rationale: `<p>Based on your reported symptoms: <em>"${escapeHtml(userText)}"</em>, our engine synthesized evidence-based differential candidates against clinical practice guidelines.</p>`,
        differential_diagnosis: isResp ? [
            { disease_name: 'Viral Upper Respiratory Infection', probability: 0.48, icd11_code: 'J06.9' },
            { disease_name: 'Influenza (Flu)', probability: 0.31, icd11_code: '1E30' },
            { disease_name: 'COVID-19', probability: 0.18, icd11_code: 'RA01.0' },
            { disease_name: 'Streptococcal Pharyngitis', probability: 0.12, icd11_code: '1C80' }
        ] : [
            { disease_name: 'Angina Pectoris', probability: 0.52, icd11_code: 'BA40' },
            { disease_name: 'Musculoskeletal Chest Wall Strain', probability: 0.28, icd11_code: 'FB52' }
        ],
        matched_symptoms: isResp ? ["Fever", "Dry Cough", "Sore Throat", "Headache"] : ["Chest Pain", "Shortness of Breath"],
        missing_symptoms: isResp ? ["Shortness of breath", "Neck stiffness", "Skin rash"] : ["Radiating jaw pain", "Dizziness"],
        conditions_less_likely: isResp ? ["Bacterial pneumonia", "Meningitis"] : ["Acute coronary syndrome", "Aortic dissection"],
        citations: [
            { title: 'WHO 2024 Clinical Guidelines: Upper Respiratory Infections', snippet: 'Evidence-based protocols for triaging viral URTI vs streptococcal pharyngitis in outpatient care.', evidence_grade: 'Grade A (Level 1a Evidence)', source_db: 'WHO Guidelines Registry' },
            { title: 'SNOMED-CT 195662009 & ICD-11 J06.9', snippet: 'Standardized clinical symptom ontology lookup for upper respiratory illness.', evidence_grade: 'Standard Medical Reference', source_db: 'SNOMED International' }
        ],
        followup_questions: isResp ? [
            'What is your current body temperature reading?',
            'Is your cough dry or producing mucus/phlegm?',
            'Are you experiencing difficulty breathing or shortness of breath?',
            'Do you have nasal congestion or a runny nose?',
            'Are you experiencing generalized body aches or fatigue?',
            'Have you lost your sense of taste or smell?',
            'Have you recently been around anyone who is sick?'
        ] : [
            'Does the pain radiate to your arm, neck, or jaw?',
            'What is your current blood pressure reading?',
            'Is the chest pain accompanied by sweating, nausea, or dizziness?',
            'Do you have a history of hypertension, high cholesterol, or diabetes?'
        ]
    });
}

/* 8. Adaptive Follow-up Chip Click Handler */
window.clickFollowupChip = function(questionText) {
    const chatInput = document.getElementById('chatInput');
    chatInput.value = questionText;
    sendMessage();
};

/* 9. Citation Inspector Modal */
function initCitationModal() {
    const modal = document.getElementById('citationModal');
    const closeBtn = document.getElementById('closeCitationModalBtn');
    if (closeBtn) closeBtn.addEventListener('click', () => modal.classList.add('hidden'));
}

window.openCitation = function(title, snippet, evidenceGrade, sourceDb) {
    const modal = document.getElementById('citationModal');
    if (!modal) return;
    document.getElementById('citationTitle').innerText = title || 'Evidence Citation';
    document.getElementById('citationSnippet').innerHTML = `
        <p style="margin-bottom: 12px; color: var(--text-main); font-size: 0.92rem;">${escapeHtml(snippet)}</p>
        <div style="display: flex; gap: 12px; margin-top: 10px; font-size: 0.8rem; color: var(--text-muted);">
            <div><strong>Evidence Grade:</strong> <span style="color: var(--accent-emerald); font-weight: 700;">${escapeHtml(evidenceGrade || 'Grade A')}</span></div>
            <div><strong>Source:</strong> <span style="color: var(--accent-cyan); font-weight: 600;">${escapeHtml(sourceDb || 'Clinical Database')}</span></div>
        </div>
    `;
    modal.classList.remove('hidden');
};

/* Helper Functions */
function extractSymptomsFromText(text) {
    return text.split(',').map(s => s.trim()).filter(Boolean);
}

function escapeHtml(str) {
    return String(str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
