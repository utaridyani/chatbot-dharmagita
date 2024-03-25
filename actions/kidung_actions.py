import requests
from typing import Optional, List

# mendapatkan informasi kidung
def get_informasi_kidung(judul: str) -> Optional[str]:
    list_endpoint = f"http://127.0.0.1:8000/api/listallkidung"
    response_list = requests.get(list_endpoint)

    if response_list.status_code == 200:
        all_items = response_list.json()
        target_item_name = judul
        target_item_id = None

        for item in all_items:
            if all(word.lower() in item["nama_post"].lower() for word in target_item_name.split()):
                return item["deskripsi"]
            else:
                print(f"No match for {target_item_name} in {item['nama_post']}")

    return None

# mendapatkan contoh kidung yadnya
def get_contoh_kidung (yadnya_type:str) -> Optional[str]:

    if yadnya_type is None:
        return None

    list_endpoint = f"http://127.0.0.1:8000/api/listallkidung"
    response_list = requests.get(list_endpoint)

    if response_list.status_code == 200:
        all_items = response_list.json()
        target_item_name = yadnya_type
        judul_kidung = []

        for item in all_items:
            if all(word.lower() in item["kategori"].lower() for word in target_item_name.split()):
                judul_kidung.append(item["nama_post"])

        if judul_kidung: 
            return judul_kidung
        else:
            print(f"No match for {target_item_name}")

    return None

# mendapatkan audio kidung
def get_audio_kidung(judul: str) -> Optional[List[dict]]:
    list_endpoint = f"http://127.0.0.1:8000/api/listallkidung"
    response_list = requests.get(list_endpoint)
    id_post = None

    if response_list.status_code == 200:
        all_items = response_list.json()
        target_item_name = judul

        for item in all_items:
            if all(word.lower() in item["nama_post"].lower() for word in target_item_name.split()):
                id_post = item["id_post"]

                list_audio = f"http://127.0.0.1:8000/api/listaudiokidung/{id_post}"
                response_audio = requests.get(list_audio)
                judul_audio = None

                if response_audio.status_code == 200:
                    audio_data = response_audio.json()
                    if audio_data and "data" in audio_data:
                        judul_audio = audio_data["data"][0]["audio"]
                        return judul_audio
                    else:
                        return None

            else:
                return None
    return None