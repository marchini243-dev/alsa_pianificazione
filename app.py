import streamlit as st
import pandas as pd
from PIL import Image
import os

# --- INTEGRAZIONE LIBRERIE ASTRONOMICHE ---
try:
    from astroquery.simbad import Simbad
    from astropy.coordinates import SkyCoord
except ImportError:
    os.system('pip install astroquery astropy')
    from astroquery.simbad import Simbad
    from astropy.coordinates import SkyCoord

# --- FUNZIONE CACHE PER SIMBAD (Evita di interrogare il server a ogni clic) ---
@st.cache_data(show_spinner=False)
def ottieni_coordinate_simbad(nome_target):
    if not nome_target:
        return "Nessun target inserito"
    try:
        # Aumentiamo il timeout per i server lenti di Strasburgo
        Simbad.TIMEOUT = 120 
        result_table = Simbad.query_object(nome_target)
        if result_table is not None:
            return f"RA: {result_table['RA'][0]} | DEC: {result_table['DEC'][0]}"
        else:
            return "Oggetto non trovato nel catalogo SIMBAD"
    except Exception as e_simbad:
        # Fallback: Se SIMBAD va in timeout o rifiuta la connessione, usiamo SESAME
        try:
            c = SkyCoord.from_name(nome_target)
            ra_str = c.ra.to_string(unit='hour', sep=' ', precision=2)
            dec_str = c.dec.to_string(unit='deg', sep=' ', precision=2)
            return f"RA: {ra_str} | DEC: {dec_str} (via SESAME)"
        except Exception as e_sesame:
            # Mostra l'errore effettivo per capire se è un problema di rete o di firewall locale
            err_msg = str(e_simbad).split('\n')[0][:50]
            return f"Errore Server: {err_msg}..."

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
    filtri = st.text_input("Filtri","Antlia")
    
    st.divider()
    
    st.subheader("📸 Esposizioni")
    ha_s, ha_n = st.number_input("Hα (sec)", 0, 999, 300), st.number_input("Hα (scatti)", 0, 999, 0)
    o3_s, o3_n = st.number_input("OIII (sec)", 0, 999, 300), st.number_input("OIII (scatti)", 0, 999, 0)
    si2_s, si2_n = st.number_input("SII (sec)", 0, 999, 300), st.number_input("SII (scatti)", 0, 999, 0)
    hb_s, hb_n = st.number_input("Hβ (sec)", 0, 999, 300), st.number_input("Hβ (scatti)", 0, 999, 0)
    bb_s, bb_n = st.number_input("Broadband (sec)", 0, 999, 180), st.number_input("Broadband (scatti)", 0, 999, 0)

# --- CALCOLI E RICERCA ---
# Recupero coordinate dal database SIMBAD
coordinate_target = ottieni_coordinate_simbad(soggetto)

# Calcolo tempi
totale = ((ha_s*ha_n)+(o3_s*o3_n)+(si2_s*si2_n)+(hb_s*hb_n)+(bb_s*bb_n)) / 3600
progresso = min(totale / target_ore, 1.0)

# --- LAYOUT FINALE ---
st.title(f"🔭 {soggetto.upper()}")
st.write(f"**Missione guidata da:** {autore}")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if img_file: 
        st.image(img_file, use_container_width=True)
    else: 
        st.info("Carica immagine target")
    st.subheader("Progresso Missione")
    st.progress(progresso)
    st.markdown(f"### {totale:.1f} / {target_ore:.1f} Ore")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("⚙️ Configurazione Setup")
    
    # Inserite le coordinate nel pannello di setup
    st.markdown(f"""
    **Ottica:** {ottica}  
    **Camera:** {camera}  
    **Montatura:** {montatura}  
    **Guida:** {guida}  
    **Filtri:** {filtri} 
    
    📡 **Posizione SIMBAD:** `{coordinate_target}`
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("") 
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Analisi Esposizioni")
    data = {"Filtro": ["Hα", "OIII", "SII", "Hβ", "Broadband"], 
            "Scatti": [ha_n, o3_n, si2_n, hb_n, bb_n],
            "Posa": [f"{ha_s}s", f"{o3_s}s", f"{si2_s}s", f"{hb_s}s", f"{bb_s}s"]}
    df = pd.DataFrame(data)
    # Mostra la tabella solo con i filtri che hanno scatti > 0
    df_filtrato = df[df["Scatti"] > 0]
    if not df_filtrato.empty:
        st.table(df_filtrato)
    else:
        st.info("Nessuno scatto ancora effettuato. Inserisci i dati nella barra laterale.")
    st.markdown('</div>', unsafe_allow_html=True)