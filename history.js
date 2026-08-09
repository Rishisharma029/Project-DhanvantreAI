/**
 * AURAMED AI — MEDICAL HISTORY CONTROLLER
 */

const API_BASE = '/api/v1';
let currentCategory = 'all';

document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    initSearchInput();
    initCategoryFilters();
    loadTimelineEvents();
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

/* 2. Real-time Search */
function initSearchInput() {
    const searchInput = document.getElementById('historySearchInput');
    let timer = null;

    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            clearTimeout(timer);
            timer = setTimeout(() => {
                filterTimelineNodes(e.target.value.toLowerCase(), currentCategory);
            }, 200);
        });
    }
}

/* 3. Category Filter Pills */
function initCategoryFilters() {
    document.querySelectorAll('.history-filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.history-filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            currentCategory = btn.getAttribute('data-cat');
            const searchVal = document.getElementById('historySearchInput').value.toLowerCase();
            filterTimelineNodes(searchVal, currentCategory);
        });
    });
}

function filterTimelineNodes(query, category) {
    const nodes = document.querySelectorAll('.timeline-node');

    nodes.forEach(node => {
        const cat = node.getAttribute('data-cat');
        const text = node.innerText.toLowerCase();

        const matchCat = (category === 'all' || cat === category);
        const matchQuery = (!query || text.includes(query));

        if (matchCat && matchQuery) {
            node.style.display = 'block';
        } else {
            node.style.display = 'none';
        }
    });
}

/* 4. Fetch Timeline Events */
async function loadTimelineEvents() {
    try {
        const res = await fetch(`${API_BASE}/history/timeline`);
        if (res.ok) {
            const data = await res.json();
            if (data.events && data.events.length > 0) {
                renderTimelineNodes(data.events);
            }
        }
    } catch (err) {
        console.warn('History timeline fetch failed, using pre-rendered HTML nodes:', err);
    }
}

function renderTimelineNodes(events) {
    const stream = document.getElementById('timelineStream');

    stream.innerHTML = events.map(e => `
        <div class="timeline-node" data-cat="${e.category || 'assessment'}">
            <div class="node-icon-dot" style="border-color: ${getCategoryColor(e.category)}; color: ${getCategoryColor(e.category)};">
                <i class="${getCategoryIcon(e.category)}"></i>
            </div>
            <div class="node-card">
                <div class="node-header">
                    <span class="badge" style="background: rgba(6,182,212,0.15); color: ${getCategoryColor(e.category)};">${escapeHtml(e.badge || 'Assessment')}</span>
                    <span class="node-date">${escapeHtml(e.date || 'Aug 01, 2026')}</span>
                </div>
                <h3 style="font-size: 1.15rem; font-weight: 800; margin-bottom: 6px;">${escapeHtml(e.title)}</h3>
                <p class="text-sm text-muted" style="margin-bottom: 14px;">${escapeHtml(e.description)}</p>
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <span style="font-size: 0.8rem; color: var(--accent-cyan);"><i class="fa-solid fa-user-doctor"></i> ${escapeHtml(e.doctor || 'Dr. A. Vance, MD')}</span>
                    <a href="${e.link || 'report_viewer.html'}" class="btn btn-secondary btn-sm">View Details <i class="fa-solid fa-chevron-right"></i></a>
                </div>
            </div>
        </div>
    `).join('');
}

function getCategoryColor(cat) {
    if (cat === 'emergency') return 'var(--accent-rose)';
    if (cat === 'prescription') return 'var(--accent-teal)';
    if (cat === 'lab') return 'var(--accent-purple)';
    return 'var(--accent-cyan)';
}

function getCategoryIcon(cat) {
    if (cat === 'emergency') return 'fa-solid fa-truck-medical';
    if (cat === 'prescription') return 'fa-solid fa-pills';
    if (cat === 'lab') return 'fa-solid fa-flask-vial';
    return 'fa-solid fa-notes-medical';
}

function escapeHtml(str) {
    return String(str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
