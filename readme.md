# 🧠 Slang-Aware Sentiment Analysis with Shadow Deployment
> Sistem ML untuk mendeteksi data drift pada bahasa slang media sosial Indonesia

---

## 📌 Problem Statement

Bahasa di media sosial Indonesia berubah dengan sangat cepat, terutama didorong oleh:
- Konten viral yang menyebarkan slang baru secara masif
- Komunitas spesifik seperti gaming, podcast, dan hiburan

**Akibatnya:**
- Model sentiment lama cepat usang karena *data drift*
- Model gagal memahami makna slang baru (contoh: *gacor*, *sabi*, *no cap*)

---

## 🎯 Objectives

Membangun sistem ML end-to-end yang mampu:
1. Mendeteksi perubahan bahasa (*slang drift*) secara otomatis
2. Membandingkan performa model lama vs model baru secara paralel
3. Menerapkan **shadow deployment** tanpa mengganggu pengalaman pengguna

---

## 📊 Data Strategy

### Sumber Data — YouTube Comments

| Kategori | Deskripsi | Keunggulan |
|---|---|---|
| 🔥 Viral Content | Video trending nasional | Slang paling baru muncul pertama di sini |
| 🎮 Gaming Community | Konten gaming populer | Slang teknis & komunitas spesifik |
| 🎙️ Podcast | Obrolan natural & santai | Bahasa sehari-hari yang autentik |
| 💬 High-Engagement Videos | Video dengan komentar masif | Variasi bahasa yang tinggi |

### Struktur Dataset

```
    data/
    ├── old_data/       # Komentar dari video lama (simulasi model lama)
    │   ├── viral/
    │   ├── gaming/
    │   └── podcast/
    └── new_data/       # Komentar terbaru (slang-aware)
        ├── viral/
        ├── gaming/
        └── podcast/
```
> **Tujuan:** Mensimulasikan *real-world data drift* antara data lama dan baru.

---

## 🏗️ System Architecture
    User Input
        │
        ▼
    ┌─────────┐
    │ FastAPI │
    └────┬────┘
         │
         ├──────────────────────┐
         ▼                      ▼
    ┌──────────┐         ┌──────────┐
    │ Model v1 │         │ Model v2 │
    │  (old)   │         │  (new)   │
    │→ response│         │→ background
    └──────────┘         └────┬─────┘
                              │
                         ┌────▼─────┐
                         │ Logging  │
                         │    DB    │
                         └────┬─────┘
                               │
                      ┌────────▼───────┐
                      │  Eval Script   │
                      └────────┬───────┘
                               │
                      ┌────────▼───────┐
                      │   Dashboard    │
                      └────────────────┘

---

## ⚙️ ML Pipeline

### 1. 🔄 Data Ingestion
- YouTube comment crawling via YouTube Data API v3
- Pengambilan data multi-kategori: gaming, podcast

### 2. 🧹 Preprocessing
- Text cleaning (hapus emoji, URL, mention)
- Stopword removal (Bahasa Indonesia)
- Slang normalization *(opsional — untuk analisis komparatif)*

### 3. 🔧 Feature Engineering
- TF-IDF Vectorizer
- N-gram (unigram + bigram)

### 4. 🤖 Modeling

| Model | Training Data | Karakteristik |
|---|---|---|
| **Model v1** | `old_data/` | Baseline, tidak mengenal slang baru |
| **Model v2** | `new_data/` | Slang-aware, dilatih data terkini |

### 5. 🚀 Shadow Deployment
- API melayani prediksi menggunakan **Model v1**
- **Model v2** berjalan di background secara paralel
- Hasil kedua model disimpan ke database untuk perbandingan

### 6. 📈 Monitoring & Evaluation
- Agreement rate antara v1 dan v2
- Disagreement case analysis
- Slang failure detection

---

## 🔥 Key Insights & Output

### 1. Agreement Analysis
Seberapa sering kedua model berbeda pendapat?

### 2. Slang Failure Case
Input : "produk ini gacor banget"
Model v1 → ❌ Negatif
Model v2 → ✅ Positif

### 3. Community Bias Analysis
Gaming comments  → Model v1 sering salah
Podcast comments → Model v1 relatif akurat

---

## 🐳 Infrastructure

### Docker
```bash
# Build & run
docker-compose up --build
```

---

## 📁 Project Structure

    ├── data/
    │   ├── old_data/
    │   └── new_data/
    ├── src/
    │   ├── crawling/           # YouTube comment scraper
    │   ├── preprocessing/      # Text cleaning & normalization
    │   ├── modeling/           # Train & evaluate models
    │   ├── api/                # FastAPI shadow deployment
    │   └── monitoring/         # Logging & evaluation scripts
    ├── dashboard/              # Monitoring dashboard
    ├── tests/                  # Unit tests
    ├── docker-compose.yml
    ├── Dockerfile
    ├── .github/
    │   └── workflows/
    │       └── ci.yml
    └── README.md

---

## 🚀 Quick Start

```bash
# Clone repo
git clone https://github.com/username/slang-sentiment-shadow.git
cd slang-sentiment-shadow

# Install dependencies
pip install -r requirements.txt

# Run API
uvicorn src.api.main:app --reload

# Or with Docker
docker-compose up --build
```

---

## 💼 Skills Demonstrated

| Domain | Detail |
|---|---|
| 🧠 ML / NLP | Sentiment analysis, TF-IDF, n-gram, slang handling |
| ⚙️ Engineering | FastAPI, REST API design, logging system |
| 🐳 DevOps | Docker, Docker Compose |
| 🔥 MLOps | Shadow deployment, model monitoring, data drift detection |

---

## 👤 Author

**Naufal F.N**
- GitHub: [@nopal-fz](https://github.com/nopal-fz)
