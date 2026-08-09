/**
 * AURAMED AI — LANDING WEBSITE INTERACTIVE APP
 * Powered by modern ES6+ JavaScript
 */

document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    initNavbarScroll();
    initMetricCounters();
    initHeroDemo();
    initPipelineTabs();
    initFaqAccordion();
    initContactForm();
    initMobileMenu();
});

/* ==========================================================================
   1. Theme Toggle (Dark / Light Mode)
   ========================================================================== */
function initThemeToggle() {
    const themeBtn = document.getElementById('themeToggleBtn');
    const themeIcon = document.getElementById('themeIcon');
    const htmlEl = document.documentElement;

    // Load saved theme or default to dark
    const savedTheme = localStorage.getItem('auramed_theme') || 'dark';
    htmlEl.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);

    themeBtn.addEventListener('click', () => {
        const currentTheme = htmlEl.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        htmlEl.setAttribute('data-theme', newTheme);
        localStorage.setItem('auramed_theme', newTheme);
        updateThemeIcon(newTheme);
    });

    function updateThemeIcon(theme) {
        if (theme === 'light') {
            themeIcon.className = 'fa-solid fa-sun';
        } else {
            themeIcon.className = 'fa-solid fa-moon';
        }
    }
}

/* ==========================================================================
   2. Navbar Scroll Shift & Active Section Highlighter
   ========================================================================== */
function initNavbarScroll() {
    const navbar = document.getElementById('navbar');
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('section[id]');

    window.addEventListener('scroll', () => {
        if (window.scrollY > 40) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }

        // Active link scroll spy
        let currentSection = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop - 120;
            const sectionHeight = section.offsetHeight;
            if (window.scrollY >= sectionTop && window.scrollY < sectionTop + sectionHeight) {
                currentSection = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${currentSection}`) {
                link.classList.add('active');
            }
        });
    });
}

/* ==========================================================================
   3. Animated Metric Counters
   ========================================================================== */
function initMetricCounters() {
    const metricElements = document.querySelectorAll('.metric-value');
    let animated = false;

    function countUp() {
        const heroSection = document.getElementById('hero');
        const heroPos = heroSection.getBoundingClientRect().top;
        const screenPos = window.innerHeight;

        if (heroPos < screenPos && !animated) {
            animated = true;
            metricElements.forEach(el => {
                const target = parseFloat(el.getAttribute('data-target'));
                const isPercent = el.innerText.includes('%');
                const isPlus = el.innerText.includes('+');
                const isMs = el.innerText.includes('ms');

                let start = 0;
                const duration = 1800; // ms
                const stepTime = 20;
                const steps = duration / stepTime;
                const increment = target / steps;

                const timer = setInterval(() => {
                    start += increment;
                    if (start >= target) {
                        start = target;
                        clearInterval(timer);
                    }

                    if (isPercent) {
                        el.innerText = start.toFixed(1) + '%';
                    } else if (isPlus) {
                        el.innerText = Math.floor(start).toLocaleString() + '+';
                    } else if (isMs) {
                        el.innerText = '<' + Math.floor(start) + 'ms';
                    } else {
                        el.innerText = Math.floor(start).toLocaleString();
                    }
                }, stepTime);
            });
        }
    }

    window.addEventListener('scroll', countUp);
    countUp(); // Trigger once on load
}

/* ==========================================================================
   4. Hero Interactive Diagnostic Preview Sandbox
   ========================================================================== */
function initHeroDemo() {
    const symptomInput = document.getElementById('symptomInput');
    const runDemoBtn = document.getElementById('runDemoBtn');
    const presetBtns = document.querySelectorAll('.preset-btn');
    const consolePlaceholder = document.getElementById('consolePlaceholder');
    const consoleResult = document.getElementById('consoleResult');

    const demoTag1 = document.getElementById('demoTag1');
    const demoTag2 = document.getElementById('demoTag2');
    const demoTag3 = document.getElementById('demoTag3');

    // Preset quick scenario clicks
    presetBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const symptoms = btn.getAttribute('data-symptoms');
            symptomInput.value = symptoms;
            runAnalysis(symptoms);
        });
    });

    runDemoBtn.addEventListener('click', () => {
        runAnalysis(symptomInput.value);
    });

    function runAnalysis(symptomText) {
        if (!symptomText.trim()) return;

        // Step 1 Highlight
        setStep(1);

        // Hide old result, show loading state
        consoleResult.classList.add('hidden');
        consolePlaceholder.innerHTML = `
            <i class="fa-solid fa-spinner fa-spin" style="font-size: 2.2rem; color: var(--accent-cyan);"></i>
            <p>Processing adaptive symptom graph & safety rules...</p>
        `;

        setTimeout(() => {
            setStep(2);
        }, 500);

        setTimeout(() => {
            setStep(3);
            renderResults(symptomText);
        }, 1100);
    }

    function setStep(stepNum) {
        demoTag1.classList.remove('active');
        demoTag2.classList.remove('active');
        demoTag3.classList.remove('active');

        if (stepNum >= 1) demoTag1.classList.add('active');
        if (stepNum >= 2) demoTag2.classList.add('active');
        if (stepNum >= 3) demoTag3.classList.add('active');
    }

    function renderResults(symptoms) {
        consolePlaceholder.classList.add('hidden');
        consoleResult.classList.remove('hidden');

        // Dynamic result based on text keywords
        const lower = symptoms.toLowerCase();
        let triageHtml = '';
        let diagHtml = '';
        let safetyHtml = '';

        if (lower.includes('fever') || lower.includes('mening') || lower.includes('stiffness')) {
            triageHtml = `<div class="result-severity alert-high"><i class="fa-solid fa-triangle-exclamation"></i> Triage Status: RED (Urgent Neurological Evaluation)</div><div class="confidence-badge">Confidence: 96.5%</div>`;
            diagHtml = `
                <li><strong>Acute Bacterial Meningitis:</strong> Primary Differential (78%)</li>
                <li><strong>Viral Encephalitis:</strong> Secondary Differential (18%)</li>
            `;
            safetyHtml = `Stat lumbar puncture recommended. Empiric IV Ceftriaxone + Dexamethasone indicated.`;
        } else if (lower.includes('diabet') || lower.includes('polyuria') || lower.includes('weight loss')) {
            triageHtml = `<div class="result-severity" style="color: var(--accent-amber); font-weight: 700;"><i class="fa-solid fa-circle-exclamation"></i> Triage Status: AMBER (Endocrine Workup)</div><div class="confidence-badge">Confidence: 94.1%</div>`;
            diagHtml = `
                <li><strong>New-onset Type 1 / Type 2 Diabetes Mellitus:</strong> Primary (85%)</li>
                <li><strong>Diabetic Ketoacidosis (DKA) Risk:</strong> Secondary Rule-out (12%)</li>
            `;
            safetyHtml = `Order STAT Fasting Blood Glucose, HbA1c, and serum ketones. Verified no baseline renal impairment.`;
        } else {
            // Default ACS / Cardiac
            triageHtml = `<div class="result-severity alert-high"><i class="fa-solid fa-triangle-exclamation"></i> Triage Status: RED (Urgent Cardiac Care)</div><div class="confidence-badge">Confidence: 98.2%</div>`;
            diagHtml = `
                <li><strong>Acute Coronary Syndrome (ACS):</strong> High Probability (88%)</li>
                <li><strong>Pulmonary Embolism:</strong> Secondary Differential (10%)</li>
            `;
            safetyHtml = `Verified zero conflict with current medications. Immediate 12-lead ECG & Troponin I panel recommended.`;
        }

        consoleResult.querySelector('.result-header').innerHTML = triageHtml;
        consoleResult.querySelector('.diag-list').innerHTML = diagHtml;
        consoleResult.querySelector('.result-section:nth-child(2) p').innerText = safetyHtml;
    }
}

/* ==========================================================================
   5. How It Works Pipeline Step Tabs
   ========================================================================== */
function initPipelineTabs() {
    const tabs = document.querySelectorAll('.pipeline-tab');
    const panels = document.querySelectorAll('.pipeline-panel');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const step = tab.getAttribute('data-step');

            tabs.forEach(t => t.classList.remove('active'));
            panels.forEach(p => p.classList.remove('active'));

            tab.classList.add('active');
            document.getElementById(`pipelineStep${step}`).classList.add('active');
        });
    });
}

/* ==========================================================================
   6. FAQ Search & Category Accordion
   ========================================================================== */
function initFaqAccordion() {
    const faqItems = document.querySelectorAll('.faq-item');
    const faqSearchInput = document.getElementById('faqSearchInput');
    const categoryBtns = document.querySelectorAll('.faq-category-btn');

    // Accordion expand / collapse
    faqItems.forEach(item => {
        const questionBtn = item.querySelector('.faq-question');
        questionBtn.addEventListener('click', () => {
            const isOpen = item.classList.contains('open');
            
            // Close other items for single accordion mode
            faqItems.forEach(i => i.classList.remove('open'));

            if (!isOpen) {
                item.classList.add('open');
            }
        });
    });

    // Category Filter
    categoryBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            categoryBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const category = btn.getAttribute('data-category');
            filterFaqs(faqSearchInput.value, category);
        });
    });

    // Search Query Filter
    faqSearchInput.addEventListener('input', (e) => {
        const activeCategoryBtn = document.querySelector('.faq-category-btn.active');
        const category = activeCategoryBtn ? activeCategoryBtn.getAttribute('data-category') : 'all';
        filterFaqs(e.target.value, category);
    });

    function filterFaqs(query, category) {
        const q = query.toLowerCase().trim();

        faqItems.forEach(item => {
            const itemCat = item.getAttribute('data-category');
            const questionText = item.querySelector('.faq-question').innerText.toLowerCase();
            const answerText = item.querySelector('.faq-answer').innerText.toLowerCase();

            const matchesCategory = (category === 'all' || itemCat === category);
            const matchesQuery = !q || questionText.includes(q) || answerText.includes(q);

            if (matchesCategory && matchesQuery) {
                item.classList.remove('hidden');
            } else {
                item.classList.add('hidden');
            }
        });
    }
}

/* ==========================================================================
   7. Contact Form Handling & Validation
   ========================================================================== */
function initContactForm() {
    const contactForm = document.getElementById('contactForm');
    const fullName = document.getElementById('fullName');
    const emailAddr = document.getElementById('emailAddr');
    const messageText = document.getElementById('messageText');
    const submitBtn = document.getElementById('submitBtn');
    const successBanner = document.getElementById('successBanner');

    const nameError = document.getElementById('nameError');
    const emailError = document.getElementById('emailError');
    const messageError = document.getElementById('messageError');

    contactForm.addEventListener('submit', (e) => {
        e.preventDefault();
        let isValid = true;

        // Reset errors
        fullName.classList.remove('invalid');
        emailAddr.classList.remove('invalid');
        messageText.classList.remove('invalid');

        nameError.style.display = 'none';
        emailError.style.display = 'none';
        messageError.style.display = 'none';

        // Validate Full Name
        if (!fullName.value.trim()) {
            fullName.classList.add('invalid');
            nameError.style.display = 'block';
            isValid = false;
        }

        // Validate Email
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailAddr.value.trim() || !emailRegex.test(emailAddr.value.trim())) {
            emailAddr.classList.add('invalid');
            emailError.style.display = 'block';
            isValid = false;
        }

        // Validate Message
        if (!messageText.value.trim()) {
            messageText.classList.add('invalid');
            messageError.style.display = 'block';
            isValid = false;
        }

        if (isValid) {
            // Show loading state
            submitBtn.disabled = true;
            submitBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Submitting...`;

            setTimeout(() => {
                contactForm.classList.add('hidden');
                successBanner.classList.remove('hidden');
            }, 1200);
        }
    });
}

/* ==========================================================================
   8. Mobile Navigation Drawer Toggle
   ========================================================================== */
function initMobileMenu() {
    const mobileBtn = document.getElementById('mobileMenuBtn');
    const navMenu = document.getElementById('navMenu');
    const navLinks = document.querySelectorAll('.nav-link');

    if (mobileBtn && navMenu) {
        mobileBtn.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            const icon = mobileBtn.querySelector('i');
            if (navMenu.classList.contains('active')) {
                icon.className = 'fa-solid fa-xmark';
            } else {
                icon.className = 'fa-solid fa-bars';
            }
        });

        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
                mobileBtn.querySelector('i').className = 'fa-solid fa-bars';
            });
        });
    }
}
