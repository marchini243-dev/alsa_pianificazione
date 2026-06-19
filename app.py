import streamlit as st
import pandas as pd
from PIL import Image

# Configurazione pagina e stile
st.set_page_config(layout="wide", page_title="ALSA Mission Control")

st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    .card { background-color: #ffffff; border-radius: 15px; padding: 20px; border: 1px solid #dcdcdc; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.header("🌌 Mission Setup")
    autore = st.text_input("Comandante", "Socio ALSA")
    soggetto = st.text_input("Target", "Sh2-91")
    target_ore = st.number_input("Goal (h)", 1.0, 100.0, 40.0)
    img_file = st.file_uploader("Carica Reference", type=['jpg', 'png'])
    st.divider()
    st.subheader("🛠️ Hardware")
    ottica = st.text_input("Ottica", "AP 86/460")
    camera = st.text_input("Camera", "Toup 2600 MM")
    montatura = st.text_input("Montatura", "EQ8-R Pro")
    guida = st.text_input("Guida", "ZWO OAG-L")
    
    st.subheader("📸 Esposizioni")
    ha_s, ha_n = st.number_input("Hα (sec)", 0, 999, 300), st.number_input("Hα (scatti)", 0, 999, 0)
    o3_s, o3_n = st.number_input("OIII (sec)", 0, 999, 300), st.number_input("OIII (scatti)", 0, 999, 0)
    si2_s, si2_n = st.number_input("SII (sec)", 0, 999, 300), st.number_input("SII (scatti)", 0, 999, 0)
    hb_s, hb_n = st.number_input("Hβ (sec)", 0, 999, 300), st.number_input("Hβ (scatti)", 0, 999, 0)
    bb_s, bb_n = st.number_input("Broadband (sec)", 0, 999, 180), st.number_input("Broadband (scatti)", 0, 999, 0)

# --- CALCOLI ---
totale = ((ha_s*ha_n)+(o3_s*o3_n)+(si2_s*si2_n)+(hb_s*hb_n)+(bb_s*bb_n)) / 3600
progresso = min(totale / target_ore, 1.0)

# --- LAYOUT FINALE ---
st.title(f"🔭 {soggetto.upper()}")
st.write(f"**Missione guidata da:** {autore}")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if img_file: st.image(img_file, use_container_width=True)
    else: st.info("Carica immagine target")
    st.subheader("Progresso Missione")
    st.progress(progresso)
    st.markdown(f"### {totale:.1f} / {target_ore:.1f} Ore")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("⚙️ Configurazione Setup")
    st.markdown(f"**Ottica:** {ottica}  \n**Camera:** {camera}  \n**Montatura:** {montatura}  \n**Guida:** {guida}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("") 
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Analisi Esposizioni")
    data = {"Filtro": ["Hα", "OIII", "SII", "Hβ", "Broadband"], 
            "Scatti": [ha_n, o3_n, si2_n, hb_n, bb_n],
            "Posa": [f"{ha_s}s", f"{o3_s}s", f"{si2_s}s", f"{hb_s}s", f"{bb_s}s"]}
    df = pd.DataFrame(data)
    st.table(df[df["Scatti"] > 0])
    st.markdown('</div>', unsafe_allow_html=True)