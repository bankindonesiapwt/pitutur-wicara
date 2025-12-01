import streamlit as st
import json
import re
from datetime import datetime
from PyPDF2 import PdfReader
import requests
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model (cached)
@st.cache_resource
def load_embedding_model():
    """Load sentence transformer model for semantic search"""
    return SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Page config
st.set_page_config(
    page_title="Bank Indonesia Chatbot",
    page_icon="🏦",
    layout="wide"
)

# Custom CSS - WhatsApp-style Mobile-Friendly Theme
st.markdown("""
<style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background: #efeae2;
        max-width: 100%;
    }
    
    /* Sticky Header - WhatsApp Style */
    .wa-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 999;
        background: #2563eb;
        padding: 0.75rem 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin: 0;
    }
    
    /* Add padding to main content to prevent overlap with fixed header */
    .block-container {
        padding-top: 3.5rem !important;
    }
    .wa-header h3 {
        color: white !important;
        margin: 0 !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
    }
    
    /* Chat messages - WhatsApp Style */
    .chat-message {
        padding: 0.6rem 0.8rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        max-width: 80%;
        word-wrap: break-word;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        font-size: 0.95rem;
        line-height: 1.4;
    }
    .user-message {
        background: #dbeafe;
        color: #000;
        margin-left: auto;
        margin-right: 0;
        border-radius: 8px 0 8px 8px;
    }
    .assistant-message {
        background: white;
        color: #000;
        margin-right: auto;
        margin-left: 0;
        border-radius: 0 8px 8px 8px;
    }
    
    /* Mobile optimization */
    @media (max-width: 768px) {
        .chat-message {
            max-width: 85%;
            font-size: 0.9rem;
        }
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: #f0f2f5;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'documents' not in st.session_state:
    st.session_state.documents = []
if 'api_key' not in st.session_state:
    st.session_state.api_key = 'AIzaSyD7_PAF98KwkGPGSHLWPmBF1GsXDAyxEA8'

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

def create_embedding_features(text, model=None):
    """Create embedding vector for semantic search"""
    words = text.lower().split()
    features = {
        'text': text,
        'words': set(words),
        'length': len(text),
        'keywords': [w for w in words if len(w) > 4][:30]
    }
    
    # Add semantic embedding if model is provided
    if model is not None:
        try:
            features['embedding'] = model.encode(text, convert_to_numpy=True)
        except:
            features['embedding'] = None
    
    return features

def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors"""
    if vec1 is None or vec2 is None:
        return 0.0
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot_product / (norm1 * norm2)

def find_relevant_chunks(query, documents, model=None, top_k=5):
    """Find most relevant document chunks using semantic search"""
    if not documents:
        return []
    
    query_lower = query.lower()
    
    # Generate query embedding for semantic search
    query_embedding = None
    if model is not None:
        try:
            query_embedding = model.encode(query, convert_to_numpy=True)
        except:
            pass
    
    scored_docs = []
    for doc in documents:
        score = 0.0
        
        # SEMANTIC SIMILARITY (Primary scoring method)
        if query_embedding is not None and doc['features'].get('embedding') is not None:
            semantic_score = cosine_similarity(query_embedding, doc['features']['embedding'])
            score += semantic_score * 100  # Scale to 0-100
        
        # KEYWORD MATCHING (Fallback/boost)
        doc_text = doc['chunk'].lower()
        query_words = set(query_lower.split())
        doc_words = doc['features']['words']
        
        # Word overlap
        overlap = query_words.intersection(doc_words)
        score += len(overlap) * 2
        
        # Exact phrase match
        if len(query) > 3 and query_lower in doc_text:
            score += 10
        
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

def process_document(file, filename, model=None):
    """Process uploaded document with semantic embeddings"""
    try:
        if filename.endswith('.pdf'):
            text = extract_text_from_pdf(file)
        else:
            text = file.read().decode('utf-8')
        
        # Clean text
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Chunk text
        chunks = chunk_text(text)
        
        # Create document entries with embeddings
        docs = []
        for i, chunk in enumerate(chunks):
            docs.append({
                'id': f"{filename}_{i}",
                'filename': filename,
                'chunk': chunk,
                'features': create_embedding_features(chunk, model),
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
    # Load embedding model
    try:
        embedding_model = load_embedding_model()
        model_loaded = True
    except Exception as e:
        st.warning(f"⚠️ Semantic search tidak tersedia: {str(e)}\nMenggunakan keyword search sebagai fallback.")
        embedding_model = None
        model_loaded = False
    # WhatsApp-style Sticky Header
    st.markdown("""
    <div class="wa-header">
        <h3>🏦 Bank Indonesia Chatbot</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Pengaturan")
        
        # API Key is pre-configured
        api_key = st.session_state.api_key
        st.success("✅ API Key siap digunakan!")
        
        st.markdown("---")
        
        # Document upload
        st.header("� Upload Dokumen")
        if model_loaded:
            st.caption(f"� Semantic search: ✅ Aktif | Dokumen: {len(st.session_state.documents)}")
        else:
            st.caption(f"� Dokumen tersimpan: {len(st.session_state.documents)}")
        
        uploaded_file = st.file_uploader(
            "Upload PDF atau TXT",
            type=['pdf', 'txt'],
            help="Upload dokumen resmi Bank Indonesia",
            key="file_uploader"
        )
        
        if uploaded_file and uploaded_file.name not in [doc.get('source_file', '') for doc in st.session_state.get('uploaded_files', [])]:
            with st.spinner("⏳ Memproses dokumen & membuat embeddings..."):
                docs, error = process_document(uploaded_file, uploaded_file.name, embedding_model)
                
                if error:
                    st.error(f"❌ Error: {error}")
                else:
                    st.session_state.documents.extend(docs)
                    
                    # Track uploaded files
                    if 'uploaded_files' not in st.session_state:
                        st.session_state.uploaded_files = []
                    st.session_state.uploaded_files.append({
                        'source_file': uploaded_file.name,
                        'timestamp': datetime.now().isoformat()
                    })
                    
                    st.success(f"✅ Berhasil! {len(docs)} bagian dokumen ditambahkan")
                    st.rerun()
        
        if st.session_state.documents:
            st.info(f"📚 {len(set([d['filename'] for d in st.session_state.documents]))} file terproses")
            if st.button("🗑️ Hapus Semua Dokumen"):
                st.session_state.documents = []
                st.session_state.uploaded_files = []
                st.success("✅ Semua dokumen dihapus")
                st.rerun()
        
        st.markdown("---")
        
        # Info
        st.header("ℹ️ Informasi")
        st.markdown("""
        **Cara Pakai:**
        1. Masukkan API Key (gratis)
        2. Upload dokumen BI (opsional)
        3. Mulai bertanya!
        
        **Teknologi:**
        - 🤖 Gemini 2.5 Flash AI
        - 🔍 Semantic Search (sentence-transformers)
        - 📄 RAG (Retrieval-Augmented Generation)
        
        **Download Dokumen BI:**
        - [Publikasi BI](https://www.bi.go.id/id/publikasi)
        - [Statistik BI](https://www.bi.go.id/id/statistik)
        - [Laporan BI](https://www.bi.go.id/id/publikasi/laporan)
        """)
    
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
                    with st.expander("� Lihat Sumber Dokumen"):
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
    user_input = st.text_input("Ketik pertanyaan Anda tentang Bank Indonesia...", key="user_input_field", value="")
    
    # Submit button
    submit_button = st.button("📤 Kirim")
    
    # Handle example query
    if 'example_query' in st.session_state:
        user_input = st.session_state.example_query
        del st.session_state.example_query
        submit_button = True  # Auto submit
    
    if submit_button and user_input:
        if not st.session_state.api_key:
            st.error("⚠️ Silakan masukkan API Key di sidebar terlebih dahulu!")
            return
        
        # Add user message
        st.session_state.messages.append({
            'role': 'user',
            'content': user_input
        })
        
        # Find relevant documents with semantic search
        relevant_docs = find_relevant_chunks(
            user_input,
            st.session_state.documents,
            model=embedding_model,
            top_k=5
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
        
        st.rerun()

if __name__ == "__main__":
    main()