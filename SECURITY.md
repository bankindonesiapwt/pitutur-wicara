# Security Policy

## 🔒 Security Best Practices

### Credentials Management

**NEVER commit sensitive information to the repository:**
- ❌ API Keys
- ❌ Passwords
- ❌ Tokens
- ❌ Private keys
- ❌ Environment variables with secrets

### For Local Development

1. **Create `.streamlit/secrets.toml`** (gitignored):
```toml
GEMINI_API_KEY = "your-api-key-here"
ADMIN_PASSWORD = "your-secure-password"
```

2. **Or use environment variables**:
```bash
# Windows CMD
set GEMINI_API_KEY=your-key
set ADMIN_PASSWORD=your-password

# Windows PowerShell
$env:GEMINI_API_KEY="your-key"
$env:ADMIN_PASSWORD="your-password"

# Linux/Mac
export GEMINI_API_KEY=your-key
export ADMIN_PASSWORD=your-password
```

### For Production (Streamlit Cloud)

1. Go to your app settings in Streamlit Cloud
2. Navigate to **Settings → Secrets**
3. Add secrets in TOML format:
```toml
GEMINI_API_KEY = "your-production-api-key"
ADMIN_PASSWORD = "your-strong-production-password"
```

### Password Requirements

**Admin Password:**
- Minimum 16 characters
- Mix of uppercase and lowercase letters
- Include numbers and special characters
- Avoid dictionary words
- Use unique password (not reused elsewhere)

**Example strong password generator:**
```python
import secrets
import string

def generate_password(length=20):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for i in range(length))

print(generate_password())
```

### API Key Security

**Google Gemini API Key:**
1. Generate at: https://ai.google.dev
2. Store in secrets.toml or environment variable
3. Rotate keys every 90 days
4. Use separate keys for dev/staging/production
5. Set API restrictions in Google Cloud Console
6. Monitor usage in Google AI Studio

### .gitignore Configuration

Verify these patterns are in `.gitignore`:
```
# Secrets
.streamlit/secrets.toml
secrets.toml
.env
.env.*
*.key
*.pem
credentials.json

# API Keys
*api_key*
*token*
*secret*
```

### Checking for Exposed Secrets

**Before committing:**
```bash
# Check git status
git status

# Check what will be committed
git diff --cached

# Search for potential secrets
git grep -i "password\|api.*key\|secret\|token" HEAD
```

**After committing (if you accidentally committed secrets):**
1. **IMMEDIATELY rotate all exposed credentials**
2. Remove from git history:
```bash
# Remove file from history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .streamlit/secrets.toml" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (WARNING: rewrites history)
git push origin --force --all
```
3. **Better option:** Use [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/)

### Repository Access Control

**GitHub Settings:**
1. Make admin dashboard URL private (share only with authorized personnel)
2. Enable GitHub 2FA (Two-Factor Authentication)
3. Use GitHub branch protection rules
4. Review repository access regularly
5. Use GitHub Secrets for CI/CD workflows

### Monitoring

**Regular Security Checks:**
- [ ] Review Streamlit Cloud logs weekly
- [ ] Monitor API usage in Google AI Studio
- [ ] Check for unauthorized access attempts
- [ ] Audit admin dashboard access logs
- [ ] Review and rotate credentials quarterly

### Reporting Security Issues

If you discover a security vulnerability:
1. **DO NOT** create a public GitHub issue
2. Contact repository owner directly via:
   - GitHub: [@bankindonesiapwt](https://github.com/bankindonesiapwt)
   - Email: [contact admin for email]
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### Security Checklist

**Before Deployment:**
- [ ] No hardcoded passwords in code
- [ ] No API keys in repository
- [ ] `.gitignore` properly configured
- [ ] Secrets configured in Streamlit Cloud
- [ ] Strong passwords set (16+ chars)
- [ ] API keys restricted (if possible)
- [ ] Admin dashboard URL not publicly shared
- [ ] 2FA enabled on GitHub account

**After Deployment:**
- [ ] Test authentication works
- [ ] Verify secrets are loaded correctly
- [ ] Check logs for errors
- [ ] Test password change process
- [ ] Document credential locations securely
- [ ] Share admin credentials securely (not via public channels)

### Secure Credential Sharing

**For Team Members:**
1. **NEVER share via:**
   - Email
   - SMS
   - Public chat (WhatsApp groups, Slack public channels)
   - GitHub issues/discussions
   - Code comments

2. **INSTEAD use:**
   - Password managers (1Password, LastPass, Bitwarden)
   - Encrypted messaging (Signal, encrypted email)
   - Secure key management systems
   - In-person handoff for critical credentials

### Incident Response

**If credentials are compromised:**
1. **Immediate Actions:**
   - Rotate all affected credentials immediately
   - Change admin password
   - Generate new API keys
   - Review access logs
   - Notify team members

2. **Investigation:**
   - Identify scope of exposure
   - Review recent access logs
   - Check for unauthorized changes
   - Document timeline

3. **Prevention:**
   - Update security procedures
   - Enhance monitoring
   - Conduct security training
   - Review and update this policy

---

## 📞 Security Contacts

- **Repository Owner:** [@bankindonesiapwt](https://github.com/bankindonesiapwt)
- **Security Issues:** Report via private channels only

---

*Last Updated: December 3, 2025*
