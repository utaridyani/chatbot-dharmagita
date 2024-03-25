from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


import requests
from actions.pupuh_actions import get_informasi, get_contoh, get_audio_pupuh
from actions.yadnya_actions import get_informasi_upacara, get_contoh_upacara
from actions.kidung_actions import get_informasi_kidung, get_contoh_kidung, get_audio_kidung
from actions.laguanak_actions import get_informasi_laguanak, get_contoh_laguanak, get_audio_laguanak
from actions.kekawin_actions import get_informasi_kekawin, get_contoh_kekawin, get_audio_kekawin
from actions.mantram_actions import get_informasi_mantram, get_contoh_mantram

class DisplayResponseAction(Action):
    def name(self) -> Text:
        return "action_display_response"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        message = tracker.latest_message.get("text")
        intent = tracker.latest_message.get("intent", {}).get("name")
        confidence = tracker.latest_message.get("intent", {}).get("confidence")
        entities = tracker.latest_message.get("entities", [])
        intent_ranking = tracker.latest_message.get("intent_ranking", [])

        response = {
            "text": message,
            "intent": {"name": intent, "confidence": confidence},
            "entities": entities,
            "intent_ranking": intent_ranking
        }

        print(response)

        return []


class InformasiDharmagitaAction(Action):
    def name(self) -> Text:
        return "action_informasi_dharmagita"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        jenis = tracker.get_slot("jenis")
        judul = tracker.get_slot("judul")

        # general information
        if jenis == "dharmagita" or "dharma gita":
            dispatcher.utter_message(text=f"Dharma Gita sebagai nyanyian keagamaan umat Hindu biasa digunakan untuk mengiringi berbagai kegiatan keagamaan khususnya yang berhubungan dengan ritual/yadnya.")

        elif jenis == "sekar agung":
            dispatcher.utter_message(text=f"Dharma Gita sebagai nyanyian keagamaan umat Hindu biasa digunakan untuk mengiringi berbagai kegiatan keagamaan khususnya yang berhubungan dengan ritual/yadnya.")

        # get informasi pupuh
        elif jenis == "pupuh":
            informasi = get_informasi(judul)    

            if informasi is not None:
                dispatcher.utter_message(text=f"{informasi}")
            else:
                dispatcher.utter_message(text=f"Wah sayang sekali saya belum memiliki informasi mengenai {judul}")
        
        # get informasi kidung
        elif jenis == "kidung" :
            informasi = get_informasi_kidung(judul)

            if informasi is not None:
                dispatcher.utter_message(text=f"{informasi}")
            else:
                dispatcher.utter_message(text=f"Wah sayang sekali saya belum memiliki informasi mengenai {judul}")
        
        # get informasi lagu anak
        elif jenis == "lagu" or jenis == "gending" :
            informasi = get_informasi_laguanak(judul)

            if informasi is not None:
                dispatcher.utter_message(text=f"{informasi}")
            else:
                dispatcher.utter_message(text=f"Wah sayang sekali saya belum memiliki informasi mengenai {jenis} {judul}")

        # get informasi kekawin
        elif jenis == "kekawin":
            informasi = get_informasi_kekawin(judul)

            if informasi is not None:
                dispatcher.utter_message(text=f"{informasi}")
            else:
                dispatcher.utter_message(text=f"Wah sayang sekali saya belum memiliki informasi mengenai {jenis} {judul}")

        # get informasi mantram
        elif jenis == "mantram":
            informasi = get_informasi_mantram(judul)

            if informasi is not None:
                deskripsi = informasi["deskripsi"]
                bait = informasi["bait_mantra"]
                arti = informasi["arti_mantra"]
                
                if arti is not None:
                    dispatcher.utter_message(text=f"{deskripsi} /nBait Mantram : {bait} /nArti Mantram : {arti}")
                else :
                    dispatcher.utter_message(text=f"{deskripsi} /nBait Mantram : {bait}")
            else:
                dispatcher.utter_message(text=f"Wah sayang sekali saya belum memiliki informasi mengenai {jenis} {judul}")
       
        else:
                dispatcher.utter_message(text=f"Wah sayang sekali saya belum memiliki informasi yang anda inginkan")
        return []
    
class ContohDharmagitaAction(Action):
    def name(self) -> Text:
        return "action_contoh_dharmagita"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        jenis = tracker.get_slot("jenis")
        judul = tracker.get_slot("judul")
        yadnya_type = tracker.get_slot("yadnya_type")

        # get contoh pupuh
        if jenis == "pupuh":
            informasi = get_contoh(judul)    

            if informasi is not None:
                informasi_cleaned = [item.translate(str.maketrans("", "", "[]")) for item in informasi]
                dispatcher.utter_message(text=f"Berikut merupakan contoh judul dari {jenis} {judul} : {', '.join(informasi_cleaned)}")
            else:
                dispatcher.utter_message(text=f"Wah sayang sekali saya belum memiliki informasi yang anda inginkan")
        
        # get contoh kidung
        elif jenis == "kidung":
            informasi = get_contoh_kidung(yadnya_type)

            if informasi is not None:
                informasi_cleaned = [item.translate(str.maketrans("", "", "[]")) for item in informasi]
                dispatcher.utter_message(text=f"Berikut merupakan contoh dari {jenis} {yadnya_type} : {', '.join(informasi_cleaned)}")
            else:
                dispatcher.utter_message(text=f"Wah sayang sekali saya belum memiliki informasi yang anda inginkan")
        
        # get contoh lagu anak
        elif jenis == "lagu anak" or jenis == "sekar rare":
            informasi = get_contoh_laguanak(jenis)

            if informasi is not None:
                informasi_cleaned = [item.translate(str.maketrans("", "", "[]")) for item in informasi]
                dispatcher.utter_message(text=f"Berikut merupakan contoh dari {jenis}: {', '.join(informasi_cleaned)}")
            else:
                dispatcher.utter_message(text=f"Wah sayang sekali saya belum memiliki informasi yang anda inginkan")
        
        # get contoh kekawin
        elif jenis == "kekawin" or jenis == "kakawin":
            informasi = get_contoh_kekawin(jenis)

            if informasi is not None:
                informasi_cleaned = [item.translate(str.maketrans("", "", "[]")) for item in informasi]
                dispatcher.utter_message(text=f"Berikut merupakan contoh dari {jenis}: {', '.join(informasi_cleaned)}")
            else:
                dispatcher.utter_message(text=f"Wah sayang sekali saya belum memiliki informasi yang anda inginkan")
        
        # get contoh mantram
        elif jenis == "mantram":
            informasi = get_contoh_mantram(yadnya_type)

            if informasi is not None:
                informasi_cleaned = [item.translate(str.maketrans("", "", "[]")) for item in informasi]
                dispatcher.utter_message(text=f"Berikut merupakan contoh dari {jenis} untuk {yadnya_type}: {', '.join(informasi_cleaned)}")
            else:
                dispatcher.utter_message(text=f"Wah sayang sekali saya belum memiliki informasi yang anda inginkan")
        
        else:
            dispatcher.utter_message(text=f"Wah sayang sekali saya belum memiliki informasi yang anda inginkan")
        return []
        
class LirikDharmagitaAction(Action):
    def name(self) -> Text:
        return "action_lirik_dharmagita"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text=f"Action 'action_lirik_dharmagita' is being executed.")
        jenis = tracker.get_slot("jenis")
        judul = tracker.get_slot("judul")

        return []
    
class AudioDharmagitaAction(Action):
    def name(self) -> Text:
        return "action_audio_dharmagita"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        judul = tracker.get_slot("judul")
        chat_id = tracker.sender_id
        bot_token = '5875579217:AAFALeGofJ80CKG9Eva8BxxllWLHenf96CY'
        api_url = f"https://api.telegram.org/bot{bot_token}/sendAudio"
        nama_file = None
        
        # cek kidung
        nama_file_kidung = get_audio_kidung(judul)
        if nama_file_kidung is not None:
            nama_file = nama_file_kidung
        else:
            #  cek pupuh
            nama_file_pupuh = get_audio_pupuh(judul)
            if nama_file_pupuh is not None:
                nama_file = nama_file_pupuh
            else:
                # cek lagu anak
                nama_file_laguanak = get_audio_laguanak(judul)
                if nama_file_laguanak is not None:
                    nama_file = nama_file_laguanak
                else:
                    # cek kekawin
                    nama_file_kekawin = get_audio_kekawin(judul)
                    nama_file = nama_file_kekawin
        print(nama_file)
        print(judul)

        if nama_file is not None :
            audio_file_url = f"http://127.0.0.1:8000/audioku/{nama_file}"
            response = requests.get(audio_file_url)

            if response.status_code == 200:
                audio_data = {'chat_id': chat_id}
                audio_files = {'audio': (nama_file, response.content)}

                send_audio_response = requests.post(api_url, data=audio_data, files=audio_files)

                if send_audio_response.status_code == 200:
                    print("Audio file sent successfully!")
                else:
                    print(f"Failed to send audio file. Status code: {send_audio_response.status_code}, Response: {send_audio_response.text}")
                    dispatcher.utter_message(text=f"Terjadi kesalahan saat saya mengirimkan audio {judul}.")

            else:
                print(f"Failed to download audio file. Status code: {response.status_code}")
                dispatcher.utter_message(text=f"Terjadi kesalahan saat saya mengirimkan audio {judul}.")
        else :
                dispatcher.utter_message(text=f"Wah sayang sekali saya belum memiliki file audio dari {judul}. Untuk selanjutnya pastikan kamu sudah mengirimkan secara spesifik judul dari audio yang kamu ingin dengarkan ya!")
        return []
    

# YADNYA
class ActionContohYadnya(Action):
    def name(self) -> Text:
        return "action_contoh_yadnya"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        yadnya_type = tracker.get_slot("yadnya_type")

        informasi = get_contoh_upacara(yadnya_type)

        if informasi is not None:
            informasi_cleaned = [item.translate(str.maketrans("", "", "[]")) for item in informasi]
            dispatcher.utter_message(text=f"Berikut merupakan contoh upacara dari {yadnya_type} : {', '.join(informasi_cleaned)}")
        else:
            dispatcher.utter_message(text=f"Wah sayang sekali saya belum memiliki informasi mengenai contoh dari {yadnya_type}")
           
        return []
    
class ActionInformasiYadnya(Action):
    def name(self) -> Text:
        return "action_informasi_yadnya"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        yadnya_type = tracker.get_slot("yadnya_type")

        if yadnya_type == "yadnya":
            dispatcher.utter_message(text=f"Yadnya adalah korban suci secara tulus ikhlas atas dasar kesadaran dan cinta kasih yang keluar dari hati sanubari sebagai pengabdian yang sejati kepada Tuhan Yang Maha Esa Wasa")
        elif yadnya_type == "dewa yadnya":
            dispatcher.utter_message(text=f"Dewa Yadnya adalah Yadnya yang wajib dipersembahkan. Hal itu karena Dewa Yadnya merupakan persembahan yang dilakukan kepada Tuhan serta segala manifestasi-Nya.")
        elif yadnya_type == "pitra yadnya":
            dispatcher.utter_message(text=f"Pitra Yadnya adalah persembahan kepada leluhur yang telah meninggal dan termasuk persembahan kepada orang tua.")
        elif yadnya_type == "manusa yadnya":
            dispatcher.utter_message(text=f"Manusa Yadnya adalah persembahan kepada sesama manusia, bentuk persembahannya dapat berupa moril atau materiil.")
        elif yadnya_type == "rsi yadnya":
            dispatcher.utter_message(text=f"Rsi Yadnya merupakan persembahan kepada Rsi (pendeta, guru, orang suci). Tujuan dari Rsi Yadnya adalah wujud rasa terima kasih.")
        elif yadnya_type == "bhuta yadnya":
            dispatcher.utter_message(text=f"Bhuta Yadnya artinya adalah persembahan kepada makhluk yang derajatnya lebih rendah dari manusia, tujuannya adalah mengharmoniskan lingkungan hidup.")
        elif yadnya_type == None:
            dispatcher.utter_message(text=f"Maaf saya tidak memahami pertanyaan Anda")
        else:
            informasi = get_informasi_upacara(yadnya_type)    

            if informasi:
                chat_id = tracker.sender_id

                bot_token = '5875579217:AAFALeGofJ80CKG9Eva8BxxllWLHenf96CY'
                api_url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"

                nama_file = informasi['gambar']
                photo_file_url = f'http://127.0.0.1:8000/gambarku/{nama_file}'

                response = requests.get(photo_file_url)

                # informasi in text
                text_message = f"{informasi['deskripsi']}"
                dispatcher.utter_message(text=f"{text_message}")

                # informasi in photo
                photo_data = {'chat_id': chat_id}
                photo_files = {'photo': (nama_file, response.content, 'image/jpeg')}

                send_photo_response = requests.post(api_url, data=photo_data, files=photo_files)
                if send_photo_response.status_code == 200:
                    print("Photo sent successfully!")
                else:
                    print(f"Failed to send photo. Status code: {send_photo_response.status_code}, Response: {send_photo_response.text}")
                    print(f"{photo_file_url}")
            
            else:
                dispatcher.utter_message(text=f"Wah sayang sekali saya belum memiliki informasi mengenai {yadnya_type}")

