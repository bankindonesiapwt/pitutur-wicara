import streamlit as st
import json
import re
from datetime import datetime
from PyPDF2 import PdfReader
import requests

# Page config
st.set_page_config(
    page_title="Bank Indonesia Chatbot",
    page_icon="🏦",
    layout="wide"
)

# Custom CSS - Light Theme
st.markdown("""
<style>
    .stApp {
        background: #f5f7fa;
    }
    .main-header {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        color: white;
    }
    .main-header h1 {
        color: white !important;
    }
    .main-header p {
        color: #e0e7ff !important;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .user-message {
        background: #2563eb;
        color: white;
        margin-left: 20%;
    }
    .assistant-message {
        background: white;
        color: #1f2937;
        margin-right: 20%;
        border: 1px solid #e5e7eb;
    }
    .source-box {
        background: #eff6ff;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2563eb;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'documents' not in st.session_state:
    st.session_state.documents = []
if 'api_key' not in st.session_state:
    st.session_state.api_key = ''

# Functions
def chunk_text(text, chunk_size=1000, overlap=200):
    """Split text into overlapping chunks"""
    chunks = []
    start = 0
    text_len = len(text)
    
    while start < text_len:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    
    return chunks

def create_embedding_features(text):
    """Create simple embedding features for retrieval"""
    words = text.lower().split()
    return {
        'text': text,
        'words': set(words),
        'length': len(text),
        'keywords': [w for w in words if len(w) > 4][:30]
    }

def find_relevant_chunks(query, documents, top_k=3):
    """Find most relevant document chunks"""
    query_words = set(query.lower().split())
    
    scored_docs = []
    for doc in documents:
        score = 0
        doc_words = doc['features']['words']
        
        # Word overlap score
        overlap = query_words.intersection(doc_words)
        score += len(overlap) * 2
        
        # Keyword match
        for keyword in doc['features']['keywords']:
            if keyword in query.lower():
                score += 3
        
        if score > 0:
            scored_docs.append({
                'doc': doc,
                'score': score
            })
    
    scored_docs.sort(key=lambda x: x['score'], reverse=True)
    return [item['doc'] for item in scored_docs[:top_k]]

def extract_text_from_pdf(pdf_file):
    """Extract text from PDF file"""
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def process_document(file, filename):
    """Process uploaded document"""
    try:
        if filename.endswith('.pdf'):
            text = extract_text_from_pdf(file)
        else:
            text = file.read().decode('utf-8')
        
        # Clean text
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Chunk text
        chunks = chunk_text(text)
        
        # Create document entries
        docs = []
        for i, chunk in enumerate(chunks):
            docs.append({
                'id': f"{filename}_{i}",
                'filename': filename,
                'chunk': chunk,
                'features': create_embedding_features(chunk),
                'index': i,
                'total_chunks': len(chunks)
            })
        
        return docs, None
    except Exception as e:
        return None, str(e)

def chat_with_ai(user_message, relevant_docs, api_key):
    """Send message to Gemini AI using REST API"""
    try:
        # Build context from relevant documents
        context = ""
        if relevant_docs:
            context = "Informasi dari dokumen Bank Indonesia:\n\n"
            for i, doc in enumerate(relevant_docs):
                context += f"[Dokumen {i+1}: {doc['filename']}, Bagian {doc['index']+1}/{doc['total_chunks']}]\n"
                context += f"{doc['chunk']}\n\n"
        
        # Build prompt
        if context:
            prompt = f"""Kamu adalah asisten chatbot Bank Indonesia yang membantu menjawab pertanyaan tentang Bank Indonesia.

{context}

Pertanyaan: {user_message}

Instruksi:
- Jawab berdasarkan informasi dari dokumen di atas
- Sebutkan dari dokumen mana informasi tersebut berasal
- Jika informasi tidak lengkap di dokumen, tambahkan pengetahuan umum tentang Bank Indonesia
- Berikan link ke website resmi bi.go.id jika relevan
- Jawab dalam Bahasa Indonesia dengan ramah, profesional, dan informatif
- Gunakan format yang jelas dengan paragraf dan bullet points jika perlu"""
        else:
            prompt = f"""Kamu adalah asisten chatbot Bank Indonesia yang membantu menjawab pertanyaan.

Pertanyaan: {user_message}

Instruksi:
- Jawab berdasarkan pengetahuan umum tentang Bank Indonesia
- Berikan informasi yang akurat dan bermanfaat
- Sertakan link ke website resmi bi.go.id untuk informasi lebih lanjut
- Sarankan user untuk mengupload dokumen resmi BI untuk informasi lebih detail
- Jawab dalam Bahasa Indonesia dengan ramah dan profesional"""
        
        # Call Gemini API using REST - Gunakan model terbaru yang tersedia
        models_to_try = [
            "gemini-2.5-flash",           # Terbaru & tercepat
            "gemini-2.0-flash",           # Alternatif 1
            "gemini-2.5-flash-lite",      # Alternatif 2
            "gemini-2.0-flash-lite",      # Alternatif 3
        ]
        
        last_error = None
        
        for model_name in models_to_try:
            try:
                url = f"https://generativelanguage.googleapis.com/v1/models/{model_name}:generateContent?key={api_key}"
                
                headers = {
                    'Content-Type': 'application/json'
                }
                
                data = {
                    "contents": [{
                        "parts": [{
                            "text": prompt
                        }]
                    }]
                }
                
                response = requests.post(url, headers=headers, json=data, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    if 'candidates' in result and len(result['candidates']) > 0:
                        text = result['candidates'][0]['content']['parts'][0]['text']
                        return text, relevant_docs
                else:
                    last_error = response.json() if response.content else "Unknown error"
                    continue  # Try next model
            except Exception as e:
                last_error = str(e)
                continue  # Try next model
        
        # Jika semua model gagal
        return f"❌ Tidak ada model yang berhasil. Last error: {last_error}\n\nSilakan jalankan check_models.py untuk cek model yang tersedia.", None
    
    except Exception as e:
        return f"❌ Error: {str(e)}", None

# Main App
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏦 Bank Indonesia Chatbot</h1>
        <p style="color: #e0e7ff; margin-top: 0.5rem;">
            Asisten pintar untuk menjawab pertanyaan tentang Bank Indonesia dengan data valid dan akurat
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Pengaturan")
        
        # API Key input
        api_key = st.text_input(
            "Google Gemini API Key",
            value=st.session_state.api_key,
            type="password",
            help="Dapatkan API key gratis di https://ai.google.dev"
        )
        
        if api_key:
            st.session_state.api_key = api_key
            st.success("✅ API Key tersimpan!")
        else:
            st.warning("⚠️ Masukkan API Key terlebih dahulu")
        
        st.markdown("---")
        
        # Document upload
        st.header("📄 Upload Dokumen")
        st.caption(f"Dokumen tersimpan: {len(st.session_state.documents)}")
        
        uploaded_file = st.file_uploader(
            "Upload PDF atau TXT",
            type=['pdf', 'txt'],
            help="Upload dokumen resmi Bank Indonesia"
        )
        
        if uploaded_file:
            with st.spinner("⏳ Memproses dokumen..."):
                docs, error = process_document(uploaded_file, uploaded_file.name)
                
                if error:
                    st.error(f"❌ Error: {error}")
                else:
                    st.session_state.documents.extend(docs)
                    st.success(f"✅ Berhasil! {len(docs)} bagian dokumen ditambahkan")
                    st.experimental_rerun()
        
        if st.session_state.documents:
            if st.button("🗑️ Hapus Semua Dokumen"):
                st.session_state.documents = []
                st.experimental_rerun()
        
        st.markdown("---")
        
        # Info
        st.header("ℹ️ Informasi")
        st.markdown("""
        **Cara Pakai:**
        1. Masukkan API Key (gratis)
        2. Upload dokumen BI (opsional)
        3. Mulai bertanya!
        
        **Download Dokumen BI:**
        - [Publikasi BI](https://www.bi.go.id/id/publikasi)
        - [Statistik BI](https://www.bi.go.id/id/statistik)
        - [Laporan BI](https://www.bi.go.id/id/publikasi/laporan)
        """)
    
    # Main chat area
    col1, col2 = st.columns([3, 1])
    
    with col2:
        st.metric("💬 Total Pesan", len(st.session_state.messages))
        st.metric("📚 Dokumen", len(st.session_state.documents))
    
    # Display chat messages
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            if message['role'] == 'user':
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>👤 Anda:</strong><br/>
                    {message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <strong>🤖 Asisten BI:</strong><br/>
                    {message['content']}
                </div>
                """, unsafe_allow_html=True)
                
                if message.get('sources'):
                    with st.expander("📄 Lihat Sumber Dokumen"):
                        for i, source in enumerate(message['sources']):
                            st.markdown(f"""
                            **{i+1}. {source['filename']}**  
                            Bagian {source['index']+1} dari {source['total_chunks']}
                            """)
                            st.text_area(
                                "Preview:",
                                source['chunk'][:300] + "...",
                                height=100,
                                key=f"source_{message.get('id', '')}_{i}",
                                disabled=True
                            )
    
    # Chat input
    st.markdown("---")
    
    # Example questions
    st.subheader("💡 Contoh Pertanyaan:")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏛️ Apa itu Bank Indonesia?"):
            st.session_state.example_query = "Apa itu Bank Indonesia?"
    with col2:
        if st.button("📊 Info Suku Bunga BI"):
            st.session_state.example_query = "Berapa suku bunga BI terkini?"
    with col3:
        if st.button("📞 Kontak Bank Indonesia"):
            st.session_state.example_query = "Bagaimana cara menghubungi Bank Indonesia?"
    
    # User input
    user_input = st.text_input("Ketik pertanyaan Anda tentang Bank Indonesia...", key="user_input")
    
    # Handle example query
    if 'example_query' in st.session_state:
        user_input = st.session_state.example_query
        del st.session_state.example_query
    
    if user_input:
        if not st.session_state.api_key:
            st.error("⚠️ Silakan masukkan API Key di sidebar terlebih dahulu!")
            return
        
        # Add user message
        st.session_state.messages.append({
            'role': 'user',
            'content': user_input
        })
        
        # Find relevant documents
        relevant_docs = find_relevant_chunks(
            user_input,
            st.session_state.documents,
            top_k=3
        )
        
        # Get AI response
        with st.spinner("🤔 Sedang berpikir..."):
            response, sources = chat_with_ai(
                user_input,
                relevant_docs,
                st.session_state.api_key
            )
        
        # Add assistant message
        st.session_state.messages.append({
            'role': 'assistant',
            'content': response,
            'sources': sources,
            'id': datetime.now().isoformat()
        })
        
        st.experimental_rerun()

if __name__ == "__main__":
    main()