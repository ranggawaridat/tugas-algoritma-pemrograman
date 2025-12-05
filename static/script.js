const API_URL = '/api/mahasiswa';

// State
let isEditing = false;
let currentEditNim = null;

// DOM Elements
const form = document.getElementById('mahasiswaForm');
const formTitle = document.getElementById('form-title');
const btnSave = document.getElementById('btn-save');
const btnCancel = document.getElementById('btn-cancel');
const tableBody = document.querySelector('#mahasiswaTable tbody');
const dataCount = document.getElementById('data-count');
const loading = document.getElementById('loading');
const emptyState = document.getElementById('empty-state');

// Search & Sort Elements
const searchInput = document.getElementById('search-input');
const searchMethod = document.getElementById('search-method');
const btnSearch = document.getElementById('btn-search');
const sortKey = document.getElementById('sort-key');
const sortOrder = document.getElementById('sort-order');
const sortAlgo = document.getElementById('sort-algo');
const btnSort = document.getElementById('btn-sort');

// --- Functions ---

async function fetchData(params = {}) {
    showLoading(true);
    try {
        const queryParams = new URLSearchParams(params).toString();
        const response = await fetch(`${API_URL}?${queryParams}`);
        if (!response.ok) throw new Error('Gagal mengambil data');
        const data = await response.json();
        renderTable(data);
    } catch (error) {
        console.error(error);
        alert('Terjadi kesalahan saat mengambil data.');
    } finally {
        showLoading(false);
    }
}

function renderTable(data) {
    tableBody.innerHTML = '';
    dataCount.textContent = `${data.length} Data`;

    if (data.length === 0) {
        emptyState.style.display = 'block';
        return;
    } else {
        emptyState.style.display = 'none';
    }

    data.forEach(mhs => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${mhs.nim}</td>
            <td>${mhs.nama}</td>
            <td>${mhs.jurusan}</td>
            <td>${mhs.ipk.toFixed(2)}</td>
            <td>
                <button class="btn btn-edit" onclick="editMahasiswa('${mhs.nim}', '${mhs.nama}', '${mhs.jurusan}', ${mhs.ipk})">Edit</button>
                <button class="btn btn-danger" onclick="deleteMahasiswa('${mhs.nim}')">Hapus</button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

function showLoading(show) {
    loading.style.display = show ? 'block' : 'none';
    if (show) {
        tableBody.innerHTML = '';
        emptyState.style.display = 'none';
    }
}

async function saveMahasiswa(event) {
    event.preventDefault();
    
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    
    // Convert IPK to float
    data.ipk = parseFloat(data.ipk);

    try {
        let response;
        if (isEditing) {
            response = await fetch(`${API_URL}/${currentEditNim}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
        } else {
            response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
        }

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'Gagal menyimpan data');
        }

        resetForm();
        fetchData(); // Refresh table
        alert(isEditing ? 'Data berhasil diperbarui!' : 'Data berhasil ditambahkan!');
        
    } catch (error) {
        alert(error.message);
    }
}

async function deleteMahasiswa(nim) {
    if (!confirm(`Apakah Anda yakin ingin menghapus data mahasiswa dengan NIM ${nim}?`)) return;

    try {
        const response = await fetch(`${API_URL}/${nim}`, {
            method: 'DELETE'
        });

        if (!response.ok) throw new Error('Gagal menghapus data');

        fetchData();
    } catch (error) {
        alert(error.message);
    }
}

// Global scope function for onclick access
window.editMahasiswa = function(nim, nama, jurusan, ipk) {
    isEditing = true;
    currentEditNim = nim;
    
    document.getElementById('nim').value = nim;
    document.getElementById('nama').value = nama;
    document.getElementById('jurusan').value = jurusan;
    document.getElementById('ipk').value = ipk;

    // NIM tidak boleh diedit saat update (primary key logic sederhana)
    // Atau bisa diedit tapi logic backend harus handle update NIM. 
    // Di sini kita disable agar konsisten dengan logic manager.update_mahasiswa yang replace object
    // tapi biasanya PK tidak berubah.
    document.getElementById('nim').readOnly = true;
    document.getElementById('nim').style.backgroundColor = '#f1f5f9';

    formTitle.textContent = 'Edit Data Mahasiswa';
    btnSave.textContent = 'Update Data';
    btnCancel.style.display = 'inline-flex';
    
    // Scroll to form
    form.scrollIntoView({ behavior: 'smooth' });
};

window.deleteMahasiswa = deleteMahasiswa;

function resetForm() {
    form.reset();
    isEditing = false;
    currentEditNim = null;
    
    document.getElementById('nim').readOnly = false;
    document.getElementById('nim').style.backgroundColor = 'white';
    
    formTitle.textContent = 'Tambah Data Mahasiswa';
    btnSave.textContent = 'Simpan Data';
    btnCancel.style.display = 'none';
}

// Event Listeners
form.addEventListener('submit', saveMahasiswa);

btnCancel.addEventListener('click', resetForm);

btnSearch.addEventListener('click', () => {
    const query = searchInput.value;
    const method = searchMethod.value;
    fetchData({ search: query, search_method: method });
});

btnSort.addEventListener('click', () => {
    const key = sortKey.value;
    const order = sortOrder.value;
    const algo = sortAlgo.value;
    
    // Jika ada search query, kita sertakan juga
    const query = searchInput.value;
    const method = searchMethod.value;
    
    const params = {
        sort_by: key,
        order: order,
        algo: algo
    };
    
    if (query) {
        params.search = query;
        params.search_method = method;
    }
    
    fetchData(params);
});

// Initial Load
fetchData();
