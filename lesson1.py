import streamlit as st

st.header('หา BMI')

if st.button('โฆษณา'):
   st.video('https://youtu.be/0IKw2BIWc4I?si=uw8VDXGG3l0emnqJ')

st.image('https://i0.wp.com/ethicalinc.com/wp-content/uploads/2022/11/iStockLargeBMI.jpg?fit=2048%2C1365&ssl=1')

st.set_page_config(page_title='BODY MASS INDEX : wab Applicaton',page_icon='🏳️‍🌈')
kg=st.number_input('นํ้าหนัก (kg) :')
cm=st.number_input('ส่วนสูง (cm) :')

from gtts import gTTS
import io

if st.button('คํานวณ'):
   bmi=kg/(cm/100)**2    
   tt=f'ค่า BMI ของคุณคือ {bmi:.2f}'
   if bmi < 18.5:
     st.info(tt)
     st.image('C:/aipython/BMI ผอม.png')
     word="ผอม"
   elif bmi < 24.9:
     st.success(tt)
     st.image('C:/aipython/BMI ปกติ.png')
     word="ปกติ"
   elif bmi < 29.9:
     st.success(tt)
     st.image('C:/aipython/BMI อ้วน.png')
     word="อ้วน"
   elif bmi < 34.9:
     st.warning(tt)
     st.image('C:/aipython/BMI อ้วน1.png')
     word="อ้วน2"
   elif bmi > 35:
     st.error(tt)
     st.image('C:/aipython/BMI อ้วน2.png')
     word="อ้วน3"
     
   tts = gTTS(text=word, lang='th')
   mp3_fp = io.BytesIO()
   tts.write_to_fp(mp3_fp)
   mp3_fp.seek(0)
   st.audio(mp3_fp, format='aidio/mp3')

import streamlit as st
import requests
from pathlib import Path

st.title("Botnoi Voice API Demo")

API_URL = "https://api-voice.botnoi.ai/openapi/v1/generate_audio"
API_TOKEN = "EJOGfkoPwJ21uCe5qv6HpFcNTXBil7pR"

text_input = st.text_input("ข้อความที่ต้องการแปลงเป็นเสียง", "สวัสดีครับ")
speaker_id = st.text_input("Speaker ID", "1")
generate_btn = st.button("Generate Voice")

if generate_btn:
    payload = {
        "text": text_input,
        "speaker": speaker_id,
        "volume": 1,
        "speed": 1,
        "type_media": "mp3",
        "save_file": "true",
        "language": "th",
        "page": "user"
    }

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "botnoi-token": API_TOKEN
    }

    try:
        res = requests.post(API_URL, json=payload, headers=headers, timeout=30)
        res.raise_for_status()
        data = res.json()
        st.write("API Response:", data)

        # ดึง URL ไฟล์เสียง
        audio_url = (
            data.get("url")
            or data.get("audio_url")
            or (data.get("data") or {}).get("url")
        )

        if audio_url:
            audio_bytes = requests.get(audio_url, timeout=30).content
            out_path = Path("botnoi_voice.mp3")
            out_path.write_bytes(audio_bytes)
            st.success(f"✅ บันทึกเสียงเรียบร้อย → {out_path.resolve()}")
            st.audio(audio_bytes, format="audio/mp3")
        else:
            st.error("ไม่พบลิงก์ไฟล์เสียงใน response")

    except Exception as e:
        st.error(f"เกิดข้อผิดพลาด: {e}")
