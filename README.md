# Manajemen Data Mahasiswa

Aplikasi sederhana untuk manajemen data mahasiswa berbasis GUI Web menggunakan **FastAPI** (Python) dan **Vanilla JS**.

## Fitur
- **CRUD**: Input, Edit, Hapus, Tampilkan data mahasiswa.
- **Sorting**: Bubble Sort, Selection Sort, Merge Sort.
- **Searching**: Linear Search, Binary Search.
- **Validasi**: Regex untuk input NIM dan Nama.
- **File I/O**: Penyimpanan data persisten (JSON).

## Cara Menjalankan Lokal

1.  **Install Python 3.10+**
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Jalankan Aplikasi**:
    ```bash
    uvicorn main:app --reload
    ```
4.  **Buka Browser**:
    Akses `http://127.0.0.1:8000`

## Cara Deploy

### Opsi 1: Menggunakan Docker

1.  **Build Image**:
    ```bash
    docker build -t manajemen-mahasiswa .
    ```
2.  **Jalankan Container**:
    ```bash
    docker run -p 8000:8000 manajemen-mahasiswa
    ```

### Opsi 2: Deploy ke Render / Railway (Gratis)

Aplikasi ini sudah dilengkapi dengan `Procfile` dan `requirements.txt` sehingga siap di-deploy ke layanan PaaS seperti **Render** atau **Railway**.

1.  Push kode ini ke **GitHub**.
2.  Buka dashboard **Render** atau **Railway**.
3.  Buat **New Web Service** dan hubungkan repository GitHub Anda.
4.  Platform akan otomatis mendeteksi `Procfile` dan melakukan build.
5.  Aplikasi Anda akan live di URL yang diberikan provider.
