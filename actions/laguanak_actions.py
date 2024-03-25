import requests
from typing import Optional, List

# mendapatkan informasi lagu anak
def get_informasi_laguanak(judul: str) -> Optional[str]:
    list_endpoint = f"http://127.0.0.1:8000/api/listalllaguanak"
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

# mendapatkan contoh lagu anak
def get_contoh_laguanak (jenis:str) -> Optional[str]:

    list_endpoint = f"http://127.0.0.1:8000/api/listalllaguanak"
    response_list = requests.get(list_endpoint)

    if response_list.status_code == 200:
        all_items = response_list.json()
        judul_laguanak = []

        for item in all_items:
            judul_laguanak.append(item["nama_post"])

        if judul_laguanak: 
            return judul_laguanak
        else:
            print(f"No match for {jenis}")

    return None

# mendapatkan audio laguanak
def get_audio_laguanak(judul: str) -> Optional[List[dict]]:
    list_endpoint = f"http://127.0.0.1:8000/api/listalllaguanak"
    response_list = requests.get(list_endpoint)
    id_post_laguanak = None
    id_post = None

    if response_list.status_code == 200:
        all_items = response_list.json()
        target_item_name = judul

        for item in all_items:
            # mencari judul lagu anak
            id_post_laguanak = item["id_post"]
            list_judul = f"http://127.0.0.1:8000/api/listkategorilaguanak/{id_post_laguanak}"
            response_judul_laguanak = requests.get(list_judul)

            if response_judul_laguanak.status_code == 200:
                all_items_judul = response_judul_laguanak.json()
                # print(f"{all_items_judul}")
                for item in all_items_judul:
                    if all(word.lower() in item["nama_post"].lower() for word in target_item_name.split()):
                        id_post = item["id_post"]
                        print(f"{id_post}")
                        list_audio = f"http://127.0.0.1:8000/api/listaudiolaguanak/{id_post}"
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