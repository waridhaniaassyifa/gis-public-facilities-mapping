# Studi Kasus: Pemetaan dan Visualisasi Aset Fasilitas Umum Berbasis GIS

## 1. Deskripsi Masalah

Data aset fasilitas umum dapat mencakup nama aset, kategori, kondisi, dan lokasi geografis. Jika informasi tidak disusun dengan format yang seragam, pencarian dan pemantauan aset dapat menjadi kurang efisien.

## 2. Rumusan Masalah

Bagaimana menerapkan GIS dan pemrograman Python untuk menyusun data aset fasilitas umum serta menyajikan lokasinya melalui peta interaktif?

## 3. Tujuan

- Menyusun data aset dalam format CSV dengan kolom yang konsisten.
- Memvalidasi kelengkapan data dan koordinat.
- Menampilkan lokasi aset pada peta interaktif.
- Menyediakan ringkasan aset berdasarkan kategori dan kondisi.

## 4. Data yang Digunakan

Data contoh terdiri atas ID, nama aset, kategori, kondisi, latitude, dan longitude. Seluruh data contoh bersifat dummy/ilustratif dan tidak boleh dianggap sebagai data inventaris resmi.

## 5. Metode dan Implementasi

1. **Pengumpulan data:** data dimasukkan ke dalam CSV.
2. **Standardisasi:** nama kolom dan nilai kategori/kondisi menggunakan format konsisten.
3. **Validasi:** program memeriksa kolom wajib, nilai kosong, ID duplikat, dan rentang koordinat.
4. **Analisis sederhana:** program menghitung jumlah aset per kategori dan kondisi.
5. **Visualisasi:** Folium membuat peta interaktif dengan penanda untuk setiap aset.
6. **Dokumentasi:** kode, data contoh, dan petunjuk penggunaan disimpan di GitHub.

## 6. Hasil yang Diharapkan

Program menghasilkan peta HTML interaktif dan dua berkas ringkasan CSV. Pengguna dapat membuka peta melalui browser dan melihat informasi setiap aset dengan memilih penandanya.

## 7. Hubungan dengan Materi Pemateri

Studi kasus ini berkaitan dengan pemanfaatan GIS untuk pengelolaan aset, kemampuan pemrograman dan analisis data, serta pentingnya integrasi dan standardisasi informasi. Pengembangan lebih lanjut dapat menggunakan PostgreSQL/PostGIS dan API untuk menyatukan data dari berbagai sumber.

## 8. Kesimpulan

GIS dapat membantu menyajikan informasi aset berdasarkan lokasi sehingga lebih mudah dipahami. Dengan Python, proses pembacaan, pemeriksaan, peringkasan, dan visualisasi data dapat dilakukan secara lebih terstruktur. Untuk penggunaan nyata, data harus diverifikasi dan dikelola sesuai standar yang disepakati.
