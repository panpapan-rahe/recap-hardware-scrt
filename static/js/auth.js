// SHARED AUTH + API HELPER
const Auth = {
    getToken() {
        return localStorage.getItem('token');
    },
    setToken(token) {
        localStorage.setItem('token', token);
    },
    removeToken() {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
    },
    getUser() {
        try { return JSON.parse(localStorage.getItem('user')) || null; }
        catch { return null; }
    },
    setUser(user) {
        localStorage.setItem('user', JSON.stringify(user));
    },
    isLoggedIn() {
        return !!this.getToken();
    },
    isAdmin() {
        const user = this.getUser();
        return user && user.role === 'admin';
    },
    async api(method, url, body = null) {
        const opts = { method, headers: { 'Content-Type': 'application/json' } };
        const token = this.getToken();
        if (token) opts.headers['Authorization'] = 'Bearer ' + token;
        if (body) opts.body = JSON.stringify(body);
        const res = await fetch('/api' + url, opts);
        if (res.status === 401) { this.logout(); throw new Error('Unauthorized'); }
        if (res.status === 403) { throw new Error('Akses ditolak'); }
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Error');
        return data;
    },
    async login(username, password) {
        const opts = { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ username, password }) };
        const res = await fetch('/api/auth/login', opts);
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Login gagal');
        this.setToken(data.access_token);
        await this.fetchMe();
        return data;
    },
    async fetchMe() {
        try { this.setUser(await this.api('GET', '/auth/me')); }
        catch { this.logout(); }
    },
    logout() {
        this.removeToken();
        window.location.href = '/login.html';
    },
    formatDate(d) {
        if (!d) return '-';
        try {
            return new Date(d).toLocaleString('id-ID', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' });
        } catch(e) { return d; }
    },
    showToast(message, type) {
        let toast = document.querySelector('.toast');
        if (!toast) return;
        toast.textContent = message;
        toast.className = 'toast toast-' + (type || 'info');
        toast.classList.add('show');
        clearTimeout(this._toastTimer);
        this._toastTimer = setTimeout(() => toast.classList.remove('show'), 3000);
    }
};

// Redirect to login if not authenticated
document.addEventListener('DOMContentLoaded', () => {
    if (!Auth.isLoggedIn() && !window.location.pathname.includes('login.html')) {
        window.location.href = '/login.html';
    }
});
