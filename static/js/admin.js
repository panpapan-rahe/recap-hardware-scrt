// ========================================
// ADMIN PAGE — Kelola User
// ========================================
let userList = [];
let loading = false;

async function init() {
    await loadUsers();
}

async function loadUsers() {
    try {
        userList = await Auth.api('GET', '/admin/users') || [];
        renderTable();
    } catch (e) {
        Auth.showToast('Gagal memuat data user', 'error');
    }
}

function renderTable() {
    const tbody = document.getElementById('userTable');
    const emptyMsg = document.getElementById('emptyMsg');

    if (userList.length === 0) {
        tbody.innerHTML = '';
        emptyMsg.style.display = 'block';
        return;
    }
    emptyMsg.style.display = 'none';

    tbody.innerHTML = userList.map(u => `
        <tr>
            <td>${u.username}</td>
            <td>${u.nama_lengkap}</td>
            <td><span class="badge badge-${u.role === 'admin' ? 'aktif' : 'warning'}">${u.role}</span></td>
            <td><span class="badge badge-${u.is_active ? 'aktif' : 'retired'}">${u.is_active ? 'Aktif' : 'Nonaktif'}</span></td>
            <td>${Auth.formatDate(u.created_at)}</td>
            <td class="col-actions">
                <button onclick="editItem(${u.id})" class="btn btn-sm btn-warning">Edit</button>
                ${u.username !== 'admin' ? `<button onclick="deleteUser(${u.id})" class="btn btn-sm btn-danger">Hapus</button>` : ''}
            </td>
        </tr>
    `).join('');
}

function openModal() {
    document.getElementById('userModal').style.display = 'flex';
    document.getElementById('modalTitle').textContent = 'Tambah User';
    document.getElementById('userForm').reset();
    document.getElementById('editId').value = '';
    document.getElementById('formRole').value = 'PIC';
    document.getElementById('formStatus').value = 'true';
    document.getElementById('passwordRequired').style.display = '';
    document.getElementById('formPassword').required = true;
}

function editItem(id) {
    const user = userList.find(x => x.id === id);
    if (!user) return;
    document.getElementById('userModal').style.display = 'flex';
    document.getElementById('modalTitle').textContent = 'Edit User';
    document.getElementById('editId').value = user.id;
    document.getElementById('formUsername').value = user.username;
    document.getElementById('formNama').value = user.nama_lengkap;
    document.getElementById('formRole').value = user.role;
    document.getElementById('formStatus').value = String(user.is_active);
    document.getElementById('formPassword').value = '';
    document.getElementById('passwordRequired').style.display = 'none';
    document.getElementById('formPassword').required = false;
}

function closeModal() {
    document.getElementById('userModal').style.display = 'none';
}

async function saveItem() {
    const editId = document.getElementById('editId').value;
    const username = document.getElementById('formUsername').value.trim();
    const password = document.getElementById('formPassword').value;
    const nama = document.getElementById('formNama').value.trim();
    const role = document.getElementById('formRole').value;
    const isActive = document.getElementById('formStatus').value === 'true';

    if (!username || !nama) {
        Auth.showToast('Username dan Nama wajib diisi', 'error');
        return;
    }
    if (!editId && !password) {
        Auth.showToast('Password wajib diisi untuk user baru', 'error');
        return;
    }

    loading = true;
    document.getElementById('saveBtn').textContent = 'Menyimpan...';

    try {
        if (editId) {
            const payload = { nama_lengkap: nama, role, is_active: isActive };
            if (password) payload.password = password;
            await Auth.api('PUT', '/admin/users/' + editId, payload);
            Auth.showToast('User berhasil diupdate', 'success');
        } else {
            await Auth.api('POST', '/admin/users', {
                username, password, nama_lengkap: nama, role
            });
            Auth.showToast('User berhasil ditambahkan', 'success');
        }
        closeModal();
        loadUsers();
    } catch (e) {
        Auth.showToast(e.message, 'error');
    } finally {
        loading = false;
        document.getElementById('saveBtn').textContent = 'Simpan';
    }
}

async function deleteUser(id) {
    if (!confirm('Yakin ingin menghapus user ini?')) return;
    try {
        await Auth.api('DELETE', '/admin/users/' + id);
        Auth.showToast('User berhasil dihapus', 'success');
        loadUsers();
    } catch (e) {
        Auth.showToast(e.message, 'error');
    }
}

document.getElementById('userForm').addEventListener('submit', function(e) {
    e.preventDefault();
    saveItem();
});

document.addEventListener('DOMContentLoaded', init);
