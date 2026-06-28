// ========================================
// AKTIVITAS PAGE
// ========================================
async function init() {
    await loadAktivitas();
}

async function loadAktivitas() {
    try {
        const tipe = document.getElementById('filterTipe')?.value;
        let url = '/aktivitas/';
        if (tipe) url += '?tipe=' + tipe;
        const data = await Auth.api('GET', url) || [];
        renderTable(data);
    } catch (e) {
        Auth.showToast('Gagal memuat data aktivitas', 'error');
    }
}

function renderTable(data) {
    const tbody = document.getElementById('aktivitasTable');
    const emptyMsg = document.getElementById('emptyMsg');

    if (data.length === 0) {
        tbody.innerHTML = '';
        emptyMsg.style.display = 'block';
        return;
    }
    emptyMsg.style.display = 'none';

    tbody.innerHTML = data.map(a => {
        let badgeClass = 'warning';
        if (['tambah'].includes(a.tipe)) badgeClass = 'success';
        else if (['hapus', 'hapus_user'].includes(a.tipe)) badgeClass = 'danger';
        else if (['tambah_user', 'edit_user'].includes(a.tipe)) badgeClass = 'aktif';

        return `
            <tr>
                <td>${Auth.formatDate(a.created_at)}</td>
                <td><span class="badge badge-${badgeClass}">${a.tipe.replace(/_/g, ' ')}</span></td>
                <td>${a.deskripsi || '-'}</td>
                <td>${a.user_id || '-'}</td>
            </tr>
        `;
    }).join('');
}

document.addEventListener('DOMContentLoaded', init);
