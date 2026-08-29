"""Add Lucide icons CDN to all HTML files and add rainbow/dark theme enhancements."""
import os
import glob
import re

frontend_dir = "frontend"
html_files = glob.glob(os.path.join(frontend_dir, "*.html"))

# Lucide CDN script tag
lucide_cdn = '    <!-- Lucide Icons -->\n    <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>\n'

# Theme enhancement script
theme_enhancement = '''    <!-- Theme Enhancement: Harsh Gradients, Rainbow, Lucide -->
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Initialize Lucide icons
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
            
            // Add rainbow class to navbar
            const navbar = document.querySelector('.navbar-header, nav');
            if (navbar && !navbar.classList.contains('navbar-harsh')) {
                navbar.classList.add('navbar-harsh');
            }
            
            // Add rainbow heading to main headings
            document.querySelectorAll('h1, h2').forEach(function(h) {
                if (!h.classList.contains('rainbow-heading')) {
                    h.classList.add('rainbow-heading');
                }
            });
            
            // Add theme toggle rainbow button
            const themeBtn = document.getElementById('themeToggleBtn');
            if (themeBtn && !themeBtn.classList.contains('theme-toggle-rainbow')) {
                themeBtn.classList.add('theme-toggle-rainbow');
            }
            
            // Add rainbow border to primary buttons
            document.querySelectorAll('.btn-primary, .btn-hero, .btn-submit, button[type="submit"]').forEach(function(btn) {
                if (!btn.classList.contains('btn-harsh')) {
                    btn.classList.add('btn-harsh');
                }
            });
            
            // Add card rainbow hover to glass cards
            document.querySelectorAll('.glass-card, .card, .metric-card, .stat-card').forEach(function(card) {
                if (!card.classList.contains('card-rainbow-hover')) {
                    card.classList.add('card-rainbow-hover');
                }
            });
            
            // Observe theme changes to update body background
            function updateBodyBg() {
                const theme = document.documentElement.getAttribute('data-theme');
                if (theme === 'light') {
                    document.body.style.backgroundColor = '#ffffff';
                } else {
                    document.body.style.backgroundColor = '#000000';
                }
            }
            
            // Initial
            updateBodyBg();
            
            // Watch for theme changes
            const observer = new MutationObserver(updateBodyBg);
            observer.observe(document.documentElement, {
                attributes: true,
                attributeFilter: ['data-theme']
            });
        });
    </script>
'''

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add Lucide CDN before </head>
    if 'lucide' not in content and '</head>' in content:
        content = content.replace('</head>', lucide_cdn + '</head>')
    
    # Add theme enhancement script before </body>
    if 'Theme Enhancement' not in content and '</body>' in content:
        content = content.replace('</body>', theme_enhancement + '</body>')
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated: {os.path.basename(html_file)}")

print(f"\nDone! Updated {len(html_files)} HTML files.")
