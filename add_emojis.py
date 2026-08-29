"""Add emoji decorations and em-dash auto-apply script to all HTML files."""
import os
import glob

frontend_dir = "frontend"
html_files = glob.glob(os.path.join(frontend_dir, "*.html"))

emoji_js = '''    <!-- Emoji & Em-Dash Enhancement -->
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Add em-dash list styling to all ul/ol lists
            document.querySelectorAll('ul, ol').forEach(function(list) {
                if (!list.classList.contains('em-dash-list')) {
                    list.classList.add('em-dash-list');
                }
            });
            
            // Add drop shadow to all cards
            document.querySelectorAll('.glass-card, .card, .metric-card, .stat-card, .feature-card').forEach(function(card) {
                if (!card.classList.contains('shadow-drop-md')) {
                    card.classList.add('shadow-drop-md');
                }
                if (!card.classList.contains('shadow-hover-lift')) {
                    card.classList.add('shadow-hover-lift');
                }
            });
            
            // Add liquid glass to glass cards
            document.querySelectorAll('.glass-card').forEach(function(card) {
                if (!card.classList.contains('liquid-glass')) {
                    card.classList.add('liquid-glass');
                }
            });
            
            // Add features-3-col to sections with 3+ cards
            document.querySelectorAll('.features-grid, .grid-3, .row').forEach(function(grid) {
                const cards = grid.querySelectorAll('.glass-card, .card, .metric-card, .stat-card');
                if (cards.length >= 3) {
                    grid.classList.add('features-3-col');
                }
            });
            
            // Add emoji decorations to section headings based on keywords
            const emojiMap = {
                'AI': '\\U0001F916',
                'Clinical': '\\U0001FA7A',
                'Medical': '\\U0001F3E5',
                'Health': '\\U0001F49A',
                'Diagnostic': '\\U0001F52C',
                'Emergency': '\\U0001F6A8',
                'Dashboard': '\\U0001F4CA',
                'Settings': '\\U0002699\\UFE0F',
                'Profile': '\\U0001F464',
                'Report': '\\U0001F4C4',
                'Medicine': '\\U0001F48A',
                'Drug': '\\U0001F48A',
                'Chat': '\\U0001F4AC',
                'History': '\\U0001F550',
                'Notification': '\\U0001F514',
                'Admin': '\\U0001F451',
                'Security': '\\U0001F6E1\\UFE0F',
                'Performance': '\\U00026A1',
                'Accessibility': '\\U000267F',
                'Explainability': '\\U0001F4A1',
                'Feature': '\\U0002B50',
                'Welcome': '\\U0001F44B',
                'Login': '\\U0001F510',
                'Register': '\\U0001F4DD',
                'Home': '\\U0001F3E0',
                'Disease': '\\U0001F9E0',
                'Symptom': '\\U0001FA7A',
                'Treatment': '\\U0001F489',
                'Lab': '\\U0001F9EA',
                'Voice': '\\U0001F399\\UFE0F',
                'Image': '\\U0001F4F7',
                'Document': '\\U0001F4C1',
                'Search': '\\U0001F50D',
                'Results': '\\U0001F4CB',
                'Insights': '\\U0001F4A1',
                'Pipeline': '\\U0001F527',
                'Metrics': '\\U0001F4C8',
                'Safety': '\\U0001F6E1\\UFE0F',
                'Guardrail': '\\U0001F6E1\\UFE0F',
                'Knowledge': '\\U0001F4DA',
                'Reasoning': '\\U0001F9E0',
                'Evidence': '\\U0001F4DA',
                'Guideline': '\\U0001F4D6',
                'Dosage': '\\U0001F48A',
                'Interaction': '\\U00026A0\\UFE0F',
                'Differential': '\\U0001F52C',
                'Confidence': '\\U0001F3AF',
                'Explain': '\\U0001F4A1',
                'Timeline': '\\U0001F550',
                'Analytics': '\\U0001F4CA',
                'Monitoring': '\\U0001F441\\UFE0F',
                'Logs': '\\U0001F4CB',
                'Backup': '\\U0001F4BE',
                'Deploy': '\\U0001F680',
                'Test': '\\U0001F9EA',
                'CI/CD': '\\U0001F504',
                'Docker': '\\U0001F426',
                'Database': '\\U0001F5C4\\UFE0F',
                'API': '\\U0001F50C',
                'Gateway': '\\U0001F310',
                'Cache': '\\U00026A1',
                'Queue': '\\U0001F4E8',
                'Audit': '\\U0001F4DD',
                'User': '\\U0001F464',
                'Role': '\\U0001F3AD',
                'Permission': '\\U0001F510',
                'Session': '\\U0001F511',
                'Token': '\\U0001F3AB',
                'OAuth': '\\U0001F510',
                'Payment': '\\U0001F4B3',
                'Billing': '\\U0001F4B5',
                'Plan': '\\U0001F4E6',
                'Subscription': '\\U0001F4B3',
                'Webhook': '\\U0001F517',
                'Stripe': '\\U0001F4B3'
            };
            
            // Add emojis before matching headings
            document.querySelectorAll('h1, h2, h3').forEach(function(heading) {
                const text = heading.textContent;
                for (const [keyword, emoji] of Object.entries(emojiMap)) {
                    if (text.includes(keyword) && !heading.dataset.emojiAdded) {
                        const span = document.createElement('span');
                        span.className = 'emoji-icon';
                        span.style.marginRight = '8px';
                        span.textContent = emoji;
                        heading.insertBefore(span, heading.firstChild);
                        heading.dataset.emojiAdded = 'true';
                        break;
                    }
                }
            });
        });
    </script>
'''

# Fix the unicode escapes in the JS
emoji_js = emoji_js.replace('\\U0001F916', '\U0001F916')  # robot
emoji_js = emoji_js.replace('\\U0001FA7A', '\U0001FA7A')  # stethoscope
emoji_js = emoji_js.replace('\\U0001F3E5', '\U0001F3E5')  # hospital
emoji_js = emoji_js.replace('\\U0001F49A', '\U0001F49A')  # green heart
emoji_js = emoji_js.replace('\\U0001F52C', '\U0001F52C')  # microscope
emoji_js = emoji_js.replace('\\U0001F6A8', '\U0001F6A8')  # rotating light
emoji_js = emoji_js.replace('\\U0001F4CA', '\U0001F4CA')  # bar chart
emoji_js = emoji_js.replace('\\U0002699\\UFE0F', '\u2699\uFE0F')  # gear
emoji_js = emoji_js.replace('\\U0001F464', '\U0001F464')  # bust in silhouette
emoji_js = emoji_js.replace('\\U0001F4C4', '\U0001F4C4')  # page facing up
emoji_js = emoji_js.replace('\\U0001F48A', '\U0001F48A')  # pill
emoji_js = emoji_js.replace('\\U0001F4AC', '\U0001F4AC')  # speech balloon
emoji_js = emoji_js.replace('\\U0001F550', '\U0001F550')  # clock
emoji_js = emoji_js.replace('\\U0001F514', '\U0001F514')  # bell
emoji_js = emoji_js.replace('\\U0001F451', '\U0001F451')  # crown
emoji_js = emoji_js.replace('\\U0001F6E1\\UFE0F', '\U0001F6E1\uFE0F')  # shield
emoji_js = emoji_js.replace('\\U00026A1', '\u26A1')  # zap
emoji_js = emoji_js.replace('\\U000267F', '\u267F')  # wheelchair
emoji_js = emoji_js.replace('\\U0001F4A1', '\U0001F4A1')  # light bulb
emoji_js = emoji_js.replace('\\U0002B50', '\u2B50')  # star
emoji_js = emoji_js.replace('\\U0001F44B', '\U0001F44B')  # waving hand
emoji_js = emoji_js.replace('\\U0001F510', '\U0001F510')  # locked
emoji_js = emoji_js.replace('\\U0001F4DD', '\U0001F4DD')  # memo
emoji_js = emoji_js.replace('\\U0001F3E0', '\U0001F3E0')  # house
emoji_js = emoji_js.replace('\\U0001F9E0', '\U0001F9E0')  # brain
emoji_js = emoji_js.replace('\\U0001F489', '\U0001F489')  # syringe
emoji_js = emoji_js.replace('\\U0001F9EA', '\U0001F9EA')  # test tube
emoji_js = emoji_js.replace('\\U0001F399\\UFE0F', '\U0001F399\uFE0F')  # microphone
emoji_js = emoji_js.replace('\\U0001F4F7', '\U0001F4F7')  # camera
emoji_js = emoji_js.replace('\\U0001F4C1', '\U0001F4C1')  # folder
emoji_js = emoji_js.replace('\\U0001F50D', '\U0001F50D')  # magnifying glass
emoji_js = emoji_js.replace('\\U0001F4CB', '\U0001F4CB')  # clipboard
emoji_js = emoji_js.replace('\\U0001F527', '\U0001F527')  # wrench
emoji_js = emoji_js.replace('\\U0001F4C8', '\U0001F4C8')  # chart increasing
emoji_js = emoji_js.replace('\\U0001F4D6', '\U0001F4D6')  # open book
emoji_js = emoji_js.replace('\\U0001F4DA', '\U0001F4DA')  # books
emoji_js = emoji_js.replace('\\U0001F441\\UFE0F', '\U0001F441\uFE0F')  # eye
emoji_js = emoji_js.replace('\\U0001F4BE', '\U0001F4BE')  # floppy disk
emoji_js = emoji_js.replace('\\U0001F680', '\U0001F680')  # rocket
emoji_js = emoji_js.replace('\\U0001F504', '\U0001F504')  # counterclockwise arrows
emoji_js = emoji_js.replace('\\U0001F426', '\U0001F426')  # bird (Docker logo approx)
emoji_js = emoji_js.replace('\\U0001F5C4\\UFE0F', '\U0001F5C4\uFE0F')  # card file box
emoji_js = emoji_js.replace('\\U0001F50C', '\U0001F50C')  # electric plug
emoji_js = emoji_js.replace('\\U0001F310', '\U0001F310')  # globe
emoji_js = emoji_js.replace('\\U0001F4E8', '\U0001F4E8')  # incoming envelope
emoji_js = emoji_js.replace('\\U00026A0\\UFE0F', '\u26A0\uFE0F')  # warning
emoji_js = emoji_js.replace('\\U0001F3AD', '\U0001F3AD')  # performing arts
emoji_js = emoji_js.replace('\\U0001F3AB', '\U0001F3AB')  # ticket
emoji_js = emoji_js.replace('\\U0001F4B3', '\U0001F4B3')  # credit card
emoji_js = emoji_js.replace('\\U0001F4B5', '\U0001F4B5')  # dollar banknote
emoji_js = emoji_js.replace('\\U0001F4E6', '\U0001F4E6')  # package
emoji_js = emoji_js.replace('\\U0001F517', '\U0001F517')  # link
emoji_js = emoji_js.replace('\\U0001F3AF', '\U0001F3AF')  # direct hit

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add emoji/enhancement script before </body> (if not already there)
    if 'Emoji & Em-Dash Enhancement' not in content and '</body>' in content:
        content = content.replace('</body>', emoji_js + '</body>')
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated: {os.path.basename(html_file)}")

print(f"\nDone! Updated {len(html_files)} HTML files.")
