# Deployment Configuration for Streamlit Cloud

## Prerequisites
- GitHub repository (already created: bankindonesiapwt/pitutur-wicara)
- Streamlit Cloud account (https://streamlit.io/cloud)
- Admin password configured in secrets (see step 4)

## Files Ready for Deployment
✅ app.py - Main chatbot application
✅ admin_dashboard.py - Admin dashboard (password-protected)
✅ requirements.txt - All dependencies
✅ .streamlit/config.toml - Theme configuration
✅ knowledge_base/ - KB storage with version control
✅ .gitignore - Security files excluded

## Deployment Steps

### 1. Push to GitHub
```bash
# Add all files
git add .

# Commit changes
git commit -m "Add Knowledge Base Management System for production"

# Push to main branch
git push origin main
```

### 2. Deploy Main Chatbot (app.py)

1. Go to https://share.streamlit.io/
2. Click "New app"
3. Select repository: `bankindonesiapwt/pitutur-wicara`
4. Branch: `main`
5. Main file path: `app.py`
6. App URL: Choose your custom URL (e.g., `pitutur-wicara-purwokerto`)
7. Click "Deploy"

**Your chatbot will be live at:**
`https://[your-app-name].streamlit.app`

### 3. Deploy Admin Dashboard (admin_dashboard.py)

1. Go to https://share.streamlit.io/
2. Click "New app"
3. Select repository: `bankindonesiapwt/pitutur-wicara`
4. Branch: `main`
5. Main file path: `admin_dashboard.py`
6. App URL: Choose URL (e.g., `pitutur-admin-purwokerto`)
7. Click "Deploy"

**Admin dashboard will be live at:**
`https://[your-admin-name].streamlit.app`

### 4. Configure Secrets (REQUIRED for Admin)

⚠️ **IMPORTANT**: Admin dashboard requires password in secrets

1. In Streamlit Cloud dashboard, select your admin app
2. Click "Settings" → "Secrets"
3. Add:
   ```toml
   ADMIN_PASSWORD = "your-secure-password-here"
   GEMINI_API_KEY = "your-gemini-api-key-here"
   ```
4. Admin dashboard will automatically load from secrets

**Security Best Practices:**
- Use strong password (16+ characters)
- Never commit passwords to repository
- Use different passwords for prod/dev
- Rotate passwords regularly

## Post-Deployment Checklist

- [ ] Configure secrets (ADMIN_PASSWORD and GEMINI_API_KEY)
- [ ] Test main chatbot URL
- [ ] Test admin dashboard URL
- [ ] Login to admin with configured password
- [ ] Edit a section in KB
- [ ] Verify changes reflect in chatbot (may need restart)
- [ ] Test all example questions
- [ ] Test hamburger menu sidebar
- [ ] Test on mobile device
- [ ] Share URLs with team

## Important URLs

After deployment, you'll have:

1. **Main Chatbot**: `https://[app-name].streamlit.app`
   - For end users
   - Public access
   - Auto-loads from knowledge_base/current_knowledge.json

2. **Admin Dashboard**: `https://[admin-name].streamlit.app`
   - For admin only
   - Password protected (configured in secrets)
   - Edit KB, version control, auto-sync

## Security Notes

✅ Admin password configured in Streamlit Secrets
✅ .gitignore configured to exclude sensitive files
✅ No hardcoded credentials in repository
⚠️ Use strong passwords (16+ characters, mix of letters/numbers/symbols)
⚠️ Restrict admin dashboard access via IP if possible
⚠️ Rotate API keys and passwords regularly

## Monitoring & Maintenance

### Check Deployment Status
- Streamlit Cloud dashboard shows app status
- View logs for debugging
- Monitor resource usage

### Update Knowledge Base
1. Go to admin dashboard
2. Login with your configured password
3. Edit knowledge base
4. Changes auto-saved with versioning
5. Restart main chatbot if needed (via Streamlit Cloud)

### Rollback
If something goes wrong:
1. Admin dashboard → "Version History"
2. Restore previous version
3. Or redeploy from GitHub

## Custom Domain (Optional)

To use custom domain (e.g., pitutur.bi.purwokerto.id):
1. Upgrade to Streamlit Cloud Team/Enterprise
2. Configure CNAME in DNS settings
3. Follow Streamlit documentation

## Auto-Sync Setup (Optional)

For scheduled auto-sync:
1. Use GitHub Actions
2. Create `.github/workflows/sync.yml`
3. Schedule to run `sync_scheduler.py`

## Support

Issues? Check:
- Streamlit Cloud logs
- GitHub repository
- ADMIN_README.md for detailed docs
- QUICKSTART.md for usage guide

---

**Ready to deploy! Follow the steps above.** 🚀
