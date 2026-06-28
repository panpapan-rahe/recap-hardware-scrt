// ========================================
// DASHBOARD PAGE
// ========================================

async function init() {
    await loadStats();
}

async function loadStats() {
    try {
        const stats = await Auth.api('GET', '/perangkat/dashboard/stats');
        document.getElementById('totalPerangkat').textContent = stats.total || 0;
        document.getElementById('totalAktif').textContent = stats.per_status?.find(s => s.status === 'aktif')?.jumlah || 0;
        document.getElementById('totalDipinjam').textContent = stats.per_status?.find(s => s.status === 'dipinjam')?.jumlah || 0;
        document.getElementById('totalMaintenance').textContent = stats.per_status?.find(s => s.status === 'maintenance')?.jumlah || 0;
    } catch (e) {
        // silent
    }
}

document.addEventListener('DOMContentLoaded', init);
