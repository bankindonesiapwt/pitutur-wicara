# Admin Dashboard - Knowledge Base Management

## 🎯 Fitur Utama

### 1. **Edit Knowledge Base tanpa Coding**
- Tambah, edit, dan hapus sections secara visual
- Interface yang user-friendly
- Real-time preview
- No coding required!

### 2. **Version Control System**
- Automatic versioning setiap perubahan
- Version history lengkap dengan timestamp
- Restore ke versi sebelumnya kapan saja
- Commit messages untuk tracking perubahan

### 3. **Auto-Sync dari Website BI**
- Monitoring multiple URLs
- Automatic content fetching
- Configurable sync interval (hourly/daily/weekly)
- Manual sync on-demand

### 4. **Export & Integration**
- Export ke format Text atau JSON
- Easy integration dengan app.py
- Preview sebelum export
- Download ready-to-use files

## 🚀 Cara Menjalankan

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Jalankan Admin Dashboard
```bash
streamlit run admin_dashboard.py
```

Dashboard akan terbuka di: `http://localhost:8501`

### 3. Login
- **Default Password:** `admin123`
- ⚠️ **PENTING:** Ganti password di production!

## 📖 Panduan Penggunaan

### Edit Knowledge Base

1. Login ke admin dashboard
2. Buka tab **"Edit Knowledge Base"**
3. Klik **"Add New Section"** untuk menambah section baru
4. Isi Title dan Content
5. Klik **"Save Section"**
6. Section otomatis tersimpan dengan versioning

### Mengedit Section Existing

1. Expand section yang ingin diedit
2. Edit Title atau Content
3. Klik **"Update"** untuk menyimpan
4. Atau **"Delete"** untuk menghapus section

### Version History

1. Buka tab **"Version History"**
2. Lihat semua versi yang pernah disimpan
3. Klik **"Restore This Version"** untuk kembali ke versi tertentu
4. Klik **"View Details"** untuk melihat isi lengkap

### Auto-Sync Configuration

1. Buka tab **"Auto-Sync"**
2. Enable/disable auto-sync
3. Tambahkan URLs yang ingin dimonitor (satu per baris):
   ```
   https://www.bi.go.id/id/tentang-bi/profil/Default.aspx
   https://www.bi.go.id/id/layanan/Default.aspx
   ```
4. Pilih sync interval (hourly/daily/weekly)
5. Klik **"Save Sync Configuration"**
6. Test dengan **"Sync Now"**

### Export Knowledge Base

1. Buka tab **"Export"**
2. Pilih format export:
   - **Text (.txt)**: Untuk copy-paste ke `BUILTIN_KNOWLEDGE` di app.py
   - **JSON (.json)**: Untuk dynamic loading
3. Klik **"Download"**
4. Gunakan file hasil export

## 🔄 Integrasi dengan App.py

### Metode 1: Manual Copy-Paste
1. Export knowledge base sebagai Text
2. Buka `app.py`
3. Replace isi variabel `BUILTIN_KNOWLEDGE` dengan text yang di-export
4. Save dan restart aplikasi

### Metode 2: Dynamic Loading (Recommended)
Sudah terintegrasi otomatis! App.py akan:
1. Check file `knowledge_base/current_knowledge.json`
2. Load knowledge base dari JSON jika ada
3. Fallback ke hardcoded knowledge jika file tidak ada

Setiap kali Anda update knowledge base di admin dashboard, perubahan otomatis terapply di chatbot!

## 📁 Struktur File

```
pitutur-wicara/
├── app.py                          # Main chatbot application
├── admin_dashboard.py              # Admin dashboard for KB management
├── requirements.txt                # Python dependencies
├── knowledge_base/                 # KB storage directory
│   ├── current_knowledge.json     # Current active KB
│   ├── versions.json              # Version history index
│   ├── version_1_abc123.json      # Version snapshots
│   ├── version_2_def456.json
│   └── sync_config.json           # Auto-sync configuration
└── .streamlit/
    └── config.toml                # Streamlit configuration
```

## 🔐 Security Notes

### Production Deployment:

1. **Ganti Password Default**
   ```python
   # Di admin_dashboard.py, line 27
   ADMIN_PASSWORD = "your_secure_password_here"
   ```

2. **Gunakan Environment Variable**
   ```python
   import os
   ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "default_password")
   ```

3. **Tambahkan Authentication Layer**
   - Gunakan Streamlit authentication library
   - Implementasi JWT atau OAuth
   - Multi-user support dengan role-based access

4. **Protect Admin Dashboard**
   - Deploy di URL terpisah
   - Gunakan firewall/IP whitelist
   - HTTPS only

## 🛠️ Advanced Configuration

### Custom Sync Sources

Edit fungsi `fetch_bi_website_content()` di `admin_dashboard.py` untuk customize parsing:

```python
def fetch_bi_website_content(url):
    # Add custom parsing logic
    # Extract specific elements
    # Filter unwanted content
    pass
```

### Scheduled Auto-Sync

Untuk menjalankan auto-sync secara scheduled, gunakan:

**Linux/Mac (cron):**
```bash
# Edit crontab
crontab -e

# Add line for daily sync at 2 AM
0 2 * * * cd /path/to/bi-chatbot && python sync_scheduler.py
```

**Windows (Task Scheduler):**
- Buat scheduled task
- Run: `python sync_scheduler.py`
- Set trigger sesuai interval

### Backup Strategy

Recommended backup:
1. **Daily backup** folder `knowledge_base/`
2. **Git version control** untuk version history
3. **Cloud storage sync** (Google Drive, Dropbox, etc.)

```bash
# Auto backup script
#!/bin/bash
DATE=$(date +%Y%m%d)
tar -czf backup_kb_$DATE.tar.gz knowledge_base/
# Upload to cloud or copy to backup location
```

## 📊 Monitoring & Analytics

Future enhancements:
- Track KB usage statistics
- Most accessed sections
- Search query analytics
- User feedback integration
- A/B testing for KB content

## 🤝 Contributing

Untuk menambahkan fitur baru:
1. Fork repository
2. Create feature branch
3. Implement & test
4. Submit pull request

## 📝 Changelog

### Version 1.0.0 (Current)
- ✅ Basic CRUD operations
- ✅ Version control system
- ✅ Auto-sync configuration
- ✅ Export functionality
- ✅ Integration with app.py

### Planned Features
- [ ] Multi-user support
- [ ] Role-based access control
- [ ] Advanced text editor (Markdown support)
- [ ] Image upload for KB
- [ ] Search & filter in admin
- [ ] Analytics dashboard
- [ ] Automated testing
- [ ] API endpoints

## 🆘 Troubleshooting

### Issue: Knowledge base tidak ter-update di chatbot
**Solution:**
1. Check file `knowledge_base/current_knowledge.json` exists
2. Restart app.py: `streamlit run app.py`
3. Clear browser cache

### Issue: Auto-sync gagal
**Solution:**
1. Check internet connection
2. Verify URLs masih accessible
3. Check website structure belum berubah
4. Review error message di dashboard

### Issue: Version restore tidak bekerja
**Solution:**
1. Check file permissions di folder `knowledge_base/`
2. Verify version file masih ada
3. Check JSON format valid

## 📧 Support

Untuk bantuan atau bug report:
- Open issue di GitHub repository
- Contact: admin@example.com

---

**Happy Managing! 🚀**
