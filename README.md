# 🏦 Bank Indonesia Chatbot - Panduan Lengkap Deploy

## 📋 Daftar Isi
1. [Persiapan Awal](#persiapan-awal)
2. [Setup Lokal](#setup-lokal)
3. [Deploy ke Streamlit Cloud](#deploy-ke-streamlit-cloud)
4. [Cara Pakai](#cara-pakai)
5. [Troubleshooting](#troubleshooting)

---

## 🎯 Persiapan Awal

### 1. Install Python
**Download Python 3.9 atau lebih baru:**
- 🪟 Windows: https://www.python.org/downloads/
- 🍎 Mac: Sudah terinstall, atau `brew install python`
- 🐧 Linux: `sudo apt install python3 python3-pip`

**Cek instalasi:**
```bash
python --version
# atau
python3 --version
```

Harus muncul: `Python 3.9.x` atau lebih tinggi

### 2. Dapatkan Google Gemini API Key (GRATIS)

**Step by step:**
1. Buka: https://ai.google.dev/
2. Klik **"Get API Key"** atau **"Get Started"**
3. Login dengan akun Google
4. Klik **"Create API Key"**
5. Copy API Key (contoh: `AIzaSyD7_PAF98KwkGPGSHLWPmBF1GsXDAyxEA8`)
6. **SIMPAN API KEY INI!** ⚠️

> ✅ **GRATIS & NO CREDIT CARD REQUIRED**
> - 15 requests per menit
> - 1,500 requests per hari
> - Cukup untuk chatbot pribadi

### 3. Install Git
**Download Git:**
- Windows: https://git-scm.com/download/win
- Mac: `brew install git`
- Linux: `sudo apt install git`

**Cek instalasi:**
```bash
git --version
```

---

## 💻 Setup Lokal (Test di Laptop)

### Step 1: Buat Folder Project
```bash
# Buat folder
mkdir bi-chatbot
cd bi-chatbot
```

### Step 2: Buat File-file Project

**A. Buat file `app.py`**
- Copy semua kode dari artifact "app.py - Main Application"
- Paste ke file `app.py`

**B. Buat file `requirements.txt`**
```
streamlit==1.31.0
google-generativeai==0.3.2
PyPDF2==3.0.1
```

**C. Buat folder `.streamlit` dan file `config.toml`**
```bash
mkdir .streamlit
```

Isi file `.streamlit/config.toml`:
```toml
[theme]
primaryColor="#667eea"
backgroundColor="#FFFFFF"
secondaryBackgroundColor="#f0f2f6"
textColor="#262730"
font="sans serif"

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

> ⚠️ Jika error, coba: `pip3 install -r requirements.txt`

### Step 4: Jalankan Aplikasi Lokal
```bash
streamlit run app.py
```

Browser akan otomatis terbuka di `http://localhost:8501`

**🎉 KALAU BERHASIL:**
- Aplikasi muncul di browser
- Ada sidebar dengan input API key
- Bisa upload dokumen
- Bisa chat

---

## 🚀 Deploy ke Streamlit Cloud (GRATIS SELAMANYA)

### Step 1: Buat Akun GitHub (Jika Belum Punya)
1. Buka: https://github.com/
2. Klik **"Sign Up"**
3. Ikuti instruksi (gratis)

### Step 2: Upload Project ke GitHub

**A. Init Git di folder project:**
```bash
cd bi-chatbot
git init
```

**B. Buat file `.gitignore`:**
```
__pycache__/
*.pyc
.streamlit/secrets.toml
*.pdf
*.txt
```

**C. Commit semua file:**
```bash
git add .
git commit -m "Initial commit - BI Chatbot"
```

**D. Buat Repository di GitHub:**
1. Login ke GitHub
2. Klik ikon **"+"** di pojok kanan atas
3. Pilih **"New repository"**
4. Nama repository: `bi-chatbot`
5. Set ke **Public**
6. **JANGAN** centang "Initialize with README"
7. Klik **"Create repository"**

**E. Push ke GitHub:**
```bash
# Ganti YOUR_USERNAME dengan username GitHub Anda
git remote add origin https://github.com/YOUR_USERNAME/bi-chatbot.git
git branch -M main
git push -u origin main
```

> Akan diminta username & password GitHub

### Step 3: Deploy ke Streamlit Cloud

**A. Buat Akun Streamlit Cloud:**
1. Buka: https://streamlit.io/cloud
2. Klik **"Sign up"**
3. Login dengan akun **GitHub** (yang tadi dibuat)
4. Authorize Streamlit

**B. Deploy Aplikasi:**
1. Klik **"New app"**
2. Pilih:
   - **Repository:** `YOUR_USERNAME/bi-chatbot`
   - **Branch:** `main`
   - **Main file path:** `app.py`
3. Klik **"Deploy!"**

**C. Tunggu Deploy (2-3 menit)**
- Status akan berubah dari "Building" ke "Running"
- URL akan muncul: `https://YOUR_APP.streamlit.app`

### Step 4: Tambahkan API Key (AMAN)

**Opsi 1: User Input API Key (Recommended)**
- User memasukkan API key mereka sendiri di sidebar
- Tidak perlu config tambahan
- Setiap user pakai API key sendiri

**Opsi 2: Simpan API Key di Secrets (Admin Only)**
1. Di Streamlit Cloud, buka app Anda
2. Klik **⚙️ Settings** → **Secrets**
3. Tambahkan:
```toml
GOOGLE_API_KEY = "AIzaSyD7_PAF98KwkGPGSHLWPmBF1GsXDAyxEA8"
```
4. Save

Lalu ubah kode di `app.py`:
```python
# Tambahkan di bagian atas main()
if 'api_key' not in st.session_state:
    st.session_state.api_key = st.secrets.get("GOOGLE_API_KEY", "")
```

---

## 🎮 Cara Pakai Chatbot

### 1. Buka Aplikasi
- Lokal: `http://localhost:8501`
- Online: `https://YOUR_APP.streamlit.app`

### 2. Masukkan API Key
- Di sidebar, paste API key Gemini Anda
- Klik enter atau klik di luar input box

### 3. Upload Dokumen (Opsional)
**Download dokumen resmi BI:**
- [Publikasi BI](https://www.bi.go.id/id/publikasi/laporan/Default.aspx)
- [Statistik BI](https://www.bi.go.id/id/statistik/Default.aspx)

**Upload:**
- Klik **"Upload PDF atau TXT"**
- Pilih file PDF/TXT dari komputer
- Tunggu proses (beberapa detik)
- Dokumen otomatis tersimpan

### 4. Mulai Chat!
**Contoh pertanyaan:**
- "Apa itu Bank Indonesia?"
- "Berapa suku bunga BI rate saat ini?"
- "Apa tugas utama Bank Indonesia?"
- "Bagaimana cara menghubungi BI?"
- "Jelaskan tentang inflasi di Indonesia"

**Jika sudah upload dokumen:**
- Chatbot akan jawab berdasarkan dokumen
- Akan tampil sumber dokumen di bawah jawaban

---

## 🔧 Troubleshooting

### ❌ Error: "No module named 'streamlit'"
**Solusi:**
```bash
pip install streamlit
# atau
pip3 install streamlit
```

### ❌ Error: "API Key not valid"
**Solusi:**
- Cek API key sudah benar
- Pastikan tidak ada spasi di awal/akhir
- Generate API key baru di https://ai.google.dev/

### ❌ Error: "Rate limit exceeded"
**Solusi:**
- Tunggu 1 menit (limit: 15 requests/menit)
- Atau generate API key baru

### ❌ Error saat upload PDF: "Cannot extract text"
**Solusi:**
- Pastikan PDF bukan scan/gambar
- Convert PDF scan ke text dulu
- Atau pakai file TXT

### ❌ Deploy gagal di Streamlit Cloud
**Solusi:**
1. Cek `requirements.txt` sudah benar
2. Pastikan semua file sudah di-push ke GitHub:
```bash
git status
git add .
git commit -m "fix"
git push
```
3. Di Streamlit Cloud, klik **"Reboot app"**

### ❌ Aplikasi lambat / hanging
**Solusi:**
- Hapus dokumen yang tidak perlu (tombol "Hapus Semua Dokumen")
- Refresh browser
- Clear cache Streamlit:
```bash
streamlit cache clear
```

---

## 📊 Struktur File Final

```
bi-chatbot/
│
├── app.py                      # Aplikasi utama
├── requirements.txt            # Dependencies
├── .gitignore                  # File yang diabaikan Git
├── README.md                   # (opsional)
│
└── .streamlit/
    └── config.toml            # Konfigurasi Streamlit
```

---

## 🎓 Tips & Trik

### 1. **Untuk Jawaban Lebih Akurat:**
- Upload dokumen resmi BI (PDF)
- Upload beberapa dokumen berbeda
- Dokumen lebih baru = jawaban lebih akurat

### 2. **Hemat API Quota:**
- Gunakan pertanyaan yang jelas
- Hindari pertanyaan yang sama berulang-ulang
- API key gratis: 1,500 requests/hari (cukup!)

### 3. **Share dengan Orang Lain:**
- Share URL Streamlit Cloud
- Mereka bisa pakai tanpa install apa-apa
- Setiap user pakai API key sendiri (aman)

### 4. **Update Aplikasi:**
```bash
# Edit file app.py
git add .
git commit -m "update fitur baru"
git push
# Streamlit Cloud otomatis update!
```

---

## 🆘 Butuh Bantuan?

**Kontak:**
- 📧 Email support Streamlit: support@streamlit.io
- 📚 Dokumentasi: https://docs.streamlit.io
- 💬 Forum: https://discuss.streamlit.io

**Link Berguna:**
- 🔑 Google AI Studio: https://ai.google.dev/
- 🐙 GitHub Docs: https://docs.github.com/
- 🚀 Streamlit Cloud: https://streamlit.io/cloud

---

## ✅ Checklist Deploy

- [ ] Python 3.9+ terinstall
- [ ] Git terinstall
- [ ] Google Gemini API Key sudah didapat
- [ ] File `app.py` sudah dibuat
- [ ] File `requirements.txt` sudah dibuat
- [ ] Folder `.streamlit/config.toml` sudah dibuat
- [ ] Test lokal berhasil (`streamlit run app.py`)
- [ ] Akun GitHub sudah dibuat
- [ ] Project sudah di-push ke GitHub
- [ ] Akun Streamlit Cloud sudah dibuat
- [ ] Aplikasi sudah di-deploy
- [ ] Test online berhasil
- [ ] API Key sudah di-input
- [ ] Upload dokumen test berhasil
- [ ] Chat test berhasil

---

## 🎉 SELAMAT!

Chatbot Bank Indonesia Anda sudah online dan bisa dipakai!

**URL Aplikasi:** `https://YOUR_APP.streamlit.app`

**Share ke teman/kolega dan mulai pakai! 🚀**

---

*Dibuat dengan ❤️ menggunakan Streamlit & Google Gemini*