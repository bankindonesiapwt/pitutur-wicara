import streamlit as st
import json
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import hashlib

# Page config
st.set_page_config(
    page_title="Admin Dashboard - PITUTUR-Wicara",
    page_icon="🔧",
    layout="wide"
)

# File paths
KNOWLEDGE_BASE_DIR = "knowledge_base"
VERSIONS_FILE = os.path.join(KNOWLEDGE_BASE_DIR, "versions.json")
CURRENT_KB_FILE = os.path.join(KNOWLEDGE_BASE_DIR, "current_knowledge.json")
SYNC_CONFIG_FILE = os.path.join(KNOWLEDGE_BASE_DIR, "sync_config.json")

# Create directory if not exists
os.makedirs(KNOWLEDGE_BASE_DIR, exist_ok=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False

# Authentication - Load from secrets or environment variable
ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", os.getenv("ADMIN_PASSWORD", "change-this-password"))

def authenticate():
    """Simple authentication for admin access"""
    st.sidebar.title("🔐 Admin Login")
    password = st.sidebar.text_input("Password", type="password")
    
    if st.sidebar.button("Login"):
        if password == ADMIN_PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.sidebar.error("Password salah!")
    
    if st.session_state.authenticated:
        st.sidebar.success("✅ Logged in as Admin")
        if st.sidebar.button("Logout"):
            st.session_state.authenticated = False
            st.rerun()

def load_knowledge_base():
    """Load current knowledge base"""
    if os.path.exists(CURRENT_KB_FILE):
        with open(CURRENT_KB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "sections": [],
        "last_updated": None,
        "version": "1.0.0"
    }

def save_knowledge_base(kb_data, commit_message=""):
    """Save knowledge base with versioning"""
    # Generate version hash
    content_hash = hashlib.md5(json.dumps(kb_data, sort_keys=True).encode()).hexdigest()[:8]
    
    # Load version history
    versions = load_versions()
    
    # Create new version
    version_number = len(versions) + 1
    version_data = {
        "version": f"{version_number}.0.0",
        "hash": content_hash,
        "timestamp": datetime.now().isoformat(),
        "commit_message": commit_message,
        "data": kb_data
    }
    
    # Save version
    version_file = os.path.join(KNOWLEDGE_BASE_DIR, f"version_{version_number}_{content_hash}.json")
    with open(version_file, 'w', encoding='utf-8') as f:
        json.dump(version_data, f, indent=2, ensure_ascii=False)
    
    # Update versions list
    versions.append({
        "version": version_data["version"],
        "hash": content_hash,
        "timestamp": version_data["timestamp"],
        "commit_message": commit_message,
        "file": version_file
    })
    
    with open(VERSIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(versions, f, indent=2, ensure_ascii=False)
    
    # Update current knowledge base
    kb_data["last_updated"] = datetime.now().isoformat()
    kb_data["version"] = version_data["version"]
    
    with open(CURRENT_KB_FILE, 'w', encoding='utf-8') as f:
        json.dump(kb_data, f, indent=2, ensure_ascii=False)
    
    return version_data["version"]

def load_versions():
    """Load version history"""
    if os.path.exists(VERSIONS_FILE):
        with open(VERSIONS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def restore_version(version_file):
    """Restore knowledge base from a specific version"""
    with open(version_file, 'r', encoding='utf-8') as f:
        version_data = json.load(f)
    
    # Save as current
    with open(CURRENT_KB_FILE, 'w', encoding='utf-8') as f:
        json.dump(version_data["data"], f, indent=2, ensure_ascii=False)
    
    return True

def fetch_bi_website_content(url):
    """Fetch content from BI website for auto-sync"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract text content (customize based on BI website structure)
        content = soup.get_text(separator='\n', strip=True)
        
        return {
            "success": True,
            "content": content,
            "url": url,
            "fetched_at": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "url": url
        }

def load_sync_config():
    """Load auto-sync configuration"""
    if os.path.exists(SYNC_CONFIG_FILE):
        with open(SYNC_CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "enabled": False,
        "urls": [],
        "last_sync": None,
        "sync_interval": "daily"
    }

def save_sync_config(config):
    """Save auto-sync configuration"""
    with open(SYNC_CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def export_to_text(kb_data):
    """Export knowledge base to text format for app.py"""
    text_content = "INFORMASI BANK INDONESIA KANTOR PERWAKILAN PURWOKERTO\n\n"
    
    for section in kb_data.get("sections", []):
        text_content += "=" * 47 + "\n"
        text_content += section.get("title", "").upper() + "\n"
        text_content += "=" * 47 + "\n\n"
        text_content += section.get("content", "") + "\n\n"
    
    return text_content

# Main App
def main():
    authenticate()
    
    if not st.session_state.authenticated:
        st.title("🔐 Admin Dashboard - PITUTUR-Wicara")
        st.info("Silakan login untuk mengakses admin dashboard")
        return
    
    st.title("🔧 Admin Dashboard - Knowledge Base Management")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 Edit Knowledge Base",
        "📜 Version History",
        "🔄 Auto-Sync",
        "📊 Export"
    ])
    
    # Tab 1: Edit Knowledge Base
    with tab1:
        st.header("Edit Knowledge Base")
        
        kb_data = load_knowledge_base()
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info(f"📌 Current Version: {kb_data.get('version', 'N/A')} | Last Updated: {kb_data.get('last_updated', 'Never')}")
        with col2:
            if st.button("➕ Add New Section"):
                st.session_state.edit_mode = True
        
        st.markdown("---")
        
        # Add new section
        if st.session_state.edit_mode:
            with st.form("new_section_form"):
                st.subheader("Add New Section")
                new_title = st.text_input("Section Title")
                new_content = st.text_area("Section Content", height=200)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("💾 Save Section"):
                        if new_title and new_content:
                            if "sections" not in kb_data:
                                kb_data["sections"] = []
                            
                            kb_data["sections"].append({
                                "title": new_title,
                                "content": new_content,
                                "created_at": datetime.now().isoformat()
                            })
                            
                            version = save_knowledge_base(kb_data, f"Added section: {new_title}")
                            st.success(f"✅ Section saved! Version: {version}")
                            st.session_state.edit_mode = False
                            st.rerun()
                        else:
                            st.error("Title and content are required!")
                
                with col2:
                    if st.form_submit_button("❌ Cancel"):
                        st.session_state.edit_mode = False
                        st.rerun()
        
        # Display and edit existing sections
        st.subheader("Existing Sections")
        
        if not kb_data.get("sections"):
            st.warning("No sections available. Add a new section to get started.")
        else:
            for idx, section in enumerate(kb_data["sections"]):
                with st.expander(f"📄 {section.get('title', 'Untitled')}", expanded=False):
                    with st.form(f"edit_section_{idx}"):
                        title = st.text_input("Title", value=section.get("title", ""), key=f"title_{idx}")
                        content = st.text_area("Content", value=section.get("content", ""), height=200, key=f"content_{idx}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("💾 Update"):
                                kb_data["sections"][idx]["title"] = title
                                kb_data["sections"][idx]["content"] = content
                                kb_data["sections"][idx]["updated_at"] = datetime.now().isoformat()
                                
                                version = save_knowledge_base(kb_data, f"Updated section: {title}")
                                st.success(f"✅ Section updated! Version: {version}")
                                st.rerun()
                        
                        with col2:
                            if st.form_submit_button("🗑️ Delete"):
                                kb_data["sections"].pop(idx)
                                version = save_knowledge_base(kb_data, f"Deleted section: {section.get('title')}")
                                st.success(f"✅ Section deleted! Version: {version}")
                                st.rerun()
    
    # Tab 2: Version History
    with tab2:
        st.header("📜 Version History")
        
        versions = load_versions()
        
        if not versions:
            st.info("No version history available yet.")
        else:
            st.write(f"**Total Versions:** {len(versions)}")
            
            for version in reversed(versions):
                with st.expander(f"Version {version['version']} - {version['timestamp'][:19]}"):
                    st.write(f"**Hash:** `{version['hash']}`")
                    st.write(f"**Commit Message:** {version.get('commit_message', 'No message')}")
                    st.write(f"**Timestamp:** {version['timestamp']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("🔄 Restore This Version", key=f"restore_{version['version']}"):
                            if restore_version(version['file']):
                                st.success(f"✅ Restored to version {version['version']}")
                                st.rerun()
                    
                    with col2:
                        if st.button("👁️ View Details", key=f"view_{version['version']}"):
                            with open(version['file'], 'r', encoding='utf-8') as f:
                                data = json.load(f)
                                st.json(data)
    
    # Tab 3: Auto-Sync
    with tab3:
        st.header("🔄 Auto-Sync Configuration")
        
        sync_config = load_sync_config()
        
        st.subheader("Sync Settings")
        
        enabled = st.checkbox("Enable Auto-Sync", value=sync_config.get("enabled", False))
        
        st.write("**URLs to Monitor:**")
        urls = st.text_area(
            "Enter URLs (one per line)",
            value="\n".join(sync_config.get("urls", [])),
            height=150
        )
        
        sync_interval = st.selectbox(
            "Sync Interval",
            ["hourly", "daily", "weekly"],
            index=["hourly", "daily", "weekly"].index(sync_config.get("sync_interval", "daily"))
        )
        
        if st.button("💾 Save Sync Configuration"):
            sync_config["enabled"] = enabled
            sync_config["urls"] = [url.strip() for url in urls.split("\n") if url.strip()]
            sync_config["sync_interval"] = sync_interval
            save_sync_config(sync_config)
            st.success("✅ Sync configuration saved!")
        
        st.markdown("---")
        st.subheader("Manual Sync")
        
        if st.button("🔄 Sync Now"):
            with st.spinner("Fetching content from URLs..."):
                results = []
                for url in sync_config.get("urls", []):
                    result = fetch_bi_website_content(url)
                    results.append(result)
                
                # Display results
                for result in results:
                    if result["success"]:
                        st.success(f"✅ Synced: {result['url']}")
                        with st.expander("View Content"):
                            st.text_area("Fetched Content", result["content"][:1000] + "...", height=200)
                    else:
                        st.error(f"❌ Failed: {result['url']} - {result['error']}")
                
                # Update last sync time
                sync_config["last_sync"] = datetime.now().isoformat()
                save_sync_config(sync_config)
        
        if sync_config.get("last_sync"):
            st.info(f"Last Sync: {sync_config['last_sync'][:19]}")
    
    # Tab 4: Export
    with tab4:
        st.header("📊 Export Knowledge Base")
        
        kb_data = load_knowledge_base()
        
        st.subheader("Export Formats")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Export as Text (for app.py)**")
            text_content = export_to_text(kb_data)
            st.download_button(
                label="📥 Download as .txt",
                data=text_content,
                file_name="knowledge_base.txt",
                mime="text/plain"
            )
        
        with col2:
            st.write("**Export as JSON**")
            json_content = json.dumps(kb_data, indent=2, ensure_ascii=False)
            st.download_button(
                label="📥 Download as .json",
                data=json_content,
                file_name="knowledge_base.json",
                mime="application/json"
            )
        
        st.markdown("---")
        st.subheader("Preview")
        
        with st.expander("📄 Text Preview"):
            st.code(text_content, language="text")
        
        with st.expander("📋 JSON Preview"):
            st.json(kb_data)
        
        st.markdown("---")
        st.subheader("Integration Instructions")
        
        st.info("""
        **How to use exported knowledge base in app.py:**
        
        1. Download the text file using the button above
        2. Open `app.py` in your code editor
        3. Find the `BUILTIN_KNOWLEDGE` variable
        4. Replace the content with the exported text
        5. Save and restart the application
        
        **Or use JSON import (recommended):**
        
        Add this function to `app.py`:
        ```python
        def load_knowledge_from_json():
            with open('knowledge_base/current_knowledge.json', 'r', encoding='utf-8') as f:
                kb_data = json.load(f)
            return export_to_text(kb_data)
        ```
        """)

if __name__ == "__main__":
    main()
