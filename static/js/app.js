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
        aktivitasList: [],
        riwayatList: [],
        stats: { total: 0, per_cabang: [], per_status: [] },
        filterCabang: '',
        filterKategori: '',
        filterStatus: '',
        filterAktivitasCabang: '',
        filterAktivitasTipe: '',

        // MODAL
        modal: null,
        editMode: null,
        editId: null,
        form: {},
        selectedItem: null,

        // AKTIVITAS
        activityType: null,
        activityTitle: '',
        activityForm: {},

        // REPORT
        reportCabang: '',
        reportKategori: '',
        reportStatus: '',
        reportData: [],

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

        // HELPER
        getNamaCabang(id) {
            if (!id) return '-';
            const c = this.cabangList.find(x => x.id == id);
            return c ? c.nama : id;
        },
        getNamaKategori(id) {
            if (!id) return '-';
            const k = this.kategoriList.find(x => x.id == id);
            return k ? k.nama : id;
        },
        formatDate(d) {
            if (!d) return '-';
            try {
                return new Date(d).toLocaleString('id-ID', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' });
            } catch(e) { return d; }
        },

        // API CALL
        async api(method, url, body = null) {
            const opts = { method, headers: { 'Content-Type': 'application/json' } };
            if (this.token) opts.headers['Authorization'] = 'Bearer ' + this.token;
            if (body) opts.body = JSON.stringify(body);
            const res = await fetch('/api' + url, opts);
            if (res.status === 401) { this.logout(); throw new Error('Unauthorized'); }
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
            } catch (e) { this.loginError = e.message; }
            finally { this.loading = false; }
        },
        async fetchMe() {
            try { this.user = await this.api('GET', '/auth/me'); } catch (e) { this.logout(); }
        },
        logout() {
            this.token = null; this.isLoggedIn = false; this.user = null;
            localStorage.removeItem('token');
        },

        // LOAD DATA
        async loadAll() {
            await Promise.all([this.loadCabang(), this.loadKategori(), this.loadPerangkat(), this.loadDashboard(), this.loadAktivitas()]);
        },
        async loadCabang() {
            try {
                this.cabangList = await this.api('GET', '/cabang/') || [];
                this.cabangList.sort((a, b) => (a.kode || '').localeCompare(b.kode || ''));
            } catch (e) { this.cabangList = []; }
        },
        async loadKategori() { try { this.kategoriList = await this.api('GET', '/kategori/') || []; } catch (e) { this.kategoriList = []; } },
        async loadPerangkat() {
            try {
                let url = '/perangkat/';
                const params = [];
                if (this.filterCabang) params.push('cabang_id=' + this.filterCabang);
                if (this.filterKategori) params.push('kategori_id=' + this.filterKategori);
                if (this.filterStatus) params.push('status=' + this.filterStatus);
                if (params.length) url += '?' + params.join('&');
                this.perangkatList = await this.api('GET', url) || [];
            } catch (e) { this.perangkatList = []; }
        },
        async loadDashboard() {
            try {
                const data = await this.api('GET', '/perangkat/dashboard/stats');
                this.stats = { total: data.total || 0, per_cabang: data.per_cabang || [], per_status: data.per_status || [] };
            } catch (e) { this.stats = { total: 0, per_cabang: [], per_status: [] }; }
        },
        async loadAktivitas() {
            try { this.aktivitasList = await this.api('GET', '/aktivitas/') || []; }
            catch (e) { this.aktivitasList = []; }
        },

        // MODAL
        openModal(type) {
            this.modal = type;
            this.editMode = null;
            this.editId = null;
            this.form = type === 'perangkat' ? { status: 'aktif' } : {};
        },
        editItem(type, item) {
            this.modal = type;
            this.editMode = type;
            this.editId = item.id;
            this.form = Object.assign({}, item);
        },
        closeModal() {
            this.modal = null; this.editMode = null; this.editId = null; this.form = {};
            this.selectedItem = null; this.riwayatList = [];
            this.activityType = null; this.activityForm = {};
        },
        detailPerangkat(item) {
            this.selectedItem = item; this.modal = 'detail';
            this.loadRiwayat(item.id);
        },
        async loadRiwayat(perangkatId) {
            try { this.riwayatList = await this.api('GET', '/aktivitas/perangkat/' + perangkatId) || []; }
            catch (e) { this.riwayatList = []; }
        },

        // CRUD
        async saveItem(type) {
            if (type === 'cabang' && (!this.form.nama || !this.form.kode)) {
                this.showToast('Nama dan Kode Cabang wajib diisi', 'error');
                return;
            }
            this.loading = true;
            try {
                if (this.editMode === type) {
                    await this.api('PUT', '/' + type + '/' + this.editId, this.form);
                    this.showToast('Data berhasil diupdate', 'success');
                } else {
                    await this.api('POST', '/' + type + '/', this.form);
                    this.showToast('Data berhasil ditambahkan', 'success');
                }
                this.closeModal(); this.loadAll();
            } catch (e) { this.showToast(e.message, 'error'); }
            finally { this.loading = false; }
        },
        async deleteItem(type, id) {
            if (!confirm('Yakin ingin menghapus data ini?')) return;
            try { await this.api('DELETE', '/' + type + '/' + id); this.showToast('Data berhasil dihapus', 'success'); this.loadAll(); }
            catch (e) { this.showToast(e.message, 'error'); }
        },

        // AKTIVITAS
        openActivityModal(type) {
            this.activityType = type;
            this.activityForm = {};
            const titles = { pindah: 'Pindah Cabang', pinjam: 'Pinjamkan Perangkat', maintenance: 'Masuk Maintenance' };
            this.activityTitle = titles[type] || 'Aktivitas';
            this.modal = 'activity';
        },
        async submitActivity() {
            this.loading = true;
            try {
                const id = this.selectedItem.id;
                let body = {};
                if (this.activityType === 'pindah') body = { cabang_tujuan_id: this.activityForm.cabang_tujuan_id, deskripsi: this.activityForm.deskripsi };
                else if (this.activityType === 'pinjam') body = { peminjam: this.activityForm.peminjam, deskripsi: this.activityForm.deskripsi };
                else if (this.activityType === 'maintenance') body = { deskripsi: this.activityForm.deskripsi };
                await this.api('POST', '/perangkat/' + id + '/' + this.activityType, body);
                this.showToast('Aktivitas berhasil dicatat', 'success');
                this.closeModal(); this.loadAll();
            } catch (e) { this.showToast(e.message, 'error'); }
            finally { this.loading = false; }
        },
        async kembalikan(id) {
            if (!confirm('Yakin ingin mengembalikan perangkat ini?')) return;
            this.loading = true;
            try { await this.api('POST', '/perangkat/' + id + '/kembalikan', {}); this.showToast('Perangkat berhasil dikembalikan', 'success'); this.closeModal(); this.loadAll(); }
            catch (e) { this.showToast(e.message, 'error'); }
            finally { this.loading = false; }
        },
        async selesaiMaintenance(id) {
            if (!confirm('Maintenance sudah selesai?')) return;
            this.loading = true;
            try { await this.api('POST', '/perangkat/' + id + '/selesai-maintenance', {}); this.showToast('Maintenance selesai, perangkat aktif kembali', 'success'); this.closeModal(); this.loadAll(); }
            catch (e) { this.showToast(e.message, 'error'); }
            finally { this.loading = false; }
        },

        // REPORT
        async applyReportFilter() {
            try {
                let url = '/report/data?';
                const params = [];
                if (this.reportCabang) params.push('cabang_id=' + this.reportCabang);
                if (this.reportKategori) params.push('kategori_id=' + this.reportKategori);
                if (this.reportStatus) params.push('status=' + this.reportStatus);
                url += params.join('&');
                const res = await this.api('GET', url);
                this.reportData = res.data || [];
            } catch (e) { this.showToast(e.message, 'error'); this.reportData = []; }
        },
        async exportCSV() {
            try {
                let url = '/report/export/csv?';
                const params = [];
                if (this.reportCabang) params.push('cabang_id=' + this.reportCabang);
                if (this.reportKategori) params.push('kategori_id=' + this.reportKategori);
                if (this.reportStatus) params.push('status=' + this.reportStatus);
                url += params.join('&');
                const res = await fetch('/api' + url, { headers: { 'Authorization': 'Bearer ' + this.token } });
                const blob = await res.blob();
                const a = document.createElement('a');
                a.href = URL.createObjectURL(blob);
                a.download = 'report_perangkat.csv';
                a.click();
                this.showToast('CSV berhasil diunduh', 'success');
            } catch (e) { this.showToast('Gagal export CSV', 'error'); }
        },
        async exportPDF() {
            try {
                let url = '/report/export/pdf?';
                const params = [];
                if (this.reportCabang) params.push('cabang_id=' + this.reportCabang);
                if (this.reportKategori) params.push('kategori_id=' + this.reportKategori);
                if (this.reportStatus) params.push('status=' + this.reportStatus);
                url += params.join('&');
                const res = await fetch('/api' + url, { headers: { 'Authorization': 'Bearer ' + this.token } });
                const blob = await res.blob();
                const a = document.createElement('a');
                a.href = URL.createObjectURL(blob);
                a.download = 'report_perangkat.pdf';
                a.click();
                this.showToast('PDF berhasil diunduh', 'success');
            } catch (e) { this.showToast('Gagal export PDF', 'error'); }
        },

        // TOAST
        showToast(message, type) {
            this.toast = { show: true, type: type || 'info', message: message };
            setTimeout(function() { this.toast.show = false; }.bind(this), 3000);
        }
    };
}
