// ========================================
// AUTH HELPERS — Recap Hardware
// ========================================
const Auth = (() => {
    const TOKEN_KEY = 'rh_token';
    const USER_KEY = 'rh_user';

    function getToken() {
        return localStorage.getItem(TOKEN_KEY);
    }

    function setToken(token) {
        localStorage.setItem(TOKEN_KEY, token);
    }

    function getUser() {
        try {
            return JSON.parse(localStorage.getItem(USER_KEY));
        } catch {
            return null;
        }
    }

    function setUser(user) {
        localStorage.setItem(USER_KEY, JSON.stringify(user));
    }

    function logout() {
        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem(USER_KEY);
        window.location.href = '/login.html';
    }

    async function api(method, path, body = null) {
        const opts = {
            method,
            headers: {
                'Content-Type': 'application/json',
            }
        };

        const token = getToken();
        if (token) {
            opts.headers['Authorization'] = `Bearer ${token}`;
        }

        if (body) {
            opts.body = JSON.stringify(body);
        }

        const res = await fetch(`/api${path}`, opts);

        if (res.status === 401) {
            logout();
            throw new Error('Sesi habis, silakan login kembali');
        }

        const data = await res.json().catch(() => null);

        if (!res.ok) {
            throw new Error(data?.detail || 'Terjadi kesalahan');
        }

        return data;
    }

    async function fetchMe() {
        const user = await api('GET', '/auth/me');
        setUser(user);
        return user;
    }

    function showToast(message, type = 'info') {
        const container = document.getElementById('toastContainer');
        if (!container) return;

        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        container.appendChild(toast);

        setTimeout(() => {
            if (toast.parentNode) toast.parentNode.removeChild(toast);
        }, 3000);
    }

    function formatDate(dateStr) {
        if (!dateStr) return '-';
        const d = new Date(dateStr);
        const months = ['Jan','Feb','Mar','Apr','Mei','Jun','Jul','Agu','Sep','Okt','Nov','Des'];
        return `${d.getDate()} ${months[d.getMonth()]} ${d.getFullYear()}`;
    }

    function updateSidebar() {
        const user = getUser();
        if (!user) return;

        const initial = document.getElementById('userInitial');
        const name = document.getElementById('userName');
        const role = document.getElementById('userRole');

        if (initial) initial.textContent = (user.username || 'U')[0].toUpperCase();
        if (name) name.textContent = user.nama_lengkap || user.username;
        if (role) role.textContent = user.role;

        // Hide admin-only links for PIC
        const isAdmin = user.role === 'admin';
        document.querySelectorAll('[data-admin-only]').forEach(el => {
            el.style.display = isAdmin ? '' : 'none';
        });
    }

    // Auto-init sidebar on page load
    document.addEventListener('DOMContentLoaded', () => {
        if (window.location.pathname !== '/login.html') {
            updateSidebar();
        }
    });

    return {
        getToken, setToken, getUser, setUser, logout,
        api, fetchMe, showToast, formatDate, updateSidebar
    };
})();
