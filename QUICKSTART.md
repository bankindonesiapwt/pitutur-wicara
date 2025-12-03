# 🚀 Quick Start Guide - Knowledge Base Management

## ✅ System berhasil di-setup!

Knowledge Base Management System sudah siap digunakan dengan fitur:
- ✅ Admin Dashboard untuk edit KB tanpa coding
- ✅ Version Control System
- ✅ Auto-Sync dari website BI
- ✅ Export & Integration

---

## 📝 Cara Menggunakan

### 1️⃣ Jalankan Admin Dashboard

```bash
streamlit run admin_dashboard.py
```

Dashboard akan terbuka di: **http://localhost:8502** (atau port lain jika 8502 digunakan)

### 2️⃣ Login ke Admin Dashboard

- **Password default:** `admin123`
- ⚠️ **PENTING:** Ganti password ini sebelum production!

### 3️⃣ Edit Knowledge Base

Di tab **"Edit Knowledge Base"**:
1. Klik "➕ Add New Section" untuk menambah
2. Edit section yang ada dengan expand dan klik "Update"
3. Delete section yang tidak diperlukan

**Setiap perubahan otomatis di-versioning!**

### 4️⃣ Lihat Version History

Di tab **"Version History"**:
- Lihat semua perubahan yang pernah dilakukan
- Restore ke versi sebelumnya kapan saja
- Track siapa mengubah apa dan kapan

### 5️⃣ Setup Auto-Sync (Optional)

Di tab **"Auto-Sync"**:
1. Enable auto-sync
2. Tambahkan URL website BI yang ingin dimonitor:
   ```
   https://www.bi.go.id/id/tentang-bi/profil/Default.aspx
   https://www.bi.go.id/id/layanan/Default.aspx
   ```
3. Pilih interval sync (daily recommended)
4. Save configuration
5. Test dengan "Sync Now"

### 6️⃣ Export Knowledge Base

Di tab **"Export"**:
- Download sebagai Text atau JSON
- Text format untuk manual copy-paste
- JSON format untuk dynamic loading (recommended)

---

## 🔄 Integrasi dengan Chatbot

**Kabar baik:** Integrasi sudah otomatis! ✨

`app.py` sudah diupdate untuk:
1. Load knowledge base dari `knowledge_base/current_knowledge.json`
2. Fallback ke hardcoded jika file tidak ada
3. Update otomatis ketika KB berubah

**Restart chatbot setelah edit KB:**
```bash
# Stop chatbot (Ctrl+C)
streamlit run app.py
```

---

## 📁 File Structure

```
pitutur-wicara/
├── app.py                          # Chatbot utama
├── admin_dashboard.py              # Admin dashboard (JALANKAN INI!)
├── migrate_knowledge.py            # Migration script (sudah dijalankan)
├── sync_scheduler.py               # Auto-sync scheduler
├── knowledge_base/                 # KB storage
│   ├── current_knowledge.json     # ✅ KB aktif (MIGRATED)
│   ├── versions.json              # Version history
│   └── sync_config.json           # Auto-sync config
├── ADMIN_README.md                # Dokumentasi lengkap
└── QUICKSTART.md                  # File ini
```

---

## 🎯 Use Cases

### Use Case 1: Update Informasi Kontak
1. Buka admin dashboard
2. Tab "Edit Knowledge Base"
3. Expand section "KONTAK"
4. Update nomor telepon/alamat
5. Klik "Update"
6. Restart chatbot

✅ **Result:** Chatbot sekarang punya info kontak terbaru!

### Use Case 2: Tambah Layanan Baru
1. Admin dashboard → "Add New Section"
2. Title: "Layanan Baru X"
3. Content: Detail layanan
4. Save
5. Restart chatbot

✅ **Result:** User bisa tanya tentang layanan baru!

### Use Case 3: Rollback Perubahan
1. Admin dashboard → "Version History"
2. Pilih versi yang ingin dikembalikan
3. Klik "Restore This Version"
4. Restart chatbot

✅ **Result:** KB kembali ke versi sebelumnya!

---

## 🔐 Security Checklist

Sebelum deploy ke production:

- [ ] Ganti `ADMIN_PASSWORD` di `admin_dashboard.py`
- [ ] Setup environment variable untuk password
- [ ] Enable HTTPS
- [ ] Restrict admin dashboard access (IP whitelist/VPN)
- [ ] Regular backup folder `knowledge_base/`
- [ ] Setup monitoring & logging

---

## 🆘 Troubleshooting

### ❓ Dashboard tidak bisa dibuka
**Fix:** Port mungkin digunakan. Coba:
```bash
streamlit run admin_dashboard.py --server.port 8503
```

### ❓ KB tidak update di chatbot
**Fix:** 
1. Check file `knowledge_base/current_knowledge.json` ada
2. Restart `app.py`
3. Clear browser cache

### ❓ Auto-sync gagal
**Fix:**
1. Check koneksi internet
2. Verify URL masih accessible
3. Check error di dashboard

---

## 📞 Next Steps

1. **Test Edit KB:** Coba tambah/edit/delete section
2. **Test Version Control:** Restore ke versi lama
3. **Setup Auto-Sync:** Configure URLs yang ingin dimonitor
4. **Export KB:** Download dan lihat hasilnya
5. **Integration Test:** Edit KB dan test di chatbot

---

## 🎉 You're All Set!

Knowledge Base Management System sudah siap digunakan!

**Commands to remember:**
```bash
# Jalankan admin dashboard
streamlit run admin_dashboard.py

# Jalankan chatbot
streamlit run app.py

# Manual sync (scheduled)
python sync_scheduler.py
```

**Password default:** `admin123`

---

## 📚 More Info

- Baca **ADMIN_README.md** untuk dokumentasi lengkap
- Check **admin_dashboard.py** untuk customize fitur
- Edit **sync_scheduler.py** untuk custom sync logic

**Happy Managing! 🚀**
