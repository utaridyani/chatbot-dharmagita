import requests
from typing import Optional

def get_informasi_upacara (yadnya_type:str) -> Optional[str]:
    informasi = {}

    list_endpoint = f"http://127.0.0.1:8000/api/listallyadnya"
    response_list = requests.get(list_endpoint)

    if response_list.status_code == 200:
        all_items = response_list.json()
        target_item_name = yadnya_type
        target_item_id = None

        for item in all_items:
            if item["nama_post"].lower() == target_item_name:
                target_item_id = item["id_post"]
                break
        
        if target_item_id is not None:
            detail_endpoint = f"http://127.0.0.1:8000/api/detailyadnya/{target_item_id}"
            response_detail = requests.get(detail_endpoint)

            if response_detail.status_code == 200:
                detail = response_detail.json()
                gambar = f"http://127.0.0.1:8000/gambarku/{detail['gambar']}"
                informasi = {
                    "deskripsi": detail["deskripsi"],
                    "gambar": detail['gambar'],
                }
            return informasi
    return None

def get_contoh_upacara (yadnya_type:str) -> Optional[str]:

    list_endpoint = f"http://127.0.0.1:8000/api/listallyadnya"
    response_list = requests.get(list_endpoint)

    if response_list.status_code == 200:
        all_items = response_list.json()
        target_item_name = yadnya_type
        nama_post = []

        for item in all_items:
            if item["kategori"].lower() == target_item_name:
                nama_post.append(item["nama_post"])
        
        return nama_post
    return None