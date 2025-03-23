# Program Deteksi Gempa Terbaru 
Program ini dibuat dengan menggunakan bahasa python dengan mengambil data realtime dari BMKG api.

Rest API dapat diakses pada link berikut : 

[Link data gempa bumi BMKG ](https://data.bmkg.go.id/gempabumi/)

[REST-API gempa bumi terbaru ](https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json)

Gambar Shakemap (peta guncangan) diawali dengan URL ```https://data.bmkg.go.id/DataMKG/TEWS/ ```


## Penjelasan Kode

### 1. Import Library

```python
import requests
import io 
```

**Penjelasan:**  
- **`requests`**: Digunakan untuk melakukan HTTP request guna mengambil data dari API BMKG.  
- **`io`**: Digunakan untuk operasi input/output, dalam hal ini untuk menulis file teks dengan encoding tertentu.

---

### 2. Fungsi `fetch_latest_earthquake_data()`

```python
def fetch_latest_earthquake_data():
    json_url = "https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json"
    try:
        response = requests.get(json_url)
        if response.status_code == 200:
            data = response.json()
            if "Infogempa" in data and "gempa" in data["Infogempa"]:
                # tipe data dictionary
                gempa_data = data["Infogempa"]["gempa"]
                return gempa_data
            else:
                print("Struktur JSON tidak sesuai.")
                return {}
        else:
            print("Error fetching data:", response.status_code)
            return {}
    except Exception as e:
        print("Terjadi kesalahan:", e)
        return {}
```

**Penjelasan:**  
- **Tujuan Fungsi:** Mengambil data gempa terbaru dari URL BMKG dan mengembalikannya dalam bentuk dictionary.  
- **Langkah-langkah:**
  - Mendefinisikan URL JSON yang berisi data gempa.
  - Melakukan HTTP GET request menggunakan `requests.get()`.
  - Memeriksa status kode response, jika `200` (OK) maka:
    - Mengkonversi response menjadi format JSON.
    - Memeriksa apakah struktur JSON memiliki key `"Infogempa"` dan `"gempa"`.
    - Jika struktur sesuai, data gempa disimpan dalam variabel `gempa_data` dan dikembalikan.
  - Jika struktur JSON tidak sesuai atau terjadi error, maka fungsi mengembalikan dictionary kosong dan menampilkan pesan error.

---

### 3. Bagian Utama Program (`if __name__ == "__main__":`)

```python
if __name__ == "__main__":
    gempa_data = fetch_latest_earthquake_data()
    if gempa_data:
        print("Data Gempa Terbaru:")
        # Menggunakan key 'Wilayah' dari gempa_data untuk membuat nama file
        filename = f"{gempa_data['Wilayah']}.txt"
        with io.open(filename, "w", encoding="utf-8") as file:
            for key, value in gempa_data.items():
                if key == "Shakemap":
                    output = f"Lihat Shakemap : https://data.bmkg.go.id/DataMKG/TEWS/{value}\n"
                    print(output, end='')
                    file.write(output)
                else:
                    output = f"{key}: {value}\n"
                    print(output, end='')
                    file.write(output)
    else:
        print("Data gempa tidak tersedia.")
```

**Penjelasan:**  
- **`if __name__ == "__main__":`**  
  Menjamin bahwa kode di bawahnya hanya akan dijalankan ketika file ini dieksekusi secara langsung, bukan ketika diimpor sebagai modul.

- **Memanggil Fungsi `fetch_latest_earthquake_data()`:**  
  Mengambil data gempa terbaru. Jika data tersedia (tidak kosong), program akan melanjutkan untuk memproses dan menampilkan data.

- **Menentukan Nama File:**  
  - Menggunakan nilai dari key `"Wilayah"` pada dictionary `gempa_data` untuk membuat nama file (misalnya, "181 km BaratLaut TANIMBAR.txt").
  
- **Menulis Data ke File dan Menampilkan di Terminal:**  
  - Menggunakan `with io.open(...)` untuk membuka file dengan mode tulis (`w`) dan encoding `utf-8`.
  - Melakukan iterasi terhadap tiap key dan value pada `gempa_data`:
    - Jika key adalah `"Shakemap"`, maka program membuat URL lengkap untuk melihat image shakemap dan menuliskannya ke file serta menampilkannya ke terminal.
    - Untuk key lainnya, data ditampilkan dan ditulis ke file dengan format `key: value`.
  - Jika tidak ada data gempa yang diambil, program akan menampilkan pesan "Data gempa tidak tersedia."
