# Sistem RAG Buku Peraturan Silat

Projek ini adalah sistem Retrieval-Augmented Generation (RAG) yang lengkap untuk menjawab soalan berkaitan buku peraturan rasmi Pencak Silat. Ia menggunakan teknologi sumber terbuka tempatan untuk memproses PDF setebal 700+ muka surat, menyimpan kandungannya ke dalam pangkalan data vektor, dan menyediakan antara muka web yang mesra pengguna untuk membuat pertanyaan.

Projek ini dibangunkan sebagai projek pembelajaran untuk meneroka aliran kerja pembangunan aplikasi RAG moden dari hujung ke hujung, daripada pemprosesan dokumen yang canggih hingga penggunaan antara muka interaktif.

## Ciri-ciri Utama

- **Pemprosesan PDF Canggih**: Memproses PDF yang kompleks dengan bijak, membezakan antara halaman berisi teks dan halaman yang mengandungi kandungan visual seperti jadual dan rajah.
- **Pengendalian Kandungan Visual**: Daripada menggunakan OCR yang tidak boleh dipercayai, ia menghasilkan "pemegang tempat" deskriptif untuk halaman yang kaya dengan visual, membimbing pengguna ke halaman yang betul dalam PDF.
- **Strategi Embedding Moden**: Menggunakan model embedding Qwen yang canggih (`Qwen/Qwen3-Embedding-0.6B`) dengan tetingkap konteks yang besar.
- **Chunking Berasaskan Token**: Memanfaatkan tetingkap konteks besar model dengan membahagi teks kepada bahagian besar yang kaya secara semantik (4096 token).
- **Tempatan & Peribadi**: Keseluruhan pipeline, daripada embedding hingga penjanaan, berjalan secara tempatan menggunakan Ollama, memastikan privasi data.
- **Antara Muka Interaktif**: Antara muka web yang mudah dan intuitif dibina dengan Streamlit untuk bertanya soalan dan menerima jawapan.

## Teknologi yang Digunakan

- **Pemprosesan PDF**: `PyMuPDF`
- **Pangkalan Data Vektor**: `ChromaDB`
- **Framework Orkestrasi**: `LangChain`
- **Model Embedding**: `Qwen/Qwen3-Embedding-0.6B` (melalui `sentence-transformers`)
- **LLM Generatif**: `Ollama` (dengan `llama3`)
- **Frontend**: `Streamlit`

## Struktur Projek

```
.
├── app.py                  # Aplikasi frontend Streamlit
├── data/
│   ├── chroma_db/          # Pangkalan data vektor kekal
│   └── silat_rules_...pdf  # Dokumen PDF sumber
├── docs/
│   ├── ...                 # Fail perancangan dan log projek
├── main.py                 # Skrip ingesi utama (jalankan sekali sahaja)
├── rag_chain.py            # Logik pertanyaan RAG teras
├── README.md               # Fail README utama
├── requirements.txt        # Kebergantungan Python
└── src/
    ├── config.py           # Konfigurasi pusat untuk projek
    ├── content_analyzer.py # Logik untuk mengklasifikasikan kandungan halaman
    ├── data_processor.py   # Mengendalikan chunking teks, embedding, dan penyimpanan
    ├── pdf_parser.py       # Mengekstrak dan membersihkan teks dari PDF
    ├── pipeline_utils.py   # Fungsi pembantu untuk analisis dan paparan
    └── text_processor.py   # Utiliti pembersihan dan penapisan teks
```

## Cara Menggunakan

Projek ini dibahagikan kepada dua peringkat utama: ingesi data sekali sahaja dan aplikasi pertanyaan.

### 1. Pipeline Ingesi (Jalankan sekali sahaja)

Mula-mula, anda perlu memproses PDF dan mengisi pangkalan data vektor.

```bash
python main.py
```

Skrip ini akan:
- Membaca dan memproses PDF
- Membersihkan dan mengklasifikasikan kandungan setiap halaman
- Membahagi kandungan kepada bahagian besar berasaskan token
- Menghasilkan embedding menggunakan model Qwen
- Menyimpan embedding dalam direktori `data/chroma_db`

### 2. Menjalankan Aplikasi Streamlit

Setelah ingesi selesai, anda boleh memulakan antara muka pengguna.

```bash
streamlit run app.py
```

Ini akan membuka tab baru dalam pelayar anda dengan aplikasi yang berjalan.

## Tujuan Projek

Projek ini berfungsi sebagai contoh praktikal bagi:
- Pembangunan sistem RAG end-to-end
- Pemprosesan dokumen kompleks dengan AI
- Penggunaan model tempatan untuk privasi data
- Integrasi pelbagai teknologi AI dan machine learning

Sistem ini memberikan asas yang kukuh untuk membangunkan aplikasi RAG yang lebih canggih pada masa akan datang.