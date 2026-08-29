"""Append enhanced CSS to styles.css for harsh gradients, rainbow effects, and improved themes."""

enhanced_css = """
/* ==========================================================================
   ENHANCEMENT: HARSH GRADIENTS, RAINBOW EFFECTS, LUCIDE ICONS, PURE WHITE BG
   ========================================================================== */

/* Lucide Icons */
.lucide {
    width: 1.25em;
    height: 1.25em;
    stroke-width: 2;
    vertical-align: -0.125em;
    display: inline-block;
}

/* Harsh Gradients - Bold High-Contrast Gradient Backgrounds */
.harsh-gradient {
    background: linear-gradient(135deg, #000000 0%, #1a0033 25%, #330066 50%, #003366 75%, #000000 100%) !important;
}

.harsh-gradient-2 {
    background: linear-gradient(135deg, #ff0040 0%, #ff4000 25%, #ff8000 50%, #ffcc00 75%, #ff0040 100%) !important;
}

.harsh-gradient-3 {
    background: linear-gradient(135deg, #00ffff 0%, #0080ff 30%, #8000ff 60%, #ff0080 100%) !important;
}

.harsh-gradient-text {
    background: linear-gradient(90deg, #ff0040, #ff8000, #ffcc00, #00ff80, #00ffff, #8000ff, #ff0080, #ff0040);
    background-size: 200% auto;
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: rainbow-shift 3s linear infinite;
}

/* Rainbow Border Effect */
.rainbow-border {
    position: relative;
    border: none !important;
}
.rainbow-border::before {
    content: '';
    position: absolute;
    inset: 0;
    padding: 2px;
    background: linear-gradient(90deg, #ff0040, #ff8000, #ffcc00, #00ff80, #00ffff, #8000ff, #ff0080);
    background-size: 300% 300%;
    border-radius: inherit;
    animation: rainbow-rotate 3s linear infinite;
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    pointer-events: none;
}

/* Rainbow Glow Effect */
.rainbow-glow {
    box-shadow: 
        0 0 15px rgba(255, 0, 64, 0.3),
        0 0 30px rgba(255, 128, 0, 0.2),
        0 0 45px rgba(255, 204, 0, 0.15),
        0 0 60px rgba(0, 255, 128, 0.1);
}

/* Rainbow Text Animation */
@keyframes rainbow-shift {
    0% { background-position: 0% center; }
    100% { background-position: 200% center; }
}

/* Rainbow Border Rotation */
@keyframes rainbow-rotate {
    0% { background-position: 0% 50%; }
    100% { background-position: 300% 50%; }
}

/* Rainbow Progress Bar */
.rainbow-progress {
    background: linear-gradient(90deg, #ff0040, #ff8000, #ffcc00, #00ff80, #00ffff, #8000ff);
    background-size: 200% auto;
    animation: rainbow-shift 2s linear infinite;
    border-radius: var(--radius-full);
    height: 4px;
}

/* Harsh Dark Theme Override */
[data-theme="dark"] {
    --bg-primary: #000000 !important;
    --bg-secondary: #0a0a0a !important;
    --bg-card: rgba(10, 10, 10, 0.95) !important;
    --bg-card-hover: rgba(20, 20, 20, 0.95) !important;
}

/* Harsh gradient on dark theme cards */
[data-theme="dark"] .glass-card {
    background: linear-gradient(135deg, rgba(10, 10, 10, 0.95) 0%, rgba(20, 0, 40, 0.9) 50%, rgba(10, 10, 10, 0.95) 100%) !important;
    border: 1px solid rgba(128, 0, 255, 0.15) !important;
}

[data-theme="dark"] .glass-card:hover {
    border-color: rgba(128, 0, 255, 0.3) !important;
    box-shadow: 0 0 20px rgba(128, 0, 255, 0.1) !important;
}

/* Pure White Background for Light Theme */
[data-theme="light"] {
    --bg-primary: #ffffff !important;
    --bg-secondary: #ffffff !important;
    --bg-card: rgba(255, 255, 255, 0.98) !important;
    --bg-card-hover: #f8f8f8 !important;
}

/* Harsh gradient on light theme cards */
[data-theme="light"] .glass-card {
    background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 50%, #ffffff 100%) !important;
    border: 1px solid rgba(0, 0, 0, 0.08) !important;
}

/* Rainbow underline for headings */
.rainbow-heading {
    position: relative;
}
.rainbow-heading::after {
    content: '';
    position: absolute;
    bottom: -4px;
    left: 0;
    width: 100%;
    height: 3px;
    background: linear-gradient(90deg, #ff0040, #ff8000, #ffcc00, #00ff80, #00ffff, #8000ff);
    background-size: 200% auto;
    animation: rainbow-shift 2s linear infinite;
    border-radius: 2px;
}

/* Harsh gradient button */
.btn-harsh {
    background: linear-gradient(135deg, #ff0040 0%, #8000ff 50%, #0080ff 100%) !important;
    border: none !important;
    color: #ffffff !important;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.btn-harsh:hover {
    background: linear-gradient(135deg, #ff4060 0%, #a020ff 50%, #2090ff 100%) !important;
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(128, 0, 255, 0.4) !important;
}

/* Rainbow animated icon wrapper */
.rainbow-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(90deg, #ff0040, #ff8000, #ffcc00, #00ff80, #00ffff, #8000ff);
    background-size: 200% auto;
    animation: rainbow-shift 2s linear infinite;
    border-radius: var(--radius-md);
    padding: 8px;
    color: #ffffff;
}
.rainbow-icon i, .rainbow-icon .lucide {
    color: #ffffff;
}

/* Harsh gradient navbar */
.navbar-harsh {
    background: linear-gradient(90deg, #000000 0%, #1a0033 30%, #330066 60%, #000000 100%) !important;
}

/* Light theme harsh navbar */
[data-theme="light"] .navbar-harsh {
    background: linear-gradient(90deg, #ffffff 0%, #f0f0f0 30%, #ffffff 60%, #f0f0f0 100%) !important;
    border-bottom: 2px solid transparent;
    background-clip: padding-box;
    position: relative;
}
[data-theme="light"] .navbar-harsh::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 2px;
    background: linear-gradient(90deg, #ff0040, #ff8000, #ffcc00, #00ff80, #00ffff, #8000ff);
    background-size: 200% auto;
    animation: rainbow-shift 2s linear infinite;
}

/* Rainbow card hover effect */
.card-rainbow-hover:hover {
    border-color: transparent;
    background-clip: padding-box;
    position: relative;
}
.card-rainbow-hover:hover::before {
    content: '';
    position: absolute;
    inset: -2px;
    background: linear-gradient(90deg, #ff0040, #ff8000, #ffcc00, #00ff80, #00ffff, #8000ff, #ff0040);
    background-size: 200% auto;
    animation: rainbow-shift 1.5s linear infinite;
    border-radius: inherit;
    z-index: -1;
    opacity: 0.7;
}

/* Lucide icon sizing fix */
i[data-lucide] {
    width: 1em;
    height: 1em;
}

/* Theme toggle with rainbow */
.theme-toggle-rainbow {
    background: linear-gradient(90deg, #ff0040, #ff8000, #ffcc00, #00ff80, #00ffff, #8000ff);
    background-size: 200% auto;
    animation: rainbow-shift 2s linear infinite;
    border: none;
    border-radius: var(--radius-full);
    padding: 8px 12px;
    cursor: pointer;
}
.theme-toggle-rainbow i, .theme-toggle-rainbow .lucide {
    color: #ffffff;
}
"""

# Read current styles.css
css_path = "frontend/styles.css"
with open(css_path, 'r', encoding='utf-8') as f:
    current = f.read()

# Append
with open(css_path, 'a', encoding='utf-8') as f:
    f.write("\n" + enhanced_css + "\n")

print(f"Appended {len(enhanced_css)} bytes to styles.css")
print(f"Total lines: {len(current.splitlines())}")
