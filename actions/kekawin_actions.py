import requests
from typing import Optional, List

# mendapatkan informasi kekawin
def get_informasi_kekawin(judul: str) -> Optional[str]:
    list_endpoint = f"http://127.0.0.1:8000/api/listallkakawin"
    response_list = requests.get(list_endpoint)

    if response_list.status_code == 200:
        all_items = response_list.json()
        target_item_name = judul

        for item in all_items:
            if all(word.lower() in item["nama_post"].lower() for word in target_item_name.split()):
                return item["deskripsi"]
            else:
                print(f"No match for {target_item_name} in {item['nama_post']}")

    return None

# mendapatkan contoh kekawin
def get_contoh_kekawin (jenis:str) -> Optional[str]:

    if jenis is None:
        return None

    list_endpoint = f"http://127.0.0.1:8000/api/listallkakawin"
    response_list = requests.get(list_endpoint)

    if response_list.status_code == 200:
        all_items = response_list.json()
        target_item_name = jenis
        judul_kekawin = []

        for item in all_items:
            judul_kekawin.append(item["nama_post"])

        if judul_kekawin: 
            return judul_kekawin
        else:
            print(f"No match for {target_item_name}")

    return None

# mendapatkan audio kekawin
def get_audio_kekawin(judul: str) -> Optional[List[dict]]:
    list_endpoint = f"http://127.0.0.1:8000/api/listallkakawin"
    response_list = requests.get(list_endpoint)
    id_post_kekawin = None
    id_post = None

    if response_list.status_code == 200:
        all_items = response_list.json()
        target_item_name = judul

        for item in all_items:
            # mencari judul kekawin
            id_post_kekawin = item["id_post"]
            list_judul = f"http://127.0.0.1:8000/api/listkategorikakawin/{id_post_kekawin}"
            response_judul_kekawin = requests.get(list_judul)

            if response_judul_kekawin.status_code == 200:
                all_items_judul = response_judul_kekawin.json()
                for item in all_items_judul:
                    if all(word.lower() in item["nama_post"].lower() for word in target_item_name.split()):
                        id_post = item["id_post"]
                        print(f"{id_post}")
                        list_audio = f"http://127.0.0.1:8000/api/listaudiokakawin/{id_post}"
                        response_audio = requests.get(list_audio)
                        judul_audio = None
                        
                        if response_audio.status_code == 200:
                            audio_data = response_audio.json()
                            if "data" in audio_data and audio_data["data"] is not None and len(audio_data["data"]) > 0 :
                                judul_audio = audio_data["data"][0]["audio"]
                                return judul_audio
                            else:
                                return None
            else:
                return None
    return None