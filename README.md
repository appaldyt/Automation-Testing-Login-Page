# 🎭 Automation Testing — Login Page
### Kelas Otomesyen | Playwright Python

Project ini berisi automation test untuk halaman login pada website [Test App Kelas Otomesyen](https://test.kelasotomesyen.com), dibuat menggunakan **Playwright Python** dan **pytest**.

---

## 🛠️ Tech Stack

| Tool | Kegunaan |
|---|---|
| [Python](https://www.python.org/) | Bahasa pemrograman |
| [Playwright](https://playwright.dev/python/) | Browser automation |
| [pytest](https://docs.pytest.org/) | Test framework |
| [Allure](https://allurereport.org/) | Test report |

---

## 📁 Struktur Project

```
📦 project
 ┗ 📜 test_login.py     # Semua test case untuk fitur login
 ┗ 📜 README.md
```

---

## ⚙️ Instalasi

**1. Clone repository ini**
```bash
git clone <url-repo-kamu>
cd <nama-folder>
```

**2. Buat dan aktifkan virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install pytest-playwright allure-pytest
```

**4. Install browser Playwright**
```bash
playwright install
```

---

## ▶️ Menjalankan Test

```bash
# Jalankan semua test
pytest test_login.py -v

# Jalankan satu test tertentu
pytest test_login.py::test_login_positif -v

# Jalankan dengan Allure report
pytest test_login.py -v --alluredir=allure-results
allure serve allure-results
```

---

## 🧪 Daftar Test Case

### ✅ Login Positif

| Test Case | Skenario | Ekspektasi |
|---|---|---|
| `test_login_positif` | Login dengan email & password yang benar | Redirect ke `/products`, username tampil benar |

### ❌ Login Negatif

| Test Case | Skenario | Ekspektasi |
|---|---|---|
| `test_login_negatif` | Password salah | Tetap di `/login`, muncul pesan *"Invalid login credentials"* |
| `test_login_negatif` | Email typo (domain salah) | Tetap di `/login`, muncul pesan *"Invalid login credentials"* |
| `test_login_email_dan_password_kosong` | Submit tanpa mengisi apapun | Tetap di `/login`, browser menampilkan validasi pada field email |
| `test_login_format_email_tidak_valid` | Email tanpa karakter `@` | Tetap di `/login`, browser menampilkan validasi format email |
| `test_login_password_kosong` | Email diisi, password kosong | Tetap di `/login`, browser menampilkan validasi pada field password |

---

## 📝 Catatan

- Validasi field kosong dan format email ditangani oleh **browser secara native** (HTML `required` & `type="email"`), bukan oleh server. Oleh karena itu assertion menggunakan `el.validationMessage` via JavaScript evaluate, bukan `data-testid="login-error"`.
- Pesan validasi browser bersifat **language-dependent** (mengikuti bahasa browser). Assertion dibuat agar tidak bergantung pada teks spesifik satu bahasa.

---

## 🔗 Website yang Ditest

**URL:** https://test.kelasotomesyen.com  
**Halaman:** Login Page
