# 🏦 PITUTUR-Wicara - Bank Indonesia Purwokerto

<div align="center">
  
![Bank Indonesia](https://img.shields.io/badge/Bank%20Indonesia-KPw%20Purwokerto-blue?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini%202.5-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)

**PITUTUR-Wicara** - Chatbot AI untuk Kantor Perwakilan Bank Indonesia Purwokerto dengan Knowledge Base Management System yang lengkap.

- **PITUTUR** = Pelayanan Informasi Publik Sepenuh Hati dan Transparan
- **Wicara** = Wadah Informasi Cepat dan Akurat

[🚀 Live Demo](#) • [📖 Dokumentasi](#-dokumentasi) • [🛠️ Instalasi](#-instalasi-dan-deployment)

</div>

---

## ✨ Fitur Utama

### 🤖 Chatbot Cerdas
- **AI Google Gemini 2.5 Flash** dengan fallback models
- **RAG (Retrieval-Augmented Generation)** - Hybrid semantic + keyword search
- **WhatsApp-style UI** - Mobile-friendly dan responsif
- **Multi-turn conversation** - Context-aware chat history

### 📚 Knowledge Base Management
- **Admin Dashboard** - Update KB tanpa coding (password-protected)
- **Version Control System** - Track perubahan dengan MD5 hashing
- **Auto-Sync** - Scraping otomatis dari website BI resmi
- **Export/Import** - JSON dan text format untuk integrasi

### 🎨 UI/UX Modern
- **WhatsApp-inspired design** - Familiar dan intuitif
- **Sticky header** dengan logo Bank Indonesia
- **Mobile-responsive** - Perfect di semua device
- **Hamburger menu sidebar** - Clean interface
- **Blue theme** (#2563eb) - Professional dan modern

### 🔒 Keamanan
- **API Key Management** - Streamlit Secrets integration
- **Password-protected admin** - Secure dashboard access
- **Environment variables** - Best security practices

---

## 📋 Daftar Isi
1. [Instalasi dan Deployment](#-instalasi-dan-deployment)
2. [Knowledge Base Management](#-knowledge-base-management)
3. [Dokumentasi](#-dokumentasi)
4. [Teknologi](#-teknologi)
5. [Troubleshooting](#-troubleshooting)

---

## 🚀 Instalasi dan Deployment

### Prasyarat
- Python 3.9 atau lebih baru
- Git
- Google Gemini API Key (gratis di [Google AI Studio](https://ai.google.dev/))

### Setup Lokal

1. **Clone repository**
```bash
git clone https://github.com/send0moka/bi-chatbot.git
cd bi-chatbot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Setup API Key**

Buat file `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "your-api-key-here"
```

4. **Jalankan aplikasi**
```bash
# Main chatbot
streamlit run app.py

# Admin dashboard
streamlit run admin_dashboard.py --server.port 8502
```

### Deploy ke Streamlit Cloud

1. **Push ke GitHub**
```bash
git add .
git commit -m "Initial deployment"
git push origin main
```

2. **Deploy di Streamlit Cloud**
- Buka [share.streamlit.io](https://share.streamlit.io)
- Connect GitHub repository
- Set `app.py` sebagai main file
- Tambahkan `GEMINI_API_KEY` di Secrets

3. **Deploy Admin Dashboard (Opsional)**
- Ulangi langkah 2 dengan `admin_dashboard.py`
- Port akan otomatis diatur

📖 **Panduan lengkap:** Lihat [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 📚 Knowledge Base Management

### Admin Dashboard Features

**Akses:** `streamlit run admin_dashboard.py --server.port 8502`  
**Password:** Contact admin untuk credentials

#### 1. 📝 Edit Knowledge Base
- Tambah/Edit/Hapus sections
- Real-time preview
- Auto-save dengan commit message

#### 2. 🕐 Version History
- Track semua perubahan
- Restore ke versi sebelumnya
- View diff antar versions
- Timestamp dan commit messages

#### 3. 🔄 Auto-Sync
- Scraping otomatis dari website BI
- Konfigurasi URL dan selectors
- Schedule sync (manual trigger atau cron)
- Merge strategi: replace atau append

#### 4. 📤 Export & Integration
- Export ke text format (untuk app.py)
- Export JSON (untuk backup/transfer)
- Import dari external sources

### Migrasi Knowledge Base

Jika punya hardcoded KB di `app.py`, gunakan migration script:

```bash
python migrate_knowledge.py
```

Script akan:
- Extract KB dari `app.py`
- Convert ke JSON format
- Buat initial version dengan commit
- Backup original file

📖 **Panduan lengkap:** Lihat [ADMIN_README.md](ADMIN_README.md) dan [QUICKSTART.md](QUICKSTART.md)

---

## 📖 Dokumentasi

| File | Deskripsi |
|------|-----------|
| [ADMIN_README.md](ADMIN_README.md) | Panduan lengkap admin dashboard (200+ baris) |
| [QUICKSTART.md](QUICKSTART.md) | Quick start guide untuk KB management |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Panduan deployment production |
| [API_KEY_SETUP.md](API_KEY_SETUP.md) | Security guide untuk API key |

---

## 🛠️ Teknologi

### Core Stack
- **Frontend:** Streamlit 1.31.0+
- **AI:** Google Gemini 2.5 Flash (with fallback models)
- **Embeddings:** Sentence-Transformers (all-MiniLM-L6-v2)
- **Web Scraping:** BeautifulSoup4 + lxml

### RAG Configuration
```python
chunk_size = 2000        # characters
overlap = 400            # characters
top_k = 8               # relevant chunks
semantic_weight = 0.7    # hybrid search
keyword_weight = 0.3     # hybrid search
```

### Fallback Models
1. `gemini-2.0-flash-exp`
2. `gemini-2.5-flash-lite`
3. `gemini-2.0-flash-lite`

---

## 📊 Struktur Project

```
bi-chatbot/
│
├── app.py                          # Main chatbot application (660 lines)
├── admin_dashboard.py              # Admin interface (450+ lines)
├── migrate_knowledge.py            # Migration script
├── sync_scheduler.py               # Auto-sync scheduler
├── requirements.txt                # Python dependencies
│
├── knowledge_base/                 # KB storage
│   ├── current_knowledge.json      # Active KB (7 sections)
│   ├── versions.json               # Version index
│   ├── sync_config.json            # Auto-sync config
│   └── version_*.json              # Version snapshots
│
├── .streamlit/
│   ├── config.toml                 # Streamlit config
│   └── secrets.toml                # API keys (gitignored)
│
└── docs/
    ├── ADMIN_README.md             # Admin documentation
    ├── QUICKSTART.md               # Quick start guide
    ├── DEPLOYMENT.md               # Deployment guide
    └── API_KEY_SETUP.md            # Security guide
```

---

## 🎯 Cara Pakai

### User Interface

1. **Buka chatbot** - URL production atau localhost:8501
2. **Lihat example questions** - Button di bawah chat input
3. **Chat dengan PITUTUR-Wicara** - Tanya tentang BI Purwokerto
4. **Mobile-friendly** - Gunakan di HP untuk WhatsApp-like experience

### Knowledge Base Update

1. **Akses admin dashboard** - localhost:8502 atau admin URL
2. **Login** dengan password admin
3. **Edit KB** di tab "Edit Knowledge Base"
4. **Save** dengan commit message
5. **Auto-sync** - Chatbot langsung pakai KB terbaru

### Contoh Pertanyaan

**Informasi Umum:**
- "Apa itu Bank Indonesia?"
- "Dimana alamat KPw BI Purwokerto?"
- "Bagaimana cara menghubungi BI Purwokerto?"

**Layanan:**
- "Bagaimana cara penukaran uang?"
- "Apa itu kas keliling?"
- "Bagaimana cara magang di BI?"

**Wilayah Kerja:**
- "Apa saja kabupaten yang dilayani KPw BI Purwokerto?"
- "Berapa jumlah penduduk di wilayah kerja?"

---

## 🔧 Troubleshooting

### ❌ Chatbot Error

**"No API key found"**
```bash
# Cek file .streamlit/secrets.toml
# Pastikan format: GEMINI_API_KEY = "your-key"
```

**"Rate limit exceeded"**
- Tunggu 1 menit (limit: 15 requests/menit)
- Atau gunakan API key baru

**"Information not available"**
- Update knowledge base di admin dashboard
- Cek KB sections sudah lengkap
- Verify chunk size dan top_k settings

### ❌ Admin Dashboard Error

**"Cannot connect"**
- Pastikan port 8502 tidak dipakai
- Coba port lain: `streamlit run admin_dashboard.py --server.port 8503`

**"Version restore failed"**
- Cek file version_*.json masih ada
- Restore dari backup jika perlu

**"Sync failed"**
- Verify URL website masih aktif
- Cek CSS selectors masih valid
- Lihat error di terminal

### ❌ Deployment Error

**"ModuleNotFoundError"**
```bash
# Update requirements.txt
pip freeze > requirements.txt
git add requirements.txt
git commit -m "fix: update dependencies"
git push
```

**"App not loading"**
- Klik "Reboot app" di Streamlit Cloud
- Cek logs untuk error details
- Verify secrets sudah di-set

### ❌ Logo/UI Issues

**"Logo not displaying"**
- Logo sudah inline SVG (no CORS)
- Clear browser cache
- Check console for errors

**"Mobile view broken"**
- Refresh page
- Clear cookies
- Try different browser

---

## 🔐 Security Best Practices

1. **API Keys**
   - Never commit `.streamlit/secrets.toml` to Git
   - Use environment variables in production
   - Rotate keys regularly

2. **Admin Access**
   - Set strong admin password in secrets/environment
   - Use passwords with 16+ characters
   - Enable 2FA untuk GitHub/Streamlit accounts
   - Never commit passwords to repository

3. **Version Control**
   - Commit dengan meaningful messages
   - Review changes before pushing
   - Backup KB versions regularly

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'feat: add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

**Commit Convention:**
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation updates
- `style:` - Code formatting
- `refactor:` - Code restructuring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

---

## 📝 Changelog

### v1.2.0 (2025-12-02)
- ✨ Official Bank Indonesia SVG logo (inline, no CORS)
- 🔒 Secure API key management (Streamlit Secrets)
- 📚 Knowledge Base Management System
- 🔄 Version control with MD5 hashing
- 🌐 Auto-sync from BI website
- 📤 Export/Import functionality
- 📖 Comprehensive documentation (4 guides)

### v1.1.0 (2025-11-28)
- 🎨 WhatsApp-style mobile UI
- 🔵 Blue theme (#2563eb)
- 📱 Mobile-responsive design
- 🍔 Hamburger menu sidebar
- ⚡ RAG optimization (chunk 2000, overlap 400, top-k 8)

### v1.0.0 (2025-11-25)
- 🚀 Initial release
- 🤖 Google Gemini 2.5 Flash integration
- 📚 Hardcoded knowledge base
- 💬 Basic chat functionality

---

## 📜 License

MIT License - see [LICENSE](LICENSE) for details

---

## 👥 Team

**Developed by:** send0moka  
**Organization:** Bank Indonesia - KPw Purwokerto  
**Contact:** [GitHub](https://github.com/send0moka)

---

## 🙏 Acknowledgments

- **Streamlit** - Amazing framework untuk web apps
- **Google Gemini** - Powerful AI model
- **Sentence Transformers** - Excellent embeddings
- **BeautifulSoup** - Reliable web scraping
- **Bank Indonesia** - Logo dan knowledge base

---

## ⭐ Star History

Jika project ini bermanfaat, kasih ⭐ di GitHub!

---

<div align="center">

**[⬆ Kembali ke atas](#-pitutur-wicara---bank-indonesia-purwokerto)**

Made with ❤️ using Streamlit & Google Gemini

© 2025 Bank Indonesia Purwokerto

</div>