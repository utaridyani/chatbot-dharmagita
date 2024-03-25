import requests
from typing import Optional, List

# mendapatkan informasi mantram
def get_informasi_mantram(judul: str) -> Optional[str]:
    if judul is None:
        return None

    list_endpoint = f"http://127.0.0.1:8000/api/listallmantram"
    response_list = requests.get(list_endpoint)

    if response_list.status_code == 200:
        all_items = response_list.json()
        target_item_name = judul
        target_item_id = None

        for item in all_items:
            if all(word.lower() in item["nama_post"].lower() for word in target_item_name.split()):
                target_item_id = item["id_post"]
                print(target_item_id)
                break

        if target_item_id is not None:
            list_detailmantram_endpoint = f"http://127.0.0.1:8000/api/detailmantram/{target_item_id}"
            response_detail = requests.get(list_detailmantram_endpoint)

            if response_detail.status_code == 200:
                kategori_data = response_detail.json()
                return kategori_data
            else:
                print(f"No match for {target_item_name}")

        else:
            print(f"No match for {target_item_name} in {item['nama_post']}")


    # list_endpoint = f"http://127.0.0.1:8000/api/listallmantram"
    # response_list = requests.get(list_endpoint)

    # if response_list.status_code == 200:
    #     all_items = response_list.json()
    #     target_item_name = judul
    #     target_item_id = None

    #     for item in all_items:
    #         if all(word.lower() in item["nama_post"].lower() for word in target_item_name.split()):
    #             return item["deskripsi"]
    #         else:
    #             print(f"No match for {target_item_name} in {item['nama_post']}")

    return None

# mendapatkan contoh mantram
def get_contoh_mantram (yadnya_type:str) -> Optional[str]:

    if yadnya_type is None:
        return None
    
    list_endpoint = f"http://127.0.0.1:8000/api/listallmantram"
    response_list = requests.get(list_endpoint)
    
    if response_list.status_code == 200:
        all_items = response_list.json()
        target_item_name = yadnya_type
        judul_mantram = []

        for item in all_items:
            if item["kategori"] is not None :
                if all(word.lower() in item["kategori"].lower() for word in target_item_name.split()):
                    judul_mantram.append(item["nama_post"])

        if judul_mantram: 
            return judul_mantram
        else:
            print(f"No match for {target_item_name}")

    return None
