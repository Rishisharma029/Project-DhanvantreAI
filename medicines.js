/**
 * AURAMED AI — MEDICINE EXPLORER CONTROLLER
 */

const API_BASE = '/api/v1';
let currentSearchBy = 'all';
let searchDebounceTimer = null;

document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    initSearchFilters();
    initQuickPills();
    initModalTabs();
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

/* 2. Search Input & Filter Pills */
function initSearchFilters() {
    const searchInput = document.getElementById('medSearchInput');
    const filterBtns = document.querySelectorAll('.filter-mode-btn');

    searchInput.addEventListener('input', (e) => {
        clearTimeout(searchDebounceTimer);
        searchDebounceTimer = setTimeout(() => {
            executeMedicineSearch(e.target.value, currentSearchBy);
        }, 300);
    });

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentSearchBy = btn.getAttribute('data-by');
            executeMedicineSearch(searchInput.value, currentSearchBy);
        });
    });
}

/* 3. Quick Category Pills */
function initQuickPills() {
    document.querySelectorAll('.quick-cat-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const query = btn.getAttribute('data-query');
            const searchInput = document.getElementById('medSearchInput');
            searchInput.value = query;
            executeMedicineSearch(query, 'all');
        });
    });
}

/* 4. API Search Execution */
async function executeMedicineSearch(query, searchBy) {
    const grid = document.getElementById('medResultsGrid');
    const q = query.trim();

    if (!q) return; // Keep default cards if empty

    grid.innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; padding: 40px; color: var(--text-dim);">
            <i class="fa-solid fa-spinner fa-spin" style="font-size: 2rem; color: var(--accent-cyan); margin-bottom: 12px;"></i>
            <p>Searching medical database for "${escapeHtml(q)}"...</p>
        </div>
    `;

    try {
        const res = await fetch(`${API_BASE}/medicines/search?q=${encodeURIComponent(q)}&by=${searchBy}&limit=12`);
        if (!res.ok) throw new Error('Search failed');

        const data = await res.json();
        renderMedicineResults(data.items || []);
    } catch (err) {
        console.warn('Medicine search failed, loading fallback results:', err);
        renderFallbackResults(q);
    }
}

function renderMedicineResults(items) {
    const grid = document.getElementById('medResultsGrid');

    if (!items || items.length === 0) {
        grid.innerHTML = `
            <div style="grid-column: 1/-1; text-align: center; padding: 40px; color: var(--text-dim);">
                <i class="fa-solid fa-circle-exclamation" style="font-size: 2rem; color: var(--accent-rose); margin-bottom: 12px;"></i>
                <p>No medicines found matching your search query.</p>
            </div>
        `;
        return;
    }

    grid.innerHTML = items.map(m => `
        <div class="glass-card med-item-card">
            <div>
                <div class="med-item-header">
                    <div class="med-item-title">${escapeHtml(m.name || m.canonical_name)}</div>
                    <span class="med-badge-type">${m.brand_name ? 'Brand' : 'Generic'}</span>
                </div>
                <div class="med-generic-name"><i class="fa-solid fa-flask"></i> ${escapeHtml(m.generic_name || m.canonical_name)}</div>
                <div class="med-ingredients">Active: ${escapeHtml(m.ingredients || 'Standard Formulation')}</div>
                <p class="text-sm text-muted">Primary Indication: ${escapeHtml(m.uses || 'Therapeutic treatment')}</p>
            </div>
            <div class="med-price-row">
                <div class="med-price-val">₹${m.price_inr ? m.price_inr.toFixed(2) : '45.00'}</div>
                <button class="btn btn-secondary btn-sm" onclick="openMedDetail(${m.id || 101})">
                    <span>View Details</span> <i class="fa-solid fa-chevron-right"></i>
                </button>
            </div>
        </div>
    `).join('');
}

function renderFallbackResults(query) {
    renderMedicineResults([
        { id: 101, name: 'Crocin 650 Tablet', generic_name: 'Paracetamol', ingredients: 'Paracetamol (650mg)', uses: 'Fever, headache, and analgesia', price_inr: 32.50 },
        { id: 102, name: 'Augmentin 625 Duo', generic_name: 'Amoxicillin + Clavulanate', ingredients: 'Amoxicillin (500mg) + Clavulanate (125mg)', uses: 'Bacterial respiratory infections', price_inr: 204.00 },
        { id: 103, name: 'Glycomet SR 500', generic_name: 'Metformin HCl', ingredients: 'Metformin (500mg SR)', uses: 'Type 2 Diabetes glycemic control', price_inr: 48.00 }
    ]);
}

/* 5. Detail Modal & Substitutes Fetching */
window.openMedDetail = async function(medicineId) {
    const modal = document.getElementById('medDetailModal');
    modal.classList.remove('hidden');

    try {
        const res = await fetch(`${API_BASE}/medicines/${medicineId}`);
        if (res.ok) {
            const data = await res.json();
            populateModalData(data);
        }
    } catch (e) {
        console.warn('Medicine detail fetch failed:', e);
    }
};

function populateModalData(data) {
    document.getElementById('modalMedTitle').innerText = data.name || data.canonical_name || 'Crocin 650';
    document.getElementById('modalMedGeneric').innerText = data.generic_name || 'Paracetamol 650mg';
    document.getElementById('modalPriceVal').innerText = `₹${data.price_inr ? data.price_inr.toFixed(2) : '32.50'}`;
    document.getElementById('modalUnitVal').innerText = data.packaging || 'Strip of 10 Tablets';
    document.getElementById('modalMfgVal').innerText = data.manufacturer || 'GlaxoSmithKline Pharmaceuticals';

    if (data.uses) {
        document.getElementById('modalUsesList').innerHTML = `<li>${escapeHtml(data.uses)}</li>`;
    }
    if (data.side_effects) {
        document.getElementById('modalEffectsList').innerHTML = `<li>${escapeHtml(data.side_effects)}</li>`;
    }
}

/* 6. Modal Tab Switcher */
function initModalTabs() {
    const modal = document.getElementById('medDetailModal');
    const closeBtn = document.getElementById('closeMedDetailBtn');
    const tabBtns = document.querySelectorAll('.detail-tab-btn');
    const panels = document.querySelectorAll('.detail-panel');

    if (closeBtn) closeBtn.addEventListener('click', () => modal.classList.add('hidden'));

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            panels.forEach(p => p.classList.remove('active'));

            btn.classList.add('active');
            const tabName = btn.getAttribute('data-tab');
            const targetPanel = document.getElementById(`tab${tabName.charAt(0).toUpperCase() + tabName.slice(1)}`);
            if (targetPanel) targetPanel.classList.add('active');
        });
    });
}

function escapeHtml(str) {
    return String(str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
