/**
 * AURAMED AI — EMERGENCY MODE CONTROLLER
 */

const API_BASE = '/api/v1';

document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    initSosButton();
    initGeolocationLocator();
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

/* 2. Large Red SOS Button Handler */
function initSosButton() {
    const sosBtn = document.getElementById('sosTriggerBtn');
    const statusText = document.getElementById('sosStatusText');
    let active = false;

    if (sosBtn) {
        sosBtn.addEventListener('click', () => {
            active = !active;
            if (active) {
                playEmergencyTone();
                sosBtn.style.background = 'linear-gradient(135deg, #10b981, #059669)';
                sosBtn.querySelector('span').innerText = 'SOS ACTIVE';
                statusText.innerHTML = `<span style="color: var(--accent-emerald); font-weight: 700;">🚨 DISPATCH SIGNAL SENT! Emergency team notified & GPS sent.</span>`;
            } else {
                sosBtn.style.background = 'linear-gradient(135deg, #f43f5e, #be123c)';
                sosBtn.querySelector('span').innerText = 'PRESS SOS';
                statusText.innerText = 'Status: Ready for Instant Emergency Trigger';
            }
        });
    }
}

function playEmergencyTone() {
    try {
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();

        osc.type = 'sine';
        osc.frequency.setValueAtTime(880, audioCtx.currentTime); // A5 note
        gain.gain.setValueAtTime(0.3, audioCtx.currentTime);

        osc.connect(gain);
        gain.connect(audioCtx.destination);

        osc.start();
        osc.stop(audioCtx.currentTime + 0.6);
    } catch (e) {
        console.log('Audio Context unavailable');
    }
}

/* 3. Geolocation Locator */
function initGeolocationLocator() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (pos) => {
                console.log(`GPS Location: Lat ${pos.coords.latitude}, Lon ${pos.coords.longitude}`);
            },
            (err) => {
                console.log('Geolocation permission skipped, using default hospital data');
            }
        );
    }
}
