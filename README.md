Cara Menjalankan Program ETL:
disarankan untuk menggunakan virtual environment python, anda dapat mengaktifkannya dengan
python3 -m  venv <nama virtual environment>

1. Install dependensi:
pip install -r requirements.txt

2. Jalankan ETL:
python main.py

3. Output akan tersimpan di:
products.csv

4. Menjalankan unit test pada folder tests
python3 -m pytest tests

5. Menjalankan test coverage pada folder tests
coverage run -m pytest tests

Penjelasan File:
- extract.py: Mengambil data dari website Fashion Studio (50 halaman).
- transform.py: Membersihkan harga, rating, warna, dan menghapus duplikasi.
- load.py: Menyimpan data bersih ke CSV.
- main.py: Menjalankan seluruh proses ETL.
