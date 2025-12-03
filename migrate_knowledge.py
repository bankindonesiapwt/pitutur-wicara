"""
Migration Script: Convert existing hardcoded knowledge base to JSON format
Run this once to migrate from BUILTIN_KNOWLEDGE text to JSON structure
"""

import json
import os
from datetime import datetime
import re

KNOWLEDGE_BASE_DIR = "knowledge_base"
CURRENT_KB_FILE = os.path.join(KNOWLEDGE_BASE_DIR, "current_knowledge.json")

# Your existing knowledge base text
EXISTING_KB = """
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

def parse_knowledge_base(text):
    """Parse text knowledge base into structured JSON"""
    sections = []
    
    # Split by section headers (lines with ===)
    parts = re.split(r'={40,}', text)
    
    current_title = ""
    current_content = ""
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
        
        lines = part.split('\n')
        
        # First line is usually the title
        if len(lines) > 0:
            potential_title = lines[0].strip()
            
            # Check if it looks like a section header
            if potential_title and len(potential_title) < 100:
                # Save previous section if exists
                if current_title and current_content:
                    sections.append({
                        "title": current_title,
                        "content": current_content.strip(),
                        "created_at": datetime.now().isoformat()
                    })
                
                # Start new section
                current_title = potential_title
                current_content = '\n'.join(lines[1:]).strip()
            else:
                # Continue current section
                current_content += '\n' + part
    
    # Add last section
    if current_title and current_content:
        sections.append({
            "title": current_title,
            "content": current_content.strip(),
            "created_at": datetime.now().isoformat()
        })
    
    return sections

def migrate():
    """Migrate existing knowledge base to JSON"""
    print("Starting migration...")
    
    # Create directory
    os.makedirs(KNOWLEDGE_BASE_DIR, exist_ok=True)
    
    # Parse knowledge base
    sections = parse_knowledge_base(EXISTING_KB)
    
    print(f"Parsed {len(sections)} sections")
    
    # Create JSON structure
    kb_data = {
        "sections": sections,
        "version": "1.0.0",
        "last_updated": datetime.now().isoformat(),
        "migrated_from": "hardcoded_text",
        "migration_date": datetime.now().isoformat()
    }
    
    # Save to JSON
    with open(CURRENT_KB_FILE, 'w', encoding='utf-8') as f:
        json.dump(kb_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Migration complete!")
    print(f"✅ Knowledge base saved to: {CURRENT_KB_FILE}")
    print(f"✅ Total sections: {len(sections)}")
    
    # Print section titles
    print("\nMigrated sections:")
    for idx, section in enumerate(sections, 1):
        print(f"  {idx}. {section['title']}")

if __name__ == "__main__":
    migrate()
