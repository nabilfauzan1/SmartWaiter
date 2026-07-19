<div align="center">

# SmartWaiter

### AI Digital Waiter for Sorain Kitchen

SmartWaiter adalah aplikasi chatbot berbasis LLM yang berperan sebagai pelayan digital bernama **Sora** untuk restoran Jepang fiktif **Sorain Kitchen**.

Sora membantu pelanggan memahami menu dan menemukan hidangan berdasarkan selera, anggaran, tingkat kepedasan, kebutuhan diet, serta alergi makanan.

</div>

---

## Ringkasan Proyek

Pelanggan restoran sering membutuhkan bantuan untuk memilih menu, terutama ketika:

- belum mengenal hidangan Jepang;
- mempunyai batas anggaran;
- memiliki alergi atau pantangan makanan;
- mencari pilihan vegetarian atau rendah kalori;
- ingin mengetahui menu unggulan restoran;
- membutuhkan rekomendasi makanan, minuman, dan dessert yang sesuai.

SmartWaiter menyediakan percakapan interaktif melalui Streamlit. Data menu Sorain Kitchen disimpan dalam file CSV, sedangkan Google Gemini digunakan untuk memahami pertanyaan pelanggan dan menghasilkan jawaban yang natural.

> **Catatan:** Sorain Kitchen adalah restoran fiktif. Seluruh data menu, harga, informasi nutrisi, alamat, dan kontak digunakan untuk kebutuhan pembelajaran dan demonstrasi.

---

## Identitas Produk

| Elemen | Nilai |
|---|---|
| Nama proyek | SmartWaiter |
| Nama restoran | Sorain Kitchen |
| Nama AI waiter | Sora |
| Jenis restoran | Modern Japanese Dining |
| Platform | Streamlit |
| Bahasa pemrograman | Python |
| LLM | Google Gemini |
| Environment | Miniconda |
| Sumber data utama | CSV dan JSON |

---

## Fitur Utama

### 1. Percakapan dengan Sora

Pengguna dapat bertanya secara natural, misalnya:

- “Saya ingin ramen pedas.”
- “Budget saya maksimal Rp60.000.”
- “Saya vegetarian.”
- “Saya alergi udang dan telur.”
- “Menu apa yang tinggi protein?”
- “Apa rekomendasi chef?”
- “Saya ingin paket lengkap untuk dua orang.”

Sora akan menjawab sebagai pelayan Sorain Kitchen, bukan sebagai chatbot umum.

### 2. Rekomendasi menu personal

Rekomendasi dapat mempertimbangkan:

- budget;
- kategori makanan;
- tingkat kepedasan;
- jumlah kalori;
- protein, karbohidrat, dan lemak;
- status halal;
- status vegetarian;
- kandungan alergen;
- menu rekomendasi chef;
- ketersediaan menu.

### 3. Knowledge base restoran

Sora hanya boleh menggunakan data resmi dari:

- `data/menu.csv`;
- `data/restaurant_info.json`;
- `prompts/system_prompt.txt`.

Sora tidak boleh mengarang nama menu, harga, bahan, atau informasi restoran.

### 4. Session memory

Riwayat percakapan disimpan selama sesi Streamlit menggunakan `st.session_state`. Dengan demikian, Sora dapat mengingat preferensi yang sebelumnya disebutkan oleh pelanggan.

Contoh:

1. Pelanggan: “Saya vegetarian.”
2. Pelanggan: “Sekarang rekomendasikan menu pedas.”
3. Sora tetap hanya menawarkan menu vegetarian.

### 5. Halaman daftar menu

Pengguna dapat melihat seluruh menu Sorain Kitchen dan memfilter berdasarkan:

- kategori;
- rentang harga;
- vegetarian;
- halal;
- level pedas;
- rekomendasi chef;
- status ketersediaan.

### 6. Quick prompts

Antarmuka dapat menyediakan tombol cepat seperti:

- Recommend a Menu
- Spicy Food
- Healthy Meal
- Chef’s Recommendation
- Dessert
- Drinks
- Budget Meal

---

## Arsitektur Aplikasi

```text
Customer
   |
   v
Streamlit Interface
   |
   +--> Session State / Chat History
   |
   +--> Menu Loader --------> data/menu.csv
   |
   +--> Restaurant Loader --> data/restaurant_info.json
   |
   +--> Prompt Loader -------> prompts/system_prompt.txt
   |
   v
Prompt Builder
   |
   v
Google Gemini API
   |
   v
Sora Response
   |
   v
Streamlit Chat Interface
```

---

## Struktur Folder yang Direkomendasikan

```text
smartwaiter/
|
|-- app.py
|-- config.py
|-- requirements.txt
|-- README.md
|-- .env
|-- .env.example
|-- .gitignore
|
|-- assets/
|   |-- logo.png
|   |-- favicon.png
|
|-- data/
|   |-- menu.csv
|   |-- restaurant_info.json
|
|-- prompts/
|   |-- system_prompt.txt
|   |-- greeting.txt
|
|-- services/
|   |-- __init__.py
|   |-- gemini_service.py
|   |-- menu_service.py
|   |-- prompt_builder.py
|
|-- utils/
|   |-- __init__.py
|   |-- formatter.py
|
|-- pages/
    |-- 1_Menu.py
    |-- 2_Restaurant_Info.py
    |-- 3_About.py
```

---

## Persyaratan Sistem

- Miniconda atau Anaconda
- Python 3.11 atau 3.12
- Koneksi internet
- Google AI Studio API key
- Git, jika proyek akan disimpan di GitHub

---

## Menyiapkan Environment dengan Miniconda

Buka **Anaconda Prompt** atau terminal yang sudah mengenali perintah `conda`.

```bash
conda create -n smartwaiter python=3.12 -y
conda activate smartwaiter
```

Instal dependensi:

```bash
pip install streamlit google-genai pandas python-dotenv
```

Atau gunakan file `requirements.txt`:

```bash
pip install -r requirements.txt
```

Contoh isi `requirements.txt`:

```text
streamlit
google-genai
pandas
python-dotenv
```

Untuk melihat environment yang tersedia:

```bash
conda env list
```

Untuk keluar dari environment:

```bash
conda deactivate
```

---

## Konfigurasi Google AI Studio API Key

### 1. Buat file `.env`

Di root project, buat file bernama:

```text
.env
```

Isi file:

```env
GOOGLE_API_KEY=PASTE_API_KEY_ANDA_DI_SINI
```

### 2. Jangan masukkan `.env` ke GitHub

Tambahkan baris berikut ke `.gitignore`:

```text
.env
__pycache__/
*.pyc
.venv/
.streamlit/secrets.toml
```

### 3. Sediakan `.env.example`

File ini aman diunggah karena tidak berisi key asli:

```env
GOOGLE_API_KEY=YOUR_GOOGLE_AI_STUDIO_API_KEY
```

> Jangan pernah menuliskan API key asli dalam source code, README, screenshot, PDF, commit Git, atau pesan publik.

---

## Data Menu

File `data/menu.csv` berfungsi sebagai knowledge base utama.

Kolom yang digunakan:

| Kolom | Fungsi |
|---|---|
| `menu_id` | ID unik menu |
| `menu_name` | Nama menu |
| `category` | Kategori menu |
| `description` | Deskripsi singkat |
| `price` | Harga dalam rupiah |
| `calories` | Estimasi kalori |
| `protein` | Protein dalam gram |
| `carbs` | Karbohidrat dalam gram |
| `fat` | Lemak dalam gram |
| `spicy_level` | Level pedas 0–5 |
| `halal` | Status halal |
| `vegetarian` | Status vegetarian |
| `contains` | Kandungan atau alergen |
| `recommended_for` | Segmentasi rekomendasi |
| `chef_recommendation` | Penanda menu rekomendasi chef |
| `availability` | Ketersediaan menu |

Contoh pemuatan data:

```python
from pathlib import Path
import pandas as pd

MENU_PATH = Path("data/menu.csv")

def load_menu() -> pd.DataFrame:
    if not MENU_PATH.exists():
        raise FileNotFoundError(f"Menu file tidak ditemukan: {MENU_PATH}")

    return pd.read_csv(MENU_PATH)
```

---

## Restaurant Information

File `data/restaurant_info.json` menyimpan:

- profil restoran;
- alamat dan kontak;
- jam operasional;
- fasilitas;
- informasi diet dan alergen;
- branding;
- profil Sora;
- keterbatasan fitur.

Contoh pemuatan:

```python
from pathlib import Path
import json

INFO_PATH = Path("data/restaurant_info.json")

def load_restaurant_info() -> dict:
    if not INFO_PATH.exists():
        raise FileNotFoundError(
            f"Restaurant info tidak ditemukan: {INFO_PATH}"
        )

    with INFO_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)
```

---

## Cara Kerja Prompt

Prompt yang dikirim ke Gemini sebaiknya terdiri dari empat bagian:

```text
1. System prompt
2. Informasi restoran
3. Data menu yang relevan
4. Riwayat chat dan pesan terbaru pelanggan
```

Contoh struktur:

```text
[SYSTEM INSTRUCTION]

You are Sora, the official AI Waiter of Sorain Kitchen.
Only use the restaurant data supplied by the application.

[RESTAURANT INFORMATION]

...

[AVAILABLE MENU]

...

[CONVERSATION]

Customer: Saya ingin makanan pedas.
```

Untuk MVP, seluruh menu dapat dikirim sebagai konteks. Jika data semakin besar, menu sebaiknya difilter terlebih dahulu berdasarkan kategori, budget, diet, dan alergi sebelum dikirim ke model.

---

## Aturan Utama Sora

Sora harus:

- menjawab menggunakan bahasa pelanggan;
- bersikap hangat, ramah, dan profesional;
- hanya merekomendasikan menu yang tersedia;
- mempertimbangkan budget dan preferensi;
- menjelaskan alasan rekomendasi;
- tidak mengarang menu atau harga;
- tidak mengklaim dapat memesan atau memproses pembayaran;
- menyarankan konfirmasi kepada staf manusia untuk kasus alergi serius.

Sora tidak boleh:

- memperkenalkan diri sebagai ChatGPT atau Gemini;
- memberikan informasi restoran yang tidak tersedia;
- mengabaikan alergi pelanggan;
- merekomendasikan menu di atas budget tanpa menjelaskannya;
- menjawab pertanyaan yang sama sekali tidak berhubungan dengan restoran secara panjang lebar.

---

## Menjalankan Aplikasi

Pastikan environment aktif:

```bash
conda activate smartwaiter
```

Jalankan Streamlit:

```bash
streamlit run app.py
```

Aplikasi biasanya dapat diakses melalui:

```text
http://localhost:8501
```

---

## Konsep Antarmuka

### Sidebar

Sidebar dapat menampilkan:

- logo Sorain Kitchen;
- tombol New Chat;
- navigasi ke Menu;
- informasi restoran;
- About SmartWaiter;
- status koneksi API.

API key dan parameter teknis tidak perlu diperlihatkan kepada pelanggan.

### Main area

Bagian utama dapat berisi:

1. header Sorain Kitchen;
2. pengenalan singkat Sora;
3. quick prompt buttons;
4. riwayat percakapan;
5. input chat;
6. disclaimer alergi.

### Greeting awal

```text
🍵 Irasshaimase!

Selamat datang di Sorain Kitchen.

Saya Sora, AI Waiter yang siap membantu Anda menemukan hidangan
Jepang berdasarkan selera, kebutuhan diet, alergi, dan budget.

Apa yang ingin Anda nikmati hari ini?
```

---

## Error Handling

Aplikasi harus menangani kondisi berikut:

### API key tidak ditemukan

Tampilkan pesan:

```text
Google API key belum dikonfigurasi.
Silakan tambahkan GOOGLE_API_KEY ke file .env.
```

### Data menu tidak ditemukan

Tampilkan pesan:

```text
Data menu Sorain Kitchen tidak dapat dimuat.
Pastikan file data/menu.csv tersedia.
```

### Google Gemini gagal merespons

Tampilkan pesan ramah dan jangan menghentikan aplikasi:

```text
Maaf, Sora sedang mengalami gangguan koneksi.
Silakan coba kembali beberapa saat lagi.
```

### Respons kosong

Jangan menampilkan `None`. Gunakan fallback response yang jelas.

---

## Keamanan dan Privasi

- Jangan memasukkan API key ke source code.
- Jangan mengunggah file `.env`.
- Jangan menampilkan API key di UI.
- Jangan menyimpan informasi sensitif pelanggan.
- Batasi riwayat percakapan hanya pada sesi aktif.
- Jangan menganggap informasi nutrisi dummy sebagai nasihat medis.
- Untuk alergi berat, arahkan pelanggan kepada staf restoran.

---

## Acceptance Criteria MVP

Project dianggap memenuhi MVP jika:

- [ ] Aplikasi dapat dijalankan melalui `streamlit run app.py`.
- [ ] Logo Sorain Kitchen tampil dengan benar.
- [ ] Data `menu.csv` berhasil dimuat.
- [ ] Data `restaurant_info.json` berhasil dimuat.
- [ ] System prompt berhasil digunakan.
- [ ] Pesan pengguna dapat dikirim ke Gemini.
- [ ] Respons Sora muncul di chat.
- [ ] Riwayat chat bertahan selama sesi aktif.
- [ ] Tombol New Chat menghapus percakapan.
- [ ] Sora tidak merekomendasikan menu yang unavailable.
- [ ] Sora mematuhi budget yang jelas.
- [ ] Sora mematuhi status vegetarian.
- [ ] Sora menghindari alergen yang disebutkan pengguna.
- [ ] Sora tidak mengarang menu.
- [ ] Kesalahan API ditampilkan secara ramah.

---

## Contoh Skenario Pengujian

### Budget

**Input:**

```text
Saya punya budget Rp50.000. Rekomendasikan makanan dan minuman.
```

**Ekspektasi:**

Total rekomendasi tidak melebihi Rp50.000, atau Sora menjelaskan jika kombinasi tidak memungkinkan.

### Vegetarian

**Input:**

```text
Saya vegetarian dan ingin makanan utama.
```

**Ekspektasi:**

Sora hanya memilih menu dengan `vegetarian = Yes`.

### Alergi shellfish

**Input:**

```text
Saya alergi udang dan kerang.
```

**Ekspektasi:**

Sora tidak merekomendasikan menu dengan `Shellfish` pada kolom `contains`.

### Menu tidak tersedia

**Input:**

```text
Saya ingin menu yang statusnya sedang unavailable.
```

**Ekspektasi:**

Sora tidak merekomendasikannya dan menawarkan alternatif.

### Pertanyaan di luar konteks

**Input:**

```text
Buatkan program sorting Python.
```

**Ekspektasi:**

Sora mengarahkan percakapan kembali ke layanan Sorain Kitchen.

---

## Pengembangan Lanjutan

Fitur berikut berada di luar MVP:

- pemesanan langsung dari chatbot;
- integrasi POS;
- pembayaran digital;
- reservasi meja;
- QR code per meja;
- dashboard admin restoran;
- database produksi;
- user authentication;
- voice assistant;
- gambar makanan;
- OCR menu;
- rekomendasi berbasis histori pelanggan;
- integrasi stok real-time;
- multilingual support yang lebih luas;
- RAG atau vector database untuk data berskala besar.

---

## Batasan Proyek

SmartWaiter versi awal:

- hanya digunakan untuk satu restoran contoh;
- menggunakan data menu dummy;
- belum memproses order;
- belum melakukan pembayaran;
- belum terhubung dengan stok restoran;
- tidak menggantikan staf restoran untuk penanganan alergi;
- bergantung pada koneksi internet dan ketersediaan Gemini API.

---

## Tujuan Pembelajaran

Project ini menunjukkan pemahaman mengenai:

- integrasi LLM melalui API;
- system prompt dan prompt engineering;
- context engineering;
- pengolahan data CSV dan JSON;
- pengelolaan environment dengan Miniconda;
- Streamlit session state;
- modularisasi aplikasi Python;
- keamanan API key;
- desain chatbot yang memiliki domain khusus;
- error handling dan acceptance testing.

---

## Lisensi

Project ini dibuat untuk kebutuhan pembelajaran dan portofolio.

Data Sorain Kitchen bersifat fiktif. Penggunaan nama, alamat, menu, dan informasi lainnya tidak mewakili restoran nyata.

---

## Author

**Nabil Fauzan**

SmartWaiter — AI Digital Waiter for Sorain Kitchen.
