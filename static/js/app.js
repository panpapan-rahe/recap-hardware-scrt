function app() {
    return {
        // STATE
        isLoggedIn: false,
        token: null,
        user: null,
        currentPage: 'dashboard',
        loading: false,
        loginError: '',
        loginForm: { username: '', password: '' },

        // DATA
        cabangList: [],
        kategoriList: [],
        perangkatList: [],
        stats: { total: 0, per_cabang: [], per_status: [] },
        filterCabang: '',
        filterKategori: '',
        filterStatus: '',

        // MODAL
        modal: null,
        editMode: null,
        editId: null,
        form: {},
        selectedItem: null,

        // TOAST
        toast: { show: false, type: 'info', message: '' },

        // INIT
        init() {
            this.token = localStorage.getItem('token');
            if (this.token) {
                this.isLoggedIn = true;
                this.fetchMe();
                this.loadAll();
            }
        },

        // API CALL
        async api(method, url, body = null) {
            const opts = {
                method,
                headers: { 'Content-Type': 'application/json' },
            };
            if (this.token) opts.headers['Authorization'] = `Bearer ${this.token}`;
            if (body) opts.body = JSON.stringify(body);
            const res = await fetch(`/api${url}`, opts);
            if (res.status === 401) {
                this.logout();
                throw new Error('Unauthorized');
            }
            const data = await res.json();
            if (!res.ok) throw new Error(data.detail || 'Error');
            return data;
        },

        // AUTH
        async login() {
            this.loading = true;
            this.loginError = '';
            try {
                const data = await this.api('POST', '/auth/login', this.loginForm);
                this.token = data.access_token;
                localStorage.setItem('token', this.token);
                this.isLoggedIn = true;
                await this.fetchMe();
                this.loadAll();
                this.currentPage = 'dashboard';
            } catch (e) {
                this.loginError = e.message;
            } finally {
                this.loading = false;
            }
        },

        async fetchMe() {
            try {
                this.user = await this.api('GET', '/auth/me');
            } catch (e) {
                this.logout();
            }
        },

        logout() {
            this.token = null;
            this.isLoggedIn = false;
            this.user = null;
            localStorage.removeItem('token');
        },

        // LOAD DATA
        async loadAll() {
            await Promise.all([
                this.loadCabang(),
                this.loadKategori(),
                this.loadPerangkat(),
                this.loadDashboard(),
            ]);
        },

        async loadCabang() {
            try { this.cabangList = await this.api('GET', '/cabang/'); } catch (e) {}
        },

        async loadKategori() {
            try { this.kategoriList = await this.api('GET', '/kategori/'); } catch (e) {}
        },

        async loadPerangkat() {
            try {
                let url = '/perangkat/';
                const params = [];
                if (this.filterCabang) params.push(`cabang_id=${this.filterCabang}`);
                if (this.filterKategori) params.push(`kategori_id=${this.filterKategori}`);
                if (this.filterStatus) params.push(`status=${this.filterStatus}`);
                if (params.length) url += '?' + params.join('&');
                this.perangkatList = await this.api('GET', url);
            } catch (e) {}
        },

        async loadDashboard() {
            try { this.stats = await this.api('GET', '/perangkat/dashboard/stats'); } catch (e) {}
        },

        // MODAL
        openModal(type) {
            this.modal = type;
            this.editMode = null;
            this.editId = null;
            this.form = {};
        },

        editItem(type, item) {
            this.modal = type;
            this.editMode = type;
            this.editId = item.id;
            this.form = { ...item };
        },

        closeModal() {
            this.modal = null;
            this.editMode = null;
            this.editId = null;
            this.form = {};
            this.selectedItem = null;
        },

        detailPerangkat(item) {
            this.selectedItem = item;
            this.modal = 'detail';
        },

        // CRUD
        async saveItem(type) {
            this.loading = true;
            try {
                if (this.editMode === type) {
                    await this.api('PUT', `/${type}/${this.editId}`, this.form);
                    this.showToast('Data berhasil diupdate', 'success');
                } else {
                    await this.api('POST', `/${type}/`, this.form);
                    this.showToast('Data berhasil ditambahkan', 'success');
                }
                this.closeModal();
                this.loadAll();
            } catch (e) {
                this.showToast(e.message, 'error');
            } finally {
                this.loading = false;
            }
        },

        async deleteItem(type, id) {
            if (!confirm('Yakin ingin menghapus data ini?')) return;
            try {
                await this.api('DELETE', `/${type}/${id}`);
                this.showToast('Data berhasil dihapus', 'success');
                this.loadAll();
            } catch (e) {
                this.showToast(e.message, 'error');
            }
        },

        // TOAST
        showToast(message, type = 'info') {
            this.toast = { show: true, type, message };
            setTimeout(() => { this.toast.show = false; }, 3000);
        },
    };
}
