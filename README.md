Automation Testing Tutorial

#Deskripsi
Automation test script untuk login page (https://the-internet.herokuapp.com/login) menggunakan Selenium, pytest, dan WebDriver Manager.

#Scenario
-Scenario 1
Login dengan Kredensial yang Valid
Terdapat halaman login yang dapat diakses
Saya memasukkan username yang valid "tomsmith"
Saya memasukkan password yang valid "SuperSecretPassword!"
Saya mengklik tombol login
Saya melihat pesan sukses "You logged into a secure area!"
Saya diarahkan ke halaman secure area
Saya melihat tombol logout

-Scenario 2
Terdapat halaman login yang dapat diakses
Saya memasukkan username yang valid "tomsmith"
Saya memasukkan password yang tidak valid "WrongPassword123"
Saya mengklik tombol login
Saya melihat pesan error "Your password is invalid!"
Saya tetap berada di halaman login
Saya melihat field username yang masih ditampilkan

#Cara Menggunakan
-Buat virtual environment
python -m venv venv

-Aktifkan virtual environment
venv\Scripts\activate

-Install dependencies
pip install -r requirements.txt

-Jalankan test
pytest tests/test_login.py -v**
