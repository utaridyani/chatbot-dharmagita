import requests
from typing import Optional, List

# mendapatkan informasi pupuh
def get_informasi(judul: str) -> Optional[str]:
    list_endpoint = f"http://127.0.0.1:8000/api/listallpupuh"
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

# mendapatkan contoh lagu pupuh
def get_contoh (judul:str) -> Optional[str]:

    if judul is None:
        return None

    list_endpoint = f"http://127.0.0.1:8000/api/listallpupuh"
    response_list = requests.get(list_endpoint)

    # print(f"check point 0")
    if response_list.status_code == 200:
        all_items = response_list.json()
        target_item_name = judul
        target_item_id = None

        for item in all_items:
            if all(word.lower() in item["nama_post"].lower() for word in target_item_name.split()):
                target_item_id = item["id_post"]
                # print(f"check point 1")
                break

        if target_item_id is not None:
            # print(f"check point 2")
            list_kategori_endpoint = f"http://127.0.0.1:8000/api/listkategoripupuh/{target_item_id}"
            response_kategori = requests.get(list_kategori_endpoint)

            if response_kategori.status_code == 200:
                kategori_data = response_kategori.json()
                judul_lagu = [item["nama_post"] for item in kategori_data]
                # print(f"berhasil")
                return judul_lagu
            else:
                # print(f"check point 3")
                print(f"No match for {target_item_name} in {item['nama_post']}")
        else:
            # print(f"check point 4")
            print(f"No match for {target_item_name} in {item['nama_post']}")


    return None

# mendapatkan audio
def get_audio_pupuh(judul: str) -> Optional[List[dict]]:
    list_endpoint = f"http://127.0.0.1:8000/api/listallpupuh"
    response_list = requests.get(list_endpoint)
    id_post_pupuh = None
    id_post = None

    if response_list.status_code == 200:
        all_items = response_list.json()
        target_item_name = judul

        for item in all_items:
            # mencari judul pupuh
            id_post_pupuh = item["id_post"]
            list_judul = f"http://127.0.0.1:8000/api/listkategoripupuh/{id_post_pupuh}"
            response_judul_pupuh = requests.get(list_judul)

            if response_judul_pupuh.status_code == 200:
                all_items_judul = response_judul_pupuh.json()
                
                for item in all_items_judul:
                    if all(word.lower() in item["nama_post"].lower() for word in target_item_name.split()):
                        id_post = item["id_post"]
                        print(f"{id_post}")
                        list_audio = f"http://127.0.0.1:8000/api/listaudiopupuh/{id_post}"
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