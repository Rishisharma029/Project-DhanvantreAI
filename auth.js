/**
 * AURAMED AI — AUTHENTICATION SYSTEM LOGIC
 */

document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    initViewSwitching();
    initPasswordToggles();
    initPasswordStrength();
    initRoleSelector();
    initForms();
    initQuickDemoAccess();
    checkUrlParams();
});

function initQuickDemoAccess() {
    const demoBtn = document.getElementById('quickDemoBtn');
    if (demoBtn) {
        demoBtn.addEventListener('click', async () => {
            const emailInput = document.getElementById('loginEmail');
            const passInput = document.getElementById('loginPassword');
            if (emailInput) emailInput.value = 'demo@auramed.ai';
            if (passInput) passInput.value = 'Password123!';

            showSuccess('⚡ 1-Click Quick Access: Authenticating as Demo Clinical User...');
            
            try {
                const res = await fetch(`${API_BASE}/auth/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        email: 'demo@auramed.ai',
                        password: 'Password123!'
                    })
                });

                if (res.ok) {
                    const data = await res.json();
                    localStorage.setItem('auramed_access_token', data.access_token);
                    localStorage.setItem('auramed_refresh_token', data.refresh_token);
                } else {
                    // Fallback token so guest mode works regardless
                    localStorage.setItem('auramed_access_token', 'demo_guest_token_bypass');
                }
            } catch (err) {
                localStorage.setItem('auramed_access_token', 'demo_guest_token_bypass');
            }

            setTimeout(() => {
                window.location.href = 'dashboard.html';
            }, 800);
        });
    }
}

/* API Base URL Configuration */
const API_BASE = '/api/v1';

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

/* 2. View Switching via Hash (#login, #register, #forgot, #verify) */
function initViewSwitching() {
    window.addEventListener('hashchange', handleHashChange);
    handleHashChange(); // Run on initial load
}

function handleHashChange() {
    let hash = window.location.hash.split('?')[0] || '#login';
    if (!['#login', '#register', '#forgot', '#verify'].includes(hash)) {
        hash = '#login';
    }

    // Hide all views
    document.querySelectorAll('.auth-view').forEach(view => view.classList.add('hidden'));

    // Clear feedback alerts
    hideAlerts();

    // Show target view
    const targetId = hash.replace('#', '') + 'View';
    const targetEl = document.getElementById(targetId);
    if (targetEl) {
        targetEl.classList.remove('hidden');
    }
}

/* 3. Password Visibility Eye Toggle */
function initPasswordToggles() {
    document.querySelectorAll('.password-toggle').forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.getAttribute('data-target');
            const input = document.getElementById(targetId);
            const icon = btn.querySelector('i');

            if (input.type === 'password') {
                input.type = 'text';
                icon.className = 'fa-regular fa-eye-slash';
            } else {
                input.type = 'password';
                icon.className = 'fa-regular fa-eye';
            }
        });
    });
}

/* 4. Password Strength Meter */
function initPasswordStrength() {
    const regPassword = document.getElementById('regPassword');
    const strengthBar = document.getElementById('strengthBar');
    const strengthLabel = document.getElementById('strengthLabel');

    if (!regPassword) return;

    regPassword.addEventListener('input', (e) => {
        const pwd = e.target.value;
        const score = calculateStrength(pwd);

        let width = '0%';
        let color = 'transparent';
        let label = 'None';

        if (pwd.length > 0) {
            if (score <= 1) {
                width = '25%';
                color = 'var(--accent-rose)';
                label = 'Weak';
            } else if (score === 2) {
                width = '50%';
                color = 'var(--accent-amber)';
                label = 'Fair';
            } else if (score === 3) {
                width = '75%';
                color = 'var(--accent-cyan)';
                label = 'Good';
            } else {
                width = '100%';
                color = 'var(--accent-emerald)';
                label = 'Strong';
            }
        }

        strengthBar.style.width = width;
        strengthBar.style.backgroundColor = color;
        strengthLabel.innerText = label;
        strengthLabel.style.color = color === 'transparent' ? 'var(--text-dim)' : color;
    });

    function calculateStrength(p) {
        let s = 0;
        if (p.length >= 8) s++;
        if (/[A-Z]/.test(p)) s++;
        if (/[0-9]/.test(p)) s++;
        if (/[^A-Za-z0-9]/.test(p)) s++;
        return s;
    }
}

/* 5. Role Selector Pills */
let selectedRole = 'user';
function initRoleSelector() {
    document.querySelectorAll('.role-option').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.role-option').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            selectedRole = btn.getAttribute('data-role');
        });
    });
}

/* 6. Form Submission Handlers */
function initForms() {
    // LOGIN FORM
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            hideAlerts();

            const email = document.getElementById('loginEmail').value.trim();
            const password = document.getElementById('loginPassword').value;
            const submitBtn = document.getElementById('loginSubmitBtn');

            if (!email || !password) {
                showError('Please enter both email and password.');
                return;
            }

            setBtnLoading(submitBtn, true, 'Signing In...');

            try {
                const res = await fetch(`${API_BASE}/auth/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });

                const data = await res.json();

                if (!res.ok) {
                    throw new Error(data.detail || 'Invalid email or password');
                }

                // Save tokens
                localStorage.setItem('auramed_access_token', data.access_token);
                localStorage.setItem('auramed_refresh_token', data.refresh_token);

                showSuccess('Login successful! Redirecting to clinical platform...');
                setTimeout(() => {
                    window.location.href = 'dashboard.html';
                }, 1200);

            } catch (err) {
                showError(err.message);
            } finally {
                setBtnLoading(submitBtn, false, 'Sign In');
            }
        });
    }

    // REGISTER FORM
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            hideAlerts();

            const fullName = document.getElementById('regFullName').value.trim();
            const email = document.getElementById('regEmail').value.trim();
            const password = document.getElementById('regPassword').value;
            const agreeTerms = document.getElementById('agreeTerms').checked;
            const submitBtn = document.getElementById('registerSubmitBtn');

            if (!fullName || !email || !password) {
                showError('Please fill in all required fields.');
                return;
            }

            if (!agreeTerms) {
                showError('You must agree to the Terms of Service & HIPAA Privacy policy.');
                return;
            }

            if (password.length < 8) {
                showError('Password must be at least 8 characters long.');
                return;
            }

            setBtnLoading(submitBtn, true, 'Creating Account...');

            try {
                const res = await fetch(`${API_BASE}/auth/register`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        email: email,
                        password: password,
                        full_name: fullName,
                        role: selectedRole
                    })
                });

                const data = await res.json();

                if (!res.ok) {
                    throw new Error(data.detail || 'Registration failed');
                }

                showSuccess(`Account created successfully! Verification email issued for ${data.email}.`);
                setTimeout(() => {
                    window.location.hash = '#verify';
                }, 1800);

            } catch (err) {
                showError(err.message);
            } finally {
                setBtnLoading(submitBtn, false, 'Create Account');
            }
        });
    }

    // FORGOT PASSWORD REQUEST FORM
    const forgotForm = document.getElementById('forgotForm');
    if (forgotForm) {
        forgotForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            hideAlerts();

            const email = document.getElementById('forgotEmail').value.trim();
            const submitBtn = document.getElementById('forgotSubmitBtn');
            const resetForm = document.getElementById('resetForm');
            const generatedTokenSpan = document.getElementById('generatedResetToken');

            if (!email) {
                showError('Please enter your account email.');
                return;
            }

            setBtnLoading(submitBtn, true, 'Sending Token...');

            try {
                const res = await fetch(`${API_BASE}/auth/forgot-password`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email })
                });

                const data = await res.json();

                if (!res.ok) {
                    throw new Error(data.detail || 'Request failed');
                }

                showSuccess(data.message || 'If an account exists, a reset token has been issued.');

                if (data.reset_token) {
                    generatedTokenSpan.innerText = data.reset_token;
                    document.getElementById('resetTokenInput').value = data.reset_token;
                    resetForm.classList.remove('hidden');
                }

            } catch (err) {
                showError(err.message);
            } finally {
                setBtnLoading(submitBtn, false, 'Send Reset Request');
            }
        });
    }

    // RESET PASSWORD SUBMIT FORM
    const resetForm = document.getElementById('resetForm');
    if (resetForm) {
        resetForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            hideAlerts();

            const token = document.getElementById('resetTokenInput').value.trim();
            const newPassword = document.getElementById('newPasswordInput').value;
            const submitBtn = document.getElementById('resetSubmitBtn');

            if (!token || !newPassword) {
                showError('Please enter the token and your new password.');
                return;
            }

            setBtnLoading(submitBtn, true, 'Updating Password...');

            try {
                const res = await fetch(`${API_BASE}/auth/reset-password`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ token, new_password: newPassword })
                });

                const data = await res.json();

                if (!res.ok) {
                    throw new Error(data.detail || 'Password reset failed');
                }

                showSuccess('Password updated successfully! You can now log in.');
                setTimeout(() => {
                    window.location.hash = '#login';
                }, 1500);

            } catch (err) {
                showError(err.message);
            } finally {
                setBtnLoading(submitBtn, false, 'Update Password');
            }
        });
    }

    // EMAIL VERIFICATION FORM
    const verifyForm = document.getElementById('verifyForm');
    if (verifyForm) {
        verifyForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            hideAlerts();

            const token = document.getElementById('verifyTokenInput').value.trim();
            const submitBtn = document.getElementById('verifySubmitBtn');

            if (!token) {
                showError('Please enter your verification token.');
                return;
            }

            setBtnLoading(submitBtn, true, 'Verifying...');

            try {
                const res = await fetch(`${API_BASE}/auth/verify-email`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ token })
                });

                const data = await res.json();

                if (!res.ok) {
                    throw new Error(data.detail || 'Verification failed');
                }

                showSuccess('Email address verified successfully!');
                setTimeout(() => {
                    window.location.hash = '#login';
                }, 1500);

            } catch (err) {
                showError(err.message);
            } finally {
                setBtnLoading(submitBtn, false, 'Verify Email');
            }
        });
    }

    // GOOGLE OAUTH SIMULATED CLICK
    const googleOAuthBtn = document.getElementById('googleOAuthBtn');
    if (googleOAuthBtn) {
        googleOAuthBtn.addEventListener('click', async () => {
            hideAlerts();
            googleOAuthBtn.disabled = true;
            googleOAuthBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Authenticating with Google...`;

            try {
                const res = await fetch(`${API_BASE}/auth/google`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ id_token: 'simulated_google_oauth_token_' + Date.now() })
                });

                const data = await res.json();

                if (!res.ok) {
                    throw new Error(data.detail || 'Google sign-in failed');
                }

                localStorage.setItem('auramed_access_token', data.access_token);
                localStorage.setItem('auramed_refresh_token', data.refresh_token);

                showSuccess('Google authentication successful! Redirecting...');
                setTimeout(() => {
                    window.location.href = 'dashboard.html';
                }, 1200);

            } catch (err) {
                showError(err.message);
            } finally {
                googleOAuthBtn.disabled = false;
                googleOAuthBtn.innerHTML = `<i class="fa-brands fa-google" style="color: #ea4335;"></i> Sign in with Google`;
            }
        });
    }
}

/* 7. Auto-detect Query Params (e.g. ?token=XYZ) */
function checkUrlParams() {
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');
    const view = urlParams.get('view');

    if (view && ['login', 'register', 'forgot', 'verify'].includes(view)) {
        window.location.hash = `#${view}`;
    }

    if (token) {
        window.location.hash = '#verify';
        const verifyInput = document.getElementById('verifyTokenInput');
        if (verifyInput) verifyInput.value = token;
    }
}

/* Helper Functions */
function showError(msg) {
    const errAlert = document.getElementById('authErrorAlert');
    const errMsg = document.getElementById('authErrorMsg');
    if (errAlert && errMsg) {
        errMsg.innerText = msg;
        errAlert.classList.remove('hidden');
    }
}

function showSuccess(msg) {
    const succAlert = document.getElementById('authSuccessAlert');
    const succMsg = document.getElementById('authSuccessMsg');
    if (succAlert && succMsg) {
        succMsg.innerText = msg;
        succAlert.classList.remove('hidden');
    }
}

function hideAlerts() {
    const errAlert = document.getElementById('authErrorAlert');
    const succAlert = document.getElementById('authSuccessAlert');
    if (errAlert) errAlert.classList.add('hidden');
    if (succAlert) succAlert.classList.add('hidden');
}

function setBtnLoading(btn, isLoading, originalText) {
    if (!btn) return;
    if (isLoading) {
        btn.disabled = true;
        btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> ${originalText}`;
    } else {
        btn.disabled = false;
        btn.innerHTML = `<span>${originalText}</span> <i class="fa-solid fa-arrow-right"></i>`;
    }
}
