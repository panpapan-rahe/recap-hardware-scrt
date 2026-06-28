// ========================================
// PERANGKAT PAGE
// ========================================
let cabangList = [];
let kategoriList = [];
let perangkatList = [];
let selectedItem = null;
let riwayatList = [];
let loading = false;

async function init() {
    await loadCabang();
    await loadKategori();
    await loadPerangkat();
}

async function loadCabang() {
    try {
        cabangList = await Auth.api('GET', '/cabang/') || [];
        cabangList.sort((a, b) => (a.kode || '').localeCompare(b.kode || ''));
        populateCabangDropdowns();
    } catch (e) { /* silent */ }
}

async function loadKategori() {
    try {
        kategoriList = await Auth.api('GET', '/kategori/') || [];
        populateKategoriDropdowns();
    } catch (e) { /* silent */ }
}

function populateCabangDropdowns() {
    const filterEl = document.getElementById('filterCabang');
    const formEl = document.getElementById('formCabang');
    const options = cabangList.map(c => `<option value="${c.id}">${c.nama}</option>`).join('');

    if (filterEl) filterEl.innerHTML = '<option value="">Semua Cabang</option>' + options;
    if (formEl) formEl.innerHTML = '<option value="">Pilih Cabang</option>' + options;
}

function populateKategoriDropdowns() {
    const filterEl = document.getElementById('filterKategori');
    const formEl = document.getElementById('formKategori');
    const options = kategoriList.map(k => `<option value="${k.id}">${k.nama}</option>`).join('');

    if (filterEl) filterEl.innerHTML = '<option value="">Semua Kategori</option>' + options;
    if (formEl) formEl.innerHTML = '<option value="">Pilih Kategori</option>' + options;
}

function getNamaCabang(id) {
    if (!id) return '-';
    const c = cabangList.find(x => x.id == id);
    return c ? c.nama : id;
}

function getNamaKategori(id) {
    if (!id) return '-';
    const k = kategoriList.find(x => x.id == id);
    return k ? k.nama : id;
}

async function loadPerangkat() {
    try {
        let url = '/perangkat/';
        const params = [];
        const filterCabang = document.getElementById('filterCabang')?.value;
        const filterKategori = document.getElementById('filterKategori')?.value;
        const filterStatus = document.getElementById('filterStatus')?.value;
        if (filterCabang) params.push('cabang_id=' + filterCabang);
        if (filterKategori) params.push('kategori_id=' + filterKategori);
        if (filterStatus) params.push('status=' + filterStatus);
        if (params.length) url += '?' + params.join('&');

        perangkatList = await Auth.api('GET', url) || [];
        renderTable();
    } catch (e) {
        Auth.showToast('Gagal memuat data perangkat', 'error');
    }
}

function renderTable() {
    const tbody = document.getElementById('perangkatTable');
    const emptyMsg = document.getElementById('emptyMsg');

    if (perangkatList.length === 0) {
        tbody.innerHTML = '';
        emptyMsg.style.display = 'block';
        return;
    }
    emptyMsg.style.display = 'none';

    tbody.innerHTML = perangkatList.map(item => `
        <tr>
            <td>${item.kode_unik}</td>
            <td>${item.nama}</td>
            <td>${(item.merk || '') + ' ' + (item.model || '')}</td>
            <td>${getNamaKategori(item.kategori_id)}</td>
            <td>${getNamaCabang(item.cabang_id)}</td>
            <td><span class="badge badge-${item.status}">${item.status}</span></td>
            <td class="col-actions">
                <button onclick="detailPerangkat(${item.id})" class="btn btn-sm btn-secondary">Detail</button>
                <button onclick="editItem(${item.id})" class="btn btn-sm btn-warning">Edit</button>
                <button onclick="deleteItem(${item.id})" class="btn btn-sm btn-danger">Hapus</button>
            </td>
        </tr>
    `).join('');
}

function openModal() {
    document.getElementById('perangkatModal').style.display = 'flex';
    document.getElementById('modalTitle').textContent = 'Tambah Perangkat';
    document.getElementById('perangkatForm').reset();
    document.getElementById('editId').value = '';
    document.getElementById('formStatus').value = 'aktif';
    document.getElementById('formKategori').value = '';
}

function editItem(id) {
    const item = perangkatList.find(x => x.id === id);
    if (!item) return;
    document.getElementById('perangkatModal').style.display = 'flex';
    document.getElementById('modalTitle').textContent = 'Edit Perangkat';
    document.getElementById('editId').value = item.id;
    document.getElementById('formCabang').value = item.cabang_id;
    document.getElementById('formKategori').value = item.kategori_id || '';
    document.getElementById('formStatus').value = item.status;
    document.getElementById('formMerk').value = item.merk || '';
    document.getElementById('formType').value = item.model || '';
    document.getElementById('formSN').value = item.serial_number || '';
    document.getElementById('formAdjuro').value = item.adjuro || '';
    document.getElementById('formLokasi').value = item.lokasi_detail || '';
}

function closeModal() {
    document.getElementById('perangkatModal').style.display = 'none';
}

async function saveItem() {
    const editId = document.getElementById('editId').value;
    const body = {
        cabang_id: parseInt(document.getElementById('formCabang').value),
        kategori_id: document.getElementById('formKategori').value ? parseInt(document.getElementById('formKategori').value) : null,
        status: document.getElementById('formStatus').value,
        merk: document.getElementById('formMerk').value.trim(),
        model: document.getElementById('formType').value.trim(),
        serial_number: document.getElementById('formSN').value.trim(),
        adjuro: document.getElementById('formAdjuro').value.trim(),
        lokasi_detail: document.getElementById('formLokasi').value.trim()
    };

    if (!body.cabang_id) {
        Auth.showToast('Pilih Cabang terlebih dahulu', 'error');
        return;
    }
    if (!body.merk) {
        Auth.showToast('Isi Merek terlebih dahulu', 'error');
        return;
    }
    if (!body.model) {
        Auth.showToast('Isi Type terlebih dahulu', 'error');
        return;
    }

    loading = true;
    document.getElementById('saveBtn').textContent = 'Menyimpan...';

    try {
        if (editId) {
            await Auth.api('PUT', '/perangkat/' + editId, body);
            Auth.showToast('Data berhasil diupdate', 'success');
        } else {
            await Auth.api('POST', '/perangkat/', body);
            Auth.showToast('Data berhasil ditambahkan', 'success');
        }
        closeModal();
        loadPerangkat();
    } catch (e) {
        Auth.showToast(e.message, 'error');
    } finally {
        loading = false;
        document.getElementById('saveBtn').textContent = 'Simpan';
    }
}

async function deleteItem(id) {
    if (!confirm('Yakin ingin menghapus data ini?')) return;
    try {
        await Auth.api('DELETE', '/perangkat/' + id);
        Auth.showToast('Data berhasil dihapus', 'success');
        loadPerangkat();
    } catch (e) {
        Auth.showToast(e.message, 'error');
    }
}

// DETAIL
async function detailPerangkat(id) {
    const item = perangkatList.find(x => x.id === id);
    if (!item) return;
    selectedItem = item;

    document.getElementById('detailModal').style.display = 'flex';

    document.getElementById('detailTable').innerHTML = `
        <tr><td><strong>Kode Unik</strong></td><td>${item.kode_unik}</td></tr>
        <tr><td><strong>Nama</strong></td><td>${item.nama}</td></tr>
        <tr><td><strong>Merk</strong></td><td>${item.merk || '-'}</td></tr>
        <tr><td><strong>Type</strong></td><td>${item.model || '-'}</td></tr>
        <tr><td><strong>Kategori</strong></td><td>${getNamaKategori(item.kategori_id)}</td></tr>
        <tr><td><strong>Adjuro</strong></td><td>${item.adjuro || '-'}</td></tr>
        <tr><td><strong>Serial Number</strong></td><td>${item.serial_number || '-'}</td></tr>
        <tr><td><strong>Cabang</strong></td><td>${getNamaCabang(item.cabang_id)}</td></tr>
        <tr><td><strong>Lokasi</strong></td><td>${item.lokasi_detail || '-'}</td></tr>
        <tr><td><strong>Status</strong></td><td><span class="badge badge-${item.status}">${item.status}</span></td></tr>
    `;

    const isMutasiRetired = item.status === 'mutasi' || item.status === 'retired';
    document.getElementById('activityActions').style.display = isMutasiRetired ? 'none' : 'block';
    document.getElementById('btnPinjam').style.display = item.status === 'aktif' ? '' : 'none';
    document.getElementById('btnKembalikan').style.display = item.status === 'dipinjam' ? '' : 'none';
    document.getElementById('btnMaintenance').style.display = item.status === 'aktif' ? '' : 'none';
    document.getElementById('btnSelesaiMaintenance').style.display = item.status === 'maintenance' ? '' : 'none';

    try {
        riwayatList = await Auth.api('GET', '/aktivitas/perangkat/' + id) || [];
        renderRiwayat();
    } catch {
        riwayatList = [];
        renderRiwayat();
    }
}

function renderRiwayat() {
    const tbody = document.getElementById('riwayatTableBody');
    const emptyMsg = document.getElementById('riwayatEmpty');

    if (riwayatList.length === 0) {
        tbody.innerHTML = '';
        emptyMsg.style.display = 'block';
        return;
    }
    emptyMsg.style.display = 'none';

    tbody.innerHTML = riwayatList.map(a => `
        <tr>
            <td>${Auth.formatDate(a.created_at)}</td>
            <td><span class="badge badge-${a.tipe === 'tambah' ? 'success' : a.tipe === 'hapus' ? 'danger' : 'warning'}">${a.tipe}</span></td>
            <td>${a.deskripsi || '-'}</td>
            <td>${a.user_id || '-'}</td>
        </tr>
    `).join('');
}

function closeDetailModal() {
    document.getElementById('detailModal').style.display = 'none';
    selectedItem = null;
}

// AKTIVITAS
function openActivityModal(type) {
    const titles = { pindah: 'Pindah Cabang', pinjam: 'Pinjamkan Perangkat', maintenance: 'Masuk Maintenance' };
    document.getElementById('activityTitle').textContent = titles[type] || 'Aktivitas';
    document.getElementById('activityType').value = type;

    const fieldsEl = document.getElementById('activityFields');
    if (type === 'pindah') {
        const options = cabangList.filter(c => c.id != selectedItem.cabang_id)
            .map(c => `<option value="${c.id}">${c.nama}</option>`).join('');
        fieldsEl.innerHTML = `<div class="form-group"><label>Cabang Tujuan</label><select id="activityCabangTujuan" class="form-control" required><option value="">Pilih Cabang</option>${options}</select></div>`;
    } else if (type === 'pinjam') {
        fieldsEl.innerHTML = `<div class="form-group"><label>Nama Peminjam</label><input type="text" id="activityPeminjam" class="form-control" placeholder="Siapa yang meminjam?" required></div>`;
    } else {
        fieldsEl.innerHTML = '';
    }

    document.getElementById('activityModal').style.display = 'flex';
}

function closeActivityModal() {
    document.getElementById('activityModal').style.display = 'none';
}

async function submitActivity() {
    const type = document.getElementById('activityType').value;
    const deskripsi = document.getElementById('activityDeskripsi').value.trim();
    let body = { deskripsi };

    if (type === 'pindah') {
        body.cabang_tujuan_id = parseInt(document.getElementById('activityCabangTujuan').value);
        if (!body.cabang_tujuan_id) { Auth.showToast('Pilih cabang tujuan', 'error'); return; }
    } else if (type === 'pinjam') {
        body.peminjam = document.getElementById('activityPeminjam').value.trim();
        if (!body.peminjam) { Auth.showToast('Isi nama peminjam', 'error'); return; }
    }

    try {
        await Auth.api('POST', '/perangkat/' + selectedItem.id + '/' + type, body);
        Auth.showToast('Aktivitas berhasil dicatat', 'success');
        closeActivityModal();
        closeDetailModal();
        loadPerangkat();
    } catch (e) {
        Auth.showToast(e.message, 'error');
    }
}

async function kembalikan() {
    if (!confirm('Yakin ingin mengembalikan perangkat ini?')) return;
    try {
        await Auth.api('POST', '/perangkat/' + selectedItem.id + '/kembalikan', {});
        Auth.showToast('Perangkat berhasil dikembalikan', 'success');
        closeDetailModal();
        loadPerangkat();
    } catch (e) {
        Auth.showToast(e.message, 'error');
    }
}

async function selesaiMaintenance() {
    if (!confirm('Maintenance sudah selesai?')) return;
    try {
        await Auth.api('POST', '/perangkat/' + selectedItem.id + '/selesai-maintenance', {});
        Auth.showToast('Maintenance selesai, perangkat aktif kembali', 'success');
        closeDetailModal();
        loadPerangkat();
    } catch (e) {
        Auth.showToast(e.message, 'error');
    }
}

// Form listeners
document.getElementById('perangkatForm').addEventListener('submit', function(e) {
    e.preventDefault();
    saveItem();
});

document.getElementById('activityForm').addEventListener('submit', function(e) {
    e.preventDefault();
    submitActivity();
});

document.addEventListener('DOMContentLoaded', init);
