"""Append drop shadows, 3-card grid, liquid glass, emoji utilities, and em dash styles."""

enhancements = """
/* ==========================================================================
   ENHANCEMENT 2: DROP SHADOWS, 3-CARD GRID, LIQUID GLASS, EMOJIS, EM DASHES
   ========================================================================== */

/* ─── DROP SHADOWS ─── */
.shadow-drop-sm {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}
.shadow-drop-md {
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}
.shadow-drop-lg {
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
}
.shadow-drop-xl {
    box-shadow: 0 16px 48px rgba(0, 0, 0, 0.3);
}
.shadow-drop-2xl {
    box-shadow: 0 24px 64px rgba(0, 0, 0, 0.4);
}
.shadow-drop-colored {
    box-shadow: 0 8px 32px rgba(128, 0, 255, 0.2), 0 4px 16px rgba(0, 0, 0, 0.15);
}
.shadow-drop-rainbow {
    box-shadow: 
        0 4px 16px rgba(255, 0, 64, 0.15),
        0 8px 32px rgba(0, 255, 128, 0.1),
        0 12px 48px rgba(0, 128, 255, 0.1);
}

/* Hover lift with shadow */
.shadow-hover-lift {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.shadow-hover-lift:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
}

/* ─── 3 FEATURE CARDS IN ROW ─── */
.features-3-col {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
    width: 100%;
}

.features-3-col .feature-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 32px 24px;
    border-radius: var(--radius-lg);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.features-3-col .feature-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 16px 48px rgba(0, 0, 0, 0.25);
}

.features-3-col .feature-icon {
    width: 64px;
    height: 64px;
    border-radius: var(--radius-full);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 16px;
    font-size: 28px;
}

.features-3-col .feature-title {
    font-size: 1.125rem;
    font-weight: 700;
    margin-bottom: 8px;
}

.features-3-col .feature-desc {
    font-size: 0.875rem;
    opacity: 0.8;
    line-height: 1.6;
}

/* Responsive: 2 columns on tablet, 1 on mobile */
@media (max-width: 1024px) {
    .features-3-col {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 640px) {
    .features-3-col {
        grid-template-columns: 1fr;
    }
}

/* ─── LIQUID GLASS EFFECT ─── */
.liquid-glass {
    background: linear-gradient(
        135deg,
        rgba(255, 255, 255, 0.12) 0%,
        rgba(255, 255, 255, 0.05) 50%,
        rgba(255, 255, 255, 0.12) 100%
    );
    backdrop-filter: blur(20px) saturate(1.8);
    -webkit-backdrop-filter: blur(20px) saturate(1.8);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: var(--radius-lg);
    box-shadow: 
        0 8px 32px rgba(0, 0, 0, 0.1),
        inset 0 1px 0 rgba(255, 255, 255, 0.2),
        inset 0 -1px 0 rgba(0, 0, 0, 0.05);
    position: relative;
    overflow: hidden;
}

/* Liquid glass shine/reflection effect */
.liquid-glass::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 50%;
    height: 100%;
    background: linear-gradient(
        90deg,
        transparent 0%,
        rgba(255, 255, 255, 0.1) 50%,
        transparent 100%
    );
    transition: left 0.6s ease;
}

.liquid-glass:hover::before {
    left: 100%;
}

/* Light theme liquid glass */
[data-theme="light"] .liquid-glass {
    background: linear-gradient(
        135deg,
        rgba(255, 255, 255, 0.85) 0%,
        rgba(255, 255, 255, 0.7) 50%,
        rgba(255, 255, 255, 0.85) 100%
    );
    backdrop-filter: blur(20px) saturate(1.5);
    -webkit-backdrop-filter: blur(20px) saturate(1.5);
    border: 1px solid rgba(255, 255, 255, 0.6);
    box-shadow: 
        0 8px 32px rgba(0, 0, 0, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.8),
        inset 0 -1px 0 rgba(0, 0, 0, 0.05);
}

/* Liquid glass button */
.btn-liquid-glass {
    background: linear-gradient(
        135deg,
        rgba(255, 255, 255, 0.15) 0%,
        rgba(255, 255, 255, 0.05) 100%
    );
    backdrop-filter: blur(16px) saturate(1.8);
    -webkit-backdrop-filter: blur(16px) saturate(1.8);
    border: 1px solid rgba(255, 255, 255, 0.25);
    border-radius: var(--radius-full);
    padding: 12px 28px;
    color: inherit;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.btn-liquid-glass:hover {
    background: linear-gradient(
        135deg,
        rgba(255, 255, 255, 0.25) 0%,
        rgba(255, 255, 255, 0.1) 100%
    );
    border-color: rgba(255, 255, 255, 0.4);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

/* Liquid glass navbar */
.navbar-liquid {
    background: linear-gradient(
        135deg,
        rgba(10, 10, 10, 0.7) 0%,
        rgba(20, 10, 40, 0.6) 50%,
        rgba(10, 10, 10, 0.7) 100%
    );
    backdrop-filter: blur(24px) saturate(1.5);
    -webkit-backdrop-filter: blur(24px) saturate(1.5);
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

[data-theme="light"] .navbar-liquid {
    background: linear-gradient(
        135deg,
        rgba(255, 255, 255, 0.8) 0%,
        rgba(248, 248, 255, 0.75) 50%,
        rgba(255, 255, 255, 0.8) 100%
    );
    backdrop-filter: blur(24px) saturate(1.5);
    -webkit-backdrop-filter: blur(24px) saturate(1.5);
    border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

/* ─── EMOJI UTILITIES ─── */
.emoji-icon {
    font-size: 1.5rem;
    line-height: 1;
    display: inline-block;
    vertical-align: middle;
    filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
}

.emoji-large {
    font-size: 3rem;
    line-height: 1;
    display: block;
    text-align: center;
    margin-bottom: 12px;
    animation: emoji-bounce 2s ease-in-out infinite;
}

.emoji-pulse {
    animation: emoji-pulse 1.5s ease-in-out infinite;
}

@keyframes emoji-bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-6px); }
}

@keyframes emoji-pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.15); }
}

/* Emoji in card icon position */
.emoji-card-icon {
    font-size: 2.5rem;
    margin-bottom: 16px;
    display: block;
    text-align: center;
}

/* ─── EM DASH TYPOGRAPHY ─── */
.em-dash-list li::before {
    content: '— ';
    opacity: 0.7;
}

.em-dash-separator {
    display: inline-block;
    margin: 0 8px;
    opacity: 0.5;
}

/* Em dash heading style */
.em-dash-heading::after {
    content: ' —';
    opacity: 0.6;
}

.em-dash-heading::before {
    content: '— ';
    opacity: 0.6;
}

/* ─── COMBINED UTILITIES ─── */
/* Feature card with all enhancements */
.feature-card-enhanced {
    @extend .liquid-glass;
    @extend .shadow-drop-md;
    @extend .shadow-hover-lift;
}

.feature-card-enhanced {
    background: linear-gradient(
        135deg,
        rgba(255, 255, 255, 0.1) 0%,
        rgba(255, 255, 255, 0.05) 50%,
        rgba(255, 255, 255, 0.1) 100%
    );
    backdrop-filter: blur(20px) saturate(1.8);
    -webkit-backdrop-filter: blur(20px) saturate(1.8);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: var(--radius-lg);
    padding: 32px 24px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.feature-card-enhanced:hover {
    transform: translateY(-8px);
    box-shadow: 0 16px 48px rgba(0, 0, 0, 0.25);
    border-color: rgba(255, 255, 255, 0.3);
}

[data-theme="light"] .feature-card-enhanced {
    background: linear-gradient(
        135deg,
        rgba(255, 255, 255, 0.9) 0%,
        rgba(248, 248, 255, 0.85) 50%,
        rgba(255, 255, 255, 0.9) 100%
    );
    border: 1px solid rgba(0, 0, 0, 0.06);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

[data-theme="light"] .feature-card-enhanced:hover {
    box-shadow: 0 16px 48px rgba(0, 0, 0, 0.12);
    border-color: rgba(0, 0, 0, 0.1);
}

/* 3-column grid with liquid glass feature cards */
.features-grid-liquid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
    width: 100%;
}

.features-grid-liquid .feature-card-enhanced {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
}

@media (max-width: 1024px) {
    .features-grid-liquid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 640px) {
    .features-grid-liquid {
        grid-template-columns: 1fr;
    }
}
"""

# Read current styles.css
css_path = "frontend/styles.css"
with open(css_path, 'r', encoding='utf-8') as f:
    current = f.read()

# Append
with open(css_path, 'a', encoding='utf-8') as f:
    f.write("\n" + enhancements + "\n")

print(f"Appended {len(enhancements)} bytes to styles.css")
print(f"Total lines now: {len(current.splitlines())}")
