from playwright.sync_api import sync_playwright, expect
import pytest
import allure

#Setiap kemungkinan yang kita coba, itu disebut dengan test case, dan 
#setiap test case itu harus memiliki hasil yang pasti, apakah itu berhasil atau gagal.

@allure.title("Test Login Positif")
@allure.description("Memastikan bahwa user dapat login dengan email dan password yang benar")
@allure.severity(allure.severity_level.CRITICAL) #Severity digunakan untuk menentukan tingkat keparahan dari sebuah test case, apakah itu critical, normal, atau minor.
def test_login_positif():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=600)
        page = browser.new_page()
        page.goto(url="https://test.kelasotomesyen.com/", timeout=10000)
        page.locator('[data-testid="login-email-input"]').fill('uno.testing3@gmail.com')
        page.locator('[data-testid="login-password-input"]').fill('1234567890')
        page.locator('[data-testid="login-submit-button"]').click()

        #Mengecek apakah URL sudah benar setelah login
        expect(page).to_have_url("https://test.kelasotomesyen.com/products")
        
        #Mengecek apakah title sudah benar setelah login
        title = page.title()
        assert title == "Kelas Otomesyen Test App"

        #Mengecek apakah username sudah benar setelah login
        username = page.locator('[data-testid="user-email"]').inner_text()
        assert username == "uno"

        #Selama masih bisa di cover dengan expect, tidak perlu pakai assert
        #Menggunakan assert jika kita perlu melakukan penjumlahan atau operasi lain sebelum melakukan pengecekan
        #Contoh:
        # total_product = page.locator('[data-testid="product-item"]').count()
        # assert total_product == 6

data_error_login = [('uno.testing3@gmail.com', 'salah', "Invalid login credentials"), 
                    ('uno.testing3@gmail.co', '1234567890', "Invalid login credentials")]

# @ merupakan fungsi decorator, dimana fungsi ini berjalan jika diletakkan diatas fungsi lain.

@allure.title("Test Login Negatif")
@allure.description("Memastikan bahwa user tidak dapat login dengan email dan password yang salah")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize('username, password, error', data_error_login)
def test_login_negatif(username, password, error):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=600)
        page = browser.new_page()
        page.goto(url="https://test.kelasotomesyen.com/", timeout=10000)
        page.locator('[data-testid="login-email-input"]').fill(username)
        page.locator('[data-testid="login-password-input"]').fill(password)
        page.locator('[data-testid="login-submit-button"]').click()

        #Mengecek apakah URL sudah benar setelah login
        expect(page).to_have_url("https://test.kelasotomesyen.com/login")
        
        #Mengecek apakah title sudah benar setelah login
        title = page.title()
        assert title == "Kelas Otomesyen Test App"

        expect(page.locator('[data-testid="login-error"]')).to_be_visible()

        error_message = page.locator('[data-testid="login-error"]').inner_text()
        assert error_message == error

@allure.title("Test Login dengan Email dan Password Kosong")
@allure.description("Memastikan bahwa user tidak dapat login ketika email dan password tidak diisi")
@allure.severity(allure.severity_level.NORMAL)
def test_login_email_dan_password_kosong():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=600)
        page = browser.new_page()
        page.goto(url="https://test.kelasotomesyen.com/", timeout=10000)
 
        # Langsung klik submit tanpa mengisi apapun
        page.locator('[data-testid="login-submit-button"]').click()
 
        # Memastikan user tetap berada di halaman login (tidak berpindah)
        expect(page).to_have_url("https://test.kelasotomesyen.com/login")
 
        # Browser menampilkan validasi HTML native (required) pada field email,
        # sehingga request tidak dikirim ke server dan login-error tidak muncul.
        # Kita cek validasi tersebut via JavaScript evaluate.
        email_input = page.locator('[data-testid="login-email-input"]')
        validation_message = email_input.evaluate("el => el.validationMessage")
        assert validation_message != "", (
            f"Seharusnya ada pesan validasi pada field email, tapi tidak ditemukan"
        )

@allure.title("Test Login dengan Format Email Tidak Valid")
@allure.description("Memastikan bahwa user tidak dapat login ketika email tidak mengandung karakter @")
@allure.severity(allure.severity_level.MINOR)
def test_login_format_email_tidak_valid():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=600)
        page = browser.new_page()
        page.goto(url="https://test.kelasotomesyen.com/", timeout=10000)
        page.locator('[data-testid="login-email-input"]').fill('uno.testing3gmail.com')
        page.locator('[data-testid="login-password-input"]').fill('1234567890')
        page.locator('[data-testid="login-submit-button"]').click()
 
        # Memastikan user tetap berada di halaman login (tidak berpindah)
        expect(page).to_have_url("https://test.kelasotomesyen.com/login")
 
        # Browser menampilkan validasi HTML native (type="email") karena email tanpa @.
        # Pesan validasi bersifat dinamis mengikuti input user, contoh:
        # "Sertakan '@' pada alamat email. 'uno.testing3gmail.com' tidak memiliki '@'."
        # Maka kita assert bahwa pesan mengandung tanda '@' sebagai penanda validasi format email.
        email_input = page.locator('[data-testid="login-email-input"]')
        validation_message = email_input.evaluate("el => el.validationMessage")
        assert "@" in validation_message, (
            f"Pesan validasi seharusnya menyebut '@', tapi didapat: '{validation_message}'"
        )

@allure.title("Test Login dengan Password Kosong")
@allure.description("Memastikan bahwa user tidak dapat login ketika password tidak diisi")
@allure.severity(allure.severity_level.NORMAL)
def test_login_password_kosong():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=600)
        page = browser.new_page()
        page.goto(url="https://test.kelasotomesyen.com/", timeout=10000)
        page.locator('[data-testid="login-email-input"]').fill('uno.testing3@gmail.com')
 
        # Password sengaja tidak diisi, langsung klik submit
        page.locator('[data-testid="login-submit-button"]').click()
 
        # Memastikan user tetap berada di halaman login (tidak berpindah)
        expect(page).to_have_url("https://test.kelasotomesyen.com/login")
 
        # Browser menampilkan validasi HTML native (required) pada field password.
        # Pesan validasi berbeda-beda tergantung bahasa browser, maka kita hanya
        # memastikan pesan tidak kosong (artinya validasi browser berhasil berjalan).
        password_input = page.locator('[data-testid="login-password-input"]')
        validation_message = password_input.evaluate("el => el.validationMessage")
        assert validation_message != "", (
            f"Seharusnya ada pesan validasi pada field password, tapi tidak ditemukan"
        )