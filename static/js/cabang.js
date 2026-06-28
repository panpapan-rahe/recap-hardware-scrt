// ========================================
// CABANG PAGE
// ========================================
let cabangList = [];
let loading = false;

async function init() {
    await loadCabang();
}

async function loadCabang() {
    try {
        cabangList = await Auth.api('GET', '/cabang/') || [];
        cabangList.sort((a, b) => (a.kode || '').localeCompare(b.kode || ''));
        renderTable();
    } catch (e) {
        Auth.showToast('Gagal memuat data cabang', 'error');
    }
}

function renderTable() {
    const tbody = document.getElementById('cabangTable');
    const emptyMsg = document.getElementById('emptyMsg');

    if (cabangList.length === 0) {
        tbody.innerHTML = '';
        emptyMsg.style.display = 'block';
        return;
    }
    emptyMsg.style.display = 'none';

    tbody.innerHTML = cabangList.map((item, i) => `
        <tr>
            <td>${i + 1}</td>
            <td>${item.kode}</td>
            <td>${item.inisial || '-'}</td>
            <td>${item.nama}</td>
            <td>${item.alamat || '-'}</td>
            <td class="col-actions">
                <button onclick="editItem(${item.id})" class="btn btn-sm btn-warning">Edit</button>
                <button onclick="deleteItem(${item.id})" class="btn btn-sm btn-danger">Hapus</button>
            </td>
        </tr>
    `).join('');
}

function openModal() {
    document.getElementById('cabangModal').style.display = 'flex';
    document.getElementById('modalTitle').textContent = 'Tambah Cabang';
    document.getElementById('cabangForm').reset();
    document.getElementById('editId').value = '';
}

function editItem(id) {
    const item = cabangList.find(x => x.id === id);
    if (!item) return;
    document.getElementById('cabangModal').style.display = 'flex';
    document.getElementById('modalTitle').textContent = 'Edit Cabang';
    document.getElementById('editId').value = item.id;
    document.getElementById('formNama').value = item.nama;
    document.getElementById('formKode').value = item.kode;
    document.getElementById('formInisial').value = item.inisial || '';
    document.getElementById('formAlamat').value = item.alamat || '';
}

function closeModal() {
    document.getElementById('cabangModal').style.display = 'none';
}

async function saveItem() {
    const editId = document.getElementById('editId').value;
    const body = {
        nama: document.getElementById('formNama').value.trim(),
        kode: document.getElementById('formKode').value.trim(),
        inisial: document.getElementById('formInisial').value.trim(),
        alamat: document.getElementById('formAlamat').value.trim()
    };

    if (!body.nama || !body.kode) {
        Auth.showToast('Nama dan Kode Cabang wajib diisi', 'error');
        return;
    }

    loading = true;
    document.getElementById('saveBtn').textContent = 'Menyimpan...';

    try {
        if (editId) {
            await Auth.api('PUT', '/cabang/' + editId, body);
            Auth.showToast('Data berhasil diupdate', 'success');
        } else {
            await Auth.api('POST', '/cabang/', body);
            Auth.showToast('Data berhasil ditambahkan', 'success');
        }
        closeModal();
        loadCabang();
    } catch (e) {
        Auth.showToast(e.message, 'error');
    } finally {
        loading = false;
        document.getElementById('saveBtn').textContent = 'Simpan';
    }
}

async function deleteItem(id) {
    if (!confirm('Yakin ingin menghapus cabang ini?')) return;
    try {
        await Auth.api('DELETE', '/cabang/' + id);
        Auth.showToast('Data berhasil dihapus', 'success');
        loadCabang();
    } catch (e) {
        Auth.showToast(e.message, 'error');
    }
}

document.getElementById('cabangForm').addEventListener('submit', function(e) {
    e.preventDefault();
    saveItem();
});

document.addEventListener('DOMContentLoaded', init);
