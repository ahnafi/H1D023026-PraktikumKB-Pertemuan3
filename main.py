import requests
import io 

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
