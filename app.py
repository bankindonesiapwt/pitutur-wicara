import streamlit as st
import json
import os
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
    page_title="PITUTUR-Wicara - KPw BI Purwokerto",
    page_icon="https://www.bi.go.id/favicon.png",
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
        display: flex;
        align-items: center;
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
        display: inline-block;
    }
    .wa-header img {
        display: inline-block;
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
        
        /* Button text alignment on mobile */
        button[kind="secondary"] p {
            text-align: left !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Load Knowledge Base from JSON if available
def load_knowledge_from_json():
    """Load knowledge base from JSON file if exists"""
    kb_file = "knowledge_base/current_knowledge.json"
    if os.path.exists(kb_file):
        try:
            with open(kb_file, 'r', encoding='utf-8') as f:
                kb_data = json.load(f)
            
            # Convert JSON to text format
            text_content = "INFORMASI BANK INDONESIA KANTOR PERWAKILAN PURWOKERTO\n\n"
            for section in kb_data.get("sections", []):
                text_content += "=" * 47 + "\n"
                text_content += section.get("title", "").upper() + "\n"
                text_content += "=" * 47 + "\n\n"
                text_content += section.get("content", "") + "\n\n"
            
            return text_content
        except Exception as e:
            st.warning(f"⚠️ Error loading knowledge base from JSON: {e}")
            return None
    return None

# Built-in Knowledge Base - Bank Indonesia Perwakilan Purwokerto
# Try to load from JSON first, fallback to hardcoded
_kb_from_json = load_knowledge_from_json()
BUILTIN_KNOWLEDGE = _kb_from_json if _kb_from_json else """
INFORMASI BANK INDONESIA KANTOR PERWAKILAN PURWOKERTO

===============================================
MENU UTAMA
===============================================
1. Tentang Bank Indonesia
2. Informasi Kantor Perwakilan Bank Indonesia Purwokerto
3. Layanan yang tersedia di Bank Indonesia Purwokerto
4. Magang dan PKL
5. Survei, Pengaduan, dan Informasi Publik

===============================================
1. TENTANG BANK INDONESIA
===============================================

Bank Indonesia (BI) adalah bank sentral Republik Indonesia yang bertanggung jawab dalam mengatur dan menjaga kestabilan nilai rupiah. BI juga memiliki peran penting dalam pengaturan kebijakan moneter untuk mencapai tujuan ekonomi nasional.

Untuk Informasi lebih lanjut terkait Bank Indonesia dapat dilihat pada tautan berikut: 
https://www.bi.go.id/id/tentang-bi/profil/Default.aspx

1.1 ORGANISASI
Struktur Organisasi Bank Indonesia dapat dilihat di tautan berikut:
https://www.bi.go.id/id/tentang-bi/profil/organisasi/Default.aspx

1.2 KONTAK BANK INDONESIA PUSAT
Bank Indonesia
Jalan M.H. Thamrin No. 2, Jakarta 10350
Contact Center Bank Indonesia Bicara
Telp: 131 dan 1500131 (dari luar negeri)
E-mail: bicara@bi.go.id
Chatbot PITUTUR-Wicara: 081 131 131 131

===============================================
2. INFORMASI KANTOR PERWAKILAN BANK INDONESIA PURWOKERTO
===============================================

2.1 PROFIL PIMPINAN
CHRISTOVENY
Deputi Direktur – Kepala Perwakilan BI Purwokerto

Christoveny lahir di Payakumbuh pada tahun 1976. Menyelesaikan pendidikan sarjana di Bidang Ekonomi Universitas Andalas pada tahun 1999. Christoveny melanjutkan Pendidikan di Universitas Indonesia dan mendapatkan gelar Master di Bidang Manajemen pada tahun 2010.

Memulai kariernya di Bank Indonesia sejak tahun 2001, saat ini Christoveny menjabat sebagai Kepala Perwakilan Bank Indonesia Purwokerto sejak tahun 2024. Sebelumnya, Christoveny menjabat sebagai Deputi Kepala Perwakilan Perumusan & Implementasi KEKDA (2023-2024).

2.2 LOKASI
Alamat KPwBI Purwokerto:
Jl. Jenderal Ahmad Yani No.30 Purwokerto 53115
Telp. (0281) 631632
Google Maps: https://g.co/kgs/qe14jYA

2.3 JAM PELAYANAN
Jam Pelayanan KPwBI Purwokerto:
Senin - Jumat, 08:00 - 16:00 WIB

2.4 KONTAK
Anda bisa menghubungi KPwBI Purwokerto di kontak berikut:
- No HP: (0281) 631632
- Instagram: https://www.instagram.com/bank_indonesia_purwokerto/
- TikTok: https://www.tiktok.com/@bi.purwokerto
- Twitter: https://twitter.com/BI_Purwokerto
- Youtube: https://www.youtube.com/@bankindonesiapurwokerto702

===============================================
3. LAYANAN YANG TERSEDIA DI BANK INDONESIA PURWOKERTO
===============================================

3.1 PENUKARAN UANG DAN KAS KELILING

Penukaran Uang dapat dilakukan langsung di KPw Bank Indonesia Purwokerto serta Kas Keliling yang informasi terkait jadwal dan lainnya bisa dilihat di:
Instagram: https://www.instagram.com/bank_indonesia_purwokerto/ 
Website: https://pintar.bi.go.id/Order/KasKeliling

3.1.1 SYARAT PENUKARAN UANG RUPIAH MELALUI KAS KELILING
1. Penukar harus menunjukkan bukti pemesanan dalam bentuk digital/cetak.
2. Uang Rupiah yang akan ditukarkan harus sesuai nominal yang tertera pada bukti pemesanan.
3. Uang Rupiah yang akan ditukarkan harus dipilah, disusun menurut jenis pecahan dan tahun emisi, serta dipisahkan antara yang layak dan tidak layak edar.
4. Tidak boleh menggunakan selotip, perekat, lakban, atau steples untuk mengelompokkan uang Rupiah.
5. Bank Indonesia memberikan penggantian sesuai dengan nominal uang Rupiah yang ditukarkan, dalam pecahan dan tahun emisi yang sama atau berbeda.
6. Penggantian uang Rupiah hanya diberikan jika ciri keasliannya dapat diidentifikasi.
7. NIK-KTP tidak dapat digunakan untuk pemesanan baru setelah tanggal yang tertera pada bukti pemesanan, namun dapat digunakan kembali setelah tanggal tersebut untuk pemesanan selanjutnya.

3.1.2 UANG RUPIAH YANG DAPAT DITUKARKAN
1. Masyarakat bisa memilih jenis pecahan uang Rupiah yang tersedia di lokasi kas keliling saat melakukan pemesanan.
2. Jumlah penukaran uang Rupiah kertas dan logam mengikuti alokasi ketersediaan di lokasi kas keliling yang dipilih.
3. Penukaran uang Rupiah logam dapat dilakukan maksimal 250 keping per pecahan.
4. Penukaran uang Rupiah kertas dilakukan dalam kelipatan setiap 100 lembar per pecahan, mengikuti alokasi yang ditetapkan oleh Bank Indonesia.
5. Bank Indonesia dapat memberikan uang Rupiah dari berbagai jenis tahun emisi yang masih berlaku sebagai alat pembayaran yang sah.

3.2 EMISI UANG
Informasi terkait Emisi Uang yang masih berlaku dapat dilihat pada tautan berikut:
https://www.bi.go.id/id/rupiah/gambar-uang/default.aspx

===============================================
4. MAGANG DAN PKL (PRAKTIK KERJA LAPANGAN)
===============================================

PKL adalah kegiatan praktik kerja yang diberikan kepada mahasiswa/siswa yang difasilitasi oleh Bank Indonesia. Memberikan kesempatan bagi mahasiswa/siswa untuk belajar dan mengembangkan diri melalui keterlibatan langsung dalam pelaksanaan tugas di Bank Indonesia.

4.1 PERSYARATAN UMUM AKADEMIK

a. Jenjang pendidikan:
   - Peserta PKL: D3/D4/S1/S2
   - Peserta PKL: Sekolah Menengah Kejuruan (SMK)

b. Tingkat pendidikan:
   - Peserta PKL, minimal semester 6
   - Peserta PKL, minimal kelas XI

c. Bidang Studi:
   - Peserta PKL: Ekonomi (Manajemen, Akuntansi, Ilmu Ekonomi, Keuangan), Matematika, Statistika, Teknik Industri, Teknik Informatika, Ilmu Komputer, Sistem Informasi, Hukum, Administrasi Bisnis/Niaga, Psikologi.
   - Peserta PKL: Semua jurusan yang tersedia di SMK.

d. Keahlian khusus antara lain:
   - Peserta PKL: Menguasai Microsoft Office (Word, Excel, PowerPoint); desain grafis; programmer;
   - Peserta PKL: komputer jaringan, multimedia; administrasi arsip; menguasai Microsoft Office (Word, Excel, PowerPoint).

4.2 ALUR PENDAFTARAN

- Pengajuan Magang melalui surat pengantar dan proposal yang dikirimkan ke Kantor Perwakilan Bank Indonesia Purwokerto
- Jangka waktu proses seleksi maksimal 1 bulan

Jika Lolos: Akan dihubungi pihak KPwBI Purwokerto
Jika Tidak Lolos: Informasi melalui telepon (0281) 631631 KPwBI

CATATAN:
1. Jika mahasiswa lolos seleksi akan dihubungi oleh pihak Bank Indonesia Purwokerto
2. Pengiriman surat pengantar dan proposal paling lambat 3 bulan sebelum periode magang yang dikehendaki
3. Seluruh dokumen surat pengantar dan proposal adalah dokumen asli, dikirim ke Bank Indonesia Purwokerto (dalam bentuk hardcopy). Tidak melayani email.

4.3 PERSYARATAN ADMINISTRASI & PERMOHONAN

- Surat Pengantar dari Universitas/Sekolah. Mencakup:
  * Keterangan data mahasiswa/siswa (Nama, NIM/NIS, Fakultas/Program Studi/Jurusan, Semester/Kelas)
  * Durasi dan Periode PKL
  
- Fotokopi transkrip nilai semester terakhir

- Proposal Individu. Mencakup:
  * Data diri lengkap (CV)
  * Motivation Letter (menjelaskan maksud dan tujuan PKL, harapan atau target yang akan dicapai)
  * Bidang pekerjaan yang diminati (menceritakan passion atau minat terhadap salah satu bidang pekerjaan: moneter & makroprudensial, sistem pembayaran, pengelolaan uang rupiah, manajemen intern)
  * Fotokopi KTP
  * Fotokopi NPWP
  * Fotokopi buku rekening tabungan pribadi (khusus untuk peserta PKL)

===============================================
5. SURVEI, PENGADUAN, DAN INFORMASI PUBLIK
===============================================

5.1 PENGAJUAN INFORMASI PUBLIK

Informasi publik bisa diakses pada tautan berikut:
https://www.bi.go.id/id/informasi-publik/informasi-publik/Default.aspx

Atau jika ingin pengajuan informasi lain bisa lewat tautan berikut:
https://www.bi.go.id/id/layanan/permintaan-informasi/default.aspx

5.2 PENGADUAN

TATA CARA PENYAMPAIAN PENGADUAN, TINDAK LANJUT DAN PENYELESAIAN PERLINDUNGAN KONSUMEN

Konsumen dapat menyampaikan pengaduan ke Bank Indonesia melalui:

1. Contact Center Bank Indonesia (BI Bicara)
   Telp: 131 dan 1500131 (dari luar negeri)

2. Surat Elektronik atau E-mail
   Email: bicara@bi.go.id

3. Surat Tertulis
   Kepada Kantor Perwakilan Bank Indonesia (KPw BI) yang terdekat dengan domisili Konsumen

4. Layanan Bicara Daring
   Melalui aplikasi Webex dengan cara klik tautan berikut:
   https://bankindonesia.webex.com/join/bicara

5. Website Form Pengaduan Konsumen
   Dengan menggunakan form online Pengaduan Konsumen BI

5.3 PENGISIAN SURVEY KEPUASAN

Silakan isi survey kepuasan pengguna untuk membantu kami meningkatkan pelayanan.

===============================================
INFORMASI TAMBAHAN
===============================================

WILAYAH KERJA KPWBI PURWOKERTO:
- Kabupaten Banyumas
- Kabupaten Purbalingga
- Kabupaten Cilacap
- Kabupaten Banjarnegara
- Kabupaten Kebumen

TUGAS DAN FUNGSI:
1. Pengelolaan Uang Rupiah
2. Sistem Pembayaran
3. Stabilitas Sistem Keuangan
4. Edukasi dan Komunikasi

PROGRAM UNGGULAN:
- Gerakan Nasional Non-Tunai (GNNT)
- Sosialisasi QRIS (Quick Response Code Indonesian Standard)
- Taman Pintar Rupiah
- Tim Pengendali Inflasi Daerah (TPID)
"""

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'documents' not in st.session_state:
    st.session_state.documents = []
if 'api_key' not in st.session_state:
    # Load API key from Streamlit secrets or environment variable
    try:
        st.session_state.api_key = st.secrets.get("GEMINI_API_KEY", "")
    except:
        st.session_state.api_key = os.getenv("GEMINI_API_KEY", "")
if 'builtin_loaded' not in st.session_state:
    st.session_state.builtin_loaded = False
if 'sidebar_open' not in st.session_state:
    st.session_state.sidebar_open = False

# Functions
def load_builtin_knowledge(model=None):
    """Load built-in knowledge base about BI Purwokerto"""
    chunks = chunk_text(BUILTIN_KNOWLEDGE)
    docs = []
    for i, chunk in enumerate(chunks):
        docs.append({
            'id': f"builtin_purwokerto_{i}",
            'filename': "📘 Pengetahuan BI Purwokerto (Built-in)",
            'chunk': chunk,
            'features': create_embedding_features(chunk, model),
            'index': i,
            'total_chunks': len(chunks)
        })
    return docs

def chunk_text(text, chunk_size=2000, overlap=400):
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
            prompt = f"""Kamu adalah asisten chatbot Bank Indonesia Perwakilan Purwokerto yang membantu menjawab pertanyaan.

INFORMASI DARI DOKUMEN:
{context}

PERTANYAAN: {user_message}

INSTRUKSI PENTING:
- WAJIB gunakan HANYA informasi dari dokumen di atas untuk menjawab
- Jika informasi ada di dokumen, jawab dengan detail dan lengkap dari dokumen tersebut
- JANGAN katakan "informasi tidak tersedia" jika sudah ada di dokumen
- Jawab dengan struktur yang jelas menggunakan bullet points dan numbering
- Berikan informasi praktis yang bisa langsung digunakan
- Sertakan nomor kontak, alamat, atau link yang relevan dari dokumen
- Jawab dalam Bahasa Indonesia yang ramah dan profesional
- Jika memang benar-benar tidak ada di dokumen, baru katakan tidak tersedia dan sarankan menghubungi kantor"""
        else:
            prompt = f"""Kamu adalah asisten chatbot Bank Indonesia yang membantu menjawab pertanyaan.

Pertanyaan: {user_message}

Instruksi:
- Jawab berdasarkan pengetahuan umum tentang Bank Indonesia
- Berikan informasi yang akurat dan bermanfaat
- Sertakan link ke website resmi bi.go.id untuk informasi lebih lanjut
- Jawab dalam Bahasa Indonesia dengan ramah dan profesional"""
        
        # Call Gemini API using REST
        models_to_try = [
            "gemini-2.5-flash",
            "gemini-2.0-flash",
            "gemini-2.5-flash-lite",
            "gemini-2.0-flash-lite",
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
                    continue
            except Exception as e:
                last_error = str(e)
                continue
        
        return f"❌ Tidak ada model yang berhasil. Last error: {last_error}", None
    
    except Exception as e:
        return f"❌ Error: {str(e)}", None

# Main App
def main():
    # Load embedding model
    try:
        embedding_model = load_embedding_model()
        model_loaded = True
    except Exception as e:
        st.warning(f"⚠️ Semantic search tidak tersedia: {str(e)}")
        embedding_model = None
        model_loaded = False
    
    # Auto-load built-in knowledge base (only once)
    if not st.session_state.builtin_loaded:
        builtin_docs = load_builtin_knowledge(embedding_model)
        st.session_state.documents.extend(builtin_docs)
        st.session_state.builtin_loaded = True
    
    # WhatsApp-style Sticky Header
    st.markdown("""
    <div class="wa-header">
        <svg width="32" height="32" viewBox="0 0 68 68" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; margin-right: 10px;">
            <path fill-rule="evenodd" clip-rule="evenodd" d="M67.5 33.748C67.5 15.1087 52.3873 0 33.752 0C15.1103 0 0 15.1087 0 33.748C0 52.3849 15.1103 67.4984 33.752 67.4984C52.3873 67.4984 67.5 52.3849 67.5 33.748ZM25.3344 61.3255C28.0118 61.3255 30.0094 61.0632 30.1534 57.4222H36.7429C36.8868 61.0632 38.91 61.1816 41.5203 61.1816V63.0281H25.3344V61.3255ZM42.4303 30.8059C45.9586 31.9231 54.2394 35.6993 54.2394 43.5115C54.2394 51.2166 46.9766 55.806 38.3559 55.806H13.2606L13.2862 53.8068C17.8388 53.8068 19.1871 53.207 19.1871 48.5584V19.1551C19.1871 13.9803 17.1447 13.6564 13.2774 13.6564V11.7963C14.0019 11.7795 23.1184 11.7915 30.1534 11.7963C30.0094 8.1513 28.0118 7.8866 25.3344 7.8866V6.18724H41.5203V8.03294C38.91 8.03294 36.8868 8.1513 36.7429 11.7963H38.3559C41.9961 11.7963 50.9351 13.0494 50.9519 20.409C50.9647 25.5735 47.4764 28.8586 42.4303 30.8059ZM47.298 44.7478C47.298 38.6357 43.1012 34.5669 37.996 32.1014C34.666 32.8251 30.7571 33.249 27.1009 33.2802L28.0198 31.0002C28.8498 30.9731 29.4784 30.9219 30.1534 30.8819V15.5933H36.7429V29.8935C42.2648 28.2637 44.5767 24.9865 44.5767 21.1816C44.5767 16.305 40.8789 13.9763 36.7261 13.9763L25.7894 13.9803V48.6935C25.7894 52.3681 27.999 53.1382 30.1534 53.1766V35.1211C32.6236 35.0347 35.2778 34.6836 36.7429 34.343V53.1766C42.0089 53.1718 47.298 49.9634 47.298 44.7478Z" fill="white"/>
        </svg>
        <div>
            <h3>PITUTUR-Wicara</h3>
            <h4 style="font-size:0.9rem; color:white; margin-top:-24px; font-style: italic; font-weight: normal;">KPw BI Purwokerto</h4>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Set API key
    api_key = st.session_state.api_key
    
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
    
    # Chat input
    st.markdown("---")
    
    # Check if API key is configured
    if not st.session_state.api_key:
        st.error("⚠️ API key tidak dikonfigurasi. Silakan hubungi administrator.")
        st.info("Administrator: Tambahkan GEMINI_API_KEY di Streamlit Secrets atau environment variable.")
        return
    
    # Example questions
    st.subheader("💡 Contoh Pertanyaan:")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🏛️ Tentang Bank Indonesia"):
            st.session_state.example_query = "Apa itu Bank Indonesia?"
        if st.button("📍 Informasi Kantor Perwakilan Bank Indonesia Purwokerto"):
            st.session_state.example_query = "Informasi Kantor Perwakilan Bank Indonesia Purwokerto"
        if st.button("💼 Layanan yang tersedia di Bank Indonesia Purwokerto"):
            st.session_state.example_query = "Layanan apa saja yang tersedia di Bank Indonesia Purwokerto?"
    with col2:
        if st.button("🎓 Magang dan PKL"):
            st.session_state.example_query = "Bagaimana cara mendaftar magang atau PKL di Bank Indonesia Purwokerto?"
        if st.button("📢 Survei, Pengaduan, dan Informasi Publik"):
            st.session_state.example_query = "Bagaimana cara menyampaikan pengaduan atau mengakses informasi publik?"
    
    # User input
    user_input = st.text_input("Ketik pertanyaan Anda tentang Bank Indonesia...", key="user_input_field", value="")
    
    # Submit button
    submit_button = st.button("📤 Kirim")
    
    # Handle example query
    if 'example_query' in st.session_state:
        user_input = st.session_state.example_query
        del st.session_state.example_query
        submit_button = True
    
    if submit_button and user_input:
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
            top_k=8
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
