// ========================================
// REPORT PAGE
// ========================================
let cabangList = [];
let kategoriList = [];

async function init() {
    await loadCabang();
    await loadKategori();
    await loadReport();
}

async function loadCabang() {
    try {
        cabangList = await Auth.api('GET', '/cabang/') || [];
        cabangList.sort((a, b) => (a.kode || '').localeCompare(b.kode || ''));
        const filterEl = document.getElementById('filterCabang');
        filterEl.innerHTML = '<option value="">Semua Cabang</option>' +
            cabangList.map(c => `<option value="${c.id}">${c.nama}</option>`).join('');
    } catch (e) { /* silent */ }
}

async function loadKategori() {
    try {
        kategoriList = await Auth.api('GET', '/kategori/') || [];
        const filterEl = document.getElementById('filterKategori');
        filterEl.innerHTML = '<option value="">Semua Kategori</option>' +
            kategoriList.map(k => `<option value="${k.id}">${k.nama}</option>`).join('');
    } catch (e) { /* silent */ }
}

async function loadReport() {
    try {
        const params = [];
        const cabang = document.getElementById('filterCabang')?.value;
        const kategori = document.getElementById('filterKategori')?.value;
        const status = document.getElementById('filterStatus')?.value;
        if (cabang) params.push('cabang_id=' + cabang);
        if (kategori) params.push('kategori_id=' + kategori);
        if (status) params.push('status=' + status);

        let url = '/report/data';
        if (params.length) url += '?' + params.join('&');

        const data = await Auth.api('GET', url) || [];
        renderTable(data);
    } catch (e) {
        document.getElementById('reportTableBody').innerHTML =
            '<tr><td colspan="7" class="text-muted text-center">Gagal memuat data</td></tr>';
    }
}

function renderTable(data) {
    const tbody = document.getElementById('reportTableBody');

    if (data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-muted text-center">Tidak ada data dengan filter tersebut</td></tr>';
        return;
    }

    tbody.innerHTML = data.map(d => `
        <tr>
            <td>${d.kode_unik}</td>
            <td>${d.nama}</td>
            <td>${d.kategori_nama || '-'}</td>
            <td>${(d.merk || '') + ' ' + (d.model || '')}</td>
            <td>${d.cabang_nama || '-'}</td>
            <td><span class="badge badge-${d.status}">${d.status}</span></td>
            <td>${d.lokasi_detail || '-'}</td>
        </tr>
    `).join('');
}

async function exportCSV() {
    try {
        const params = [];
        const cabang = document.getElementById('filterCabang')?.value;
        const kategori = document.getElementById('filterKategori')?.value;
        const status = document.getElementById('filterStatus')?.value;
        if (cabang) params.push('cabang_id=' + cabang);
        if (kategori) params.push('kategori_id=' + kategori);
        if (status) params.push('status=' + status);

        let url = '/report/export/csv';
        if (params.length) url += '?' + params.join('&');

        const res = await fetch('/api' + url, {
            headers: { 'Authorization': 'Bearer ' + Auth.getToken() }
        });
        const blob = await res.blob();
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = `report-${new Date().toISOString().slice(0,10)}.csv`;
        a.click();
        Auth.showToast('CSV berhasil diunduh', 'success');
    } catch (e) {
        Auth.showToast('Gagal export CSV', 'error');
    }
}

async function exportPDF() {
    try {
        const params = [];
        const cabang = document.getElementById('filterCabang')?.value;
        const kategori = document.getElementById('filterKategori')?.value;
        const status = document.getElementById('filterStatus')?.value;
        if (cabang) params.push('cabang_id=' + cabang);
        if (kategori) params.push('kategori_id=' + kategori);
        if (status) params.push('status=' + status);

        let url = '/report/export/pdf';
        if (params.length) url += '?' + params.join('&');

        const res = await fetch('/api' + url, {
            headers: { 'Authorization': 'Bearer ' + Auth.getToken() }
        });
        const blob = await res.blob();
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = `report-${new Date().toISOString().slice(0,10)}.pdf`;
        a.click();
        Auth.showToast('PDF berhasil diunduh', 'success');
    } catch (e) {
        Auth.showToast('Gagal export PDF', 'error');
    }
}

document.addEventListener('DOMContentLoaded', init);
