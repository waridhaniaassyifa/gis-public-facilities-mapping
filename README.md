# Pemetaan dan Visualisasi Aset Fasilitas Umum Berbasis GIS

Proyek sederhana Geographic Information System (GIS) menggunakan Python untuk mengelola data aset fasilitas umum dan menampilkan lokasinya pada peta interaktif.

## Latar Belakang

Pengelolaan aset membutuhkan data yang terstruktur agar nama, kategori, kondisi, dan lokasi aset dapat diperiksa dengan mudah. Data yang tersimpan dalam format terpisah dapat menyulitkan pencarian dan pemantauan. Proyek ini menunjukkan proses membaca data aset, memvalidasi informasi, membuat ringkasan, dan memvisualisasikan lokasi menggunakan GIS.

## Tujuan

- Menerapkan konsep GIS untuk visualisasi lokasi aset.
- Membaca dan menstandardisasi data aset dari berkas CSV.
- Memvalidasi kelengkapan data dan koordinat.
- Membuat peta interaktif yang dapat dibuka melalui browser.
- Menghasilkan ringkasan aset berdasarkan kategori dan kondisi.

## Teknologi yang Digunakan

- Python 3.10 atau lebih baru
- pandas
- Folium
- CSV sebagai sumber data

## Struktur Proyek

```text
studi-kasus-gis-aset/
├── data/
│   └── aset_fasilitas.csv
├── output/
├── src/
│   └── main.py
├── .gitignore
├── requirements.txt
├── STUDI_KASUS.md
└── README.md
```

## Instalasi

1. Unduh atau clone repositori.
2. Pastikan Python telah terpasang.
3. Buka terminal di folder proyek.
4. Instal dependensi dengan perintah:

```bash
pip install -r requirements.txt
```

## Cara Menjalankan Program

Jalankan perintah berikut dari folder utama proyek:

```bash
python src/main.py
```

Program akan membaca data aset, memeriksa kelengkapan informasi, memvalidasi koordinat, dan membuat peta interaktif.

## Hasil Program

- `output/peta_aset.html`: peta interaktif dengan penanda lokasi aset.
- `output/ringkasan_kategori.csv`: ringkasan jumlah aset berdasarkan kategori.
- `output/ringkasan_kondisi.csv`: ringkasan jumlah aset berdasarkan kondisi.

Buka `peta_aset.html` menggunakan browser untuk melihat peta. Koneksi internet diperlukan untuk memuat peta dasar OpenStreetMap.

## Format Data

| Kolom | Keterangan |
|---|---|
| `id_aset` | ID unik aset |
| `nama_aset` | Nama fasilitas |
| `kategori` | Jenis fasilitas |
| `kondisi` | Kondisi aset |
| `latitude` | Koordinat lintang |
| `longitude` | Koordinat bujur |

**Catatan:** Data yang disertakan merupakan data dummy untuk demonstrasi dan bukan data inventaris resmi.

## Pengembangan Selanjutnya

- Mengintegrasikan PostgreSQL/PostGIS sebagai basis data spasial.
- Menambahkan filter kategori dan kondisi.
- Mengembangkan dashboard statistik.
- Menghubungkan data dari beberapa instansi melalui API.
- Menambahkan fitur pengelolaan aset berbasis web.

## Relevansi dengan Materi Praktisi Mengajar

Proyek ini menerapkan konsep GIS, pemrograman, pengolahan data, visualisasi, dan pengelolaan aset. Proyek ini juga menunjukkan pentingnya integrasi dan standardisasi data agar informasi dapat dikelola secara terpadu dan dimanfaatkan secara optimal.

## Lisensi

Proyek ini dibuat untuk keperluan pembelajaran. Pastikan data tambahan yang digunakan memiliki izin penggunaan yang sesuai.
