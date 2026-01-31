# 🚀 PosFlow AI: Automated POS Indonesia Billing Extractor

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Gemini AI](https://img.shields.io/badge/AI-Gemini%202.5%20Flash-orange?style=for-the-badge&logo=google-gemini)

**PosFlow AI** adalah solusi otomasi cerdas yang menggabungkan kekuatan **Artificial Intelligence (Gemini 2.5 Flash)** untuk menyederhanakan proses administrasi struk POS Indonesia. Alat ini mampu mengekstrak nomor billing secara otomatis dari foto nota, scan gambar, atau file PDF, kemudian mengunduh struk aslinya secara massal.

---

## ✨ Fitur Unggulan

-   **🧠 Intelligent OCR**: Menggunakan Gemini 2.5 Flash untuk membaca kode billing dari foto yang miring, buram, atau dokumen hasil scan yang kompleks.
-   **⚡ Batch Processing**: Memproses ratusan file dalam satu folder sekaligus tanpa intervensi manual.
-   **🔗 Auto-Generator URL**: Mengonversi kode billing dan tanggal menjadi token Base64 yang valid untuk akses langsung ke server POS Indonesia.
-   **📂 Auto-Organization**: Hasil unduhan PDF disimpan secara rapi di folder output yang ditentukan.
-   **🎨 Terminal UI**: Antarmuka CLI yang informatif dengan progress tracker dan desain ASCII art yang estetik.

---

## 📋 Alur Kerja Sistem



1.  **Scanning**: Skrip memindai folder input untuk mencari file gambar atau PDF.
2.  **AI Inference**: File dikirim ke model Gemini untuk diekstraksi nomor billing-nya saja.
3.  **Encoding**: Kode yang ditemukan digabungkan dengan parameter tanggal dan dienkripsi ke format Base64.
4.  **Download**: Skrip melakukan request ke server POS Indonesia dan mengunduh file PDF resmi.

---

## 🛠️ Instalasi

1.  **Clone Repositori**
    ```bash
    git clone [https://github.com/FebraS/PosFlowAI.git](https://github.com/FebraS/PosFlowAI.git)
    cd PosFlowAI
    ```

2.  **Instal Dependensi**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Konfigurasi API Key**
    Buka file `posflow.py` dan masukkan API Key Gemini Anda pada variabel berikut:
    ```python
    GENAI_API_KEY = "AIzaSy..." # Dapatkan di [https://aistudio.google.com/](https://aistudio.google.com/)
    ```

---

## 🚀 Panduan Penggunaan

Jalankan skrip melalui terminal atau command prompt dengan instruksi berikut:

### Mode A: Ekstraksi AI (Dari Folder Gambar/PDF)
Gunakan mode ini jika Anda memiliki banyak foto nota fisik.
```bash
python posflow.py -r ./folder_nota -d 2026-05-20 -o hasil_unduh --ai
