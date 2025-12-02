# 🔑 API Key Setup Guide

## ⚠️ Important: API Key Leaked

API key yang sebelumnya hardcoded sudah **leaked** dan **diblokir** oleh Google. Anda perlu membuat API key baru.

## 📝 Steps to Fix

### 1. Generate New Gemini API Key

1. Buka https://makersuite.google.com/app/apikey
2. Login dengan Google account
3. Klik **"Create API Key"**
4. Copy API key yang baru (format: `AIzaSy...`)

### 2. Configure in Streamlit Cloud (PRODUCTION)

1. Buka Streamlit Cloud dashboard
2. Pilih app **lisa-bi-purwokerto**
3. Klik **"Settings"** (⚙️)
4. Pilih **"Secrets"**
5. Tambahkan:
   ```toml
   GEMINI_API_KEY = "AIzaSy_YOUR_NEW_API_KEY_HERE"
   ```
6. Klik **"Save"**
7. App akan auto-restart

### 3. Configure Locally (DEVELOPMENT)

**Option A: Using Streamlit Secrets (Recommended)**

1. Buat file `.streamlit/secrets.toml`:
   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```

2. Edit `.streamlit/secrets.toml`:
   ```toml
   GEMINI_API_KEY = "AIzaSy_YOUR_NEW_API_KEY_HERE"
   ```

3. File ini sudah di-gitignore, aman dari leak

**Option B: Using Environment Variable**

```bash
# Windows (Command Prompt)
set GEMINI_API_KEY=AIzaSy_YOUR_NEW_API_KEY_HERE

# Windows (PowerShell)
$env:GEMINI_API_KEY="AIzaSy_YOUR_NEW_API_KEY_HERE"

# Linux/Mac
export GEMINI_API_KEY=AIzaSy_YOUR_NEW_API_KEY_HERE
```

### 4. Verify Setup

1. Restart aplikasi
2. Coba chat dengan pertanyaan
3. Jika masih error, check:
   - API key sudah benar?
   - API key sudah aktif?
   - Billing sudah enable di Google Cloud?

## 🔐 Security Best Practices

### ✅ DO:
- Store API keys in Streamlit Secrets
- Use environment variables
- Never commit secrets to git
- Rotate API keys regularly
- Restrict API key usage (HTTP referrers, IP addresses)

### ❌ DON'T:
- Hardcode API keys in source code
- Commit `.streamlit/secrets.toml` to git
- Share API keys in public channels
- Use same API key across multiple projects

## 🛡️ API Key Security in Google Cloud

1. Buka https://console.cloud.google.com/apis/credentials
2. Pilih API key yang baru dibuat
3. Klik **"Edit"**
4. **Application restrictions:**
   - HTTP referrers: `https://*.streamlit.app/*`
5. **API restrictions:**
   - Restrict key: Generative Language API
6. Save

## 📊 Usage Monitoring

Monitor API usage di:
- Google Cloud Console: https://console.cloud.google.com/apis/dashboard
- Check quota dan billing
- Set up alerts untuk unusual usage

## 🆘 Troubleshooting

### Error: "API key was reported as leaked"
**Solution:** Generate new API key dan ikuti steps di atas.

### Error: "PERMISSION_DENIED"
**Solution:** 
- Check API key valid
- Enable Generative Language API di Google Cloud
- Check billing sudah aktif

### Error: "RESOURCE_EXHAUSTED"
**Solution:**
- Quota habis
- Upgrade billing plan
- Wait untuk quota reset

### Error: "API key tidak dikonfigurasi"
**Solution:**
- Check secrets.toml exists
- Check GEMINI_API_KEY spelled correctly
- Restart aplikasi

## 📧 Need Help?

If you're still having issues:
1. Check Streamlit Cloud logs
2. Verify API key di Google Cloud Console
3. Test API key dengan curl:
   ```bash
   curl "https://generativelanguage.googleapis.com/v1/models?key=YOUR_API_KEY"
   ```

---

**After setup, delete or revoke the old leaked API key from Google Cloud Console!**
