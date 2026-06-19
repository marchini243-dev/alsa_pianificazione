import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# Configurazione Pagina
st.set_page_config(page_title="ALSA - Pianificatore", layout="wide")

st.title("🔭 ALSA - Pianificatore Astrofotografico")
st.sidebar.header("⚙️ Pannello di Controllo")

# --- INPUT NELLA BARRA LATERALE ---
soggetto = st.sidebar.text_input("Soggetto Target", "M31 - Andromeda")
target_ore = st.sidebar.number_input("Traguardo Ore", 1.0, 100.0, 40.0)

st.sidebar.subheader("🛠️ Attrezzatura")
montatura = st.sidebar.text_input("Montatura", "EQ8-R Pro")
ottica = st.sidebar.text_input("Ottica", "Newton 150/750")
camera = st.sidebar.text_input("Camera", "Toup 2600 MM")
guida = st.sidebar.text_input("Guida", "OAG-L")

st.sidebar.subheader("📸 Esposizioni (Secondi / Scatti)")
ha_s = st.sidebar.number_input("Hα (sec)", 0, 900, 300); ha_n = st.sidebar.number_input("Hα (scatti)", 0, 500, 0)
o3_s = st.sidebar.number_input("OIII (sec)", 0, 900, 300); o3_n = st.sidebar.number_input("OIII (scatti)", 0, 500, 0)
bb_s = st.sidebar.number_input("Broadband (sec)", 0, 900, 180); bb_n = st.sidebar.number_input("Broadband (scatti)", 0, 500, 120)

# Caricamento Immagine
img_file = st.sidebar.file_uploader("Carica Immagine Target", type=['png', 'jpg', 'jpeg'])

# --- LOGICA CALCOLI ---
ore_tot = ((ha_s*ha_n) + (o3_s*o3_n) + (bb_s*bb_n)) / 3600.0
progresso = min((ore_tot / target_ore) * 100, 100.0)

# --- GRAFICA ---
fig = plt.figure(figsize=(12, 8))
fig.patch.set_facecolor('#1a252f')
gs = fig.add_gridspec(2, 2, width_ratios=[1.2, 1], height_ratios=[1.3, 0.7])
ax_img, ax_prog, ax_info = fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[1, 0]), fig.add_subplot(gs[:, 1])

for ax in [ax_img, ax_prog, ax_info]:
    ax.set_facecolor('#1a252f'); ax.axis('off')

if img_file:
    ax_img.imshow(Image.open(img_file))
else:
    ax_img.text(0.5, 0.5, "Carica immagine\ndalla barra laterale", color='white', ha='center')

# Barra progresso
ax_prog.add_patch(plt.Rectangle((0, 0.45), 1, 0.2, facecolor='#34495e'))
ax_prog.add_patch(plt.Rectangle((0, 0.45), progresso/100, 0.2, facecolor='#00a8ff'))
ax_prog.text(0, 0.7, f"Fatto: {ore_tot:.1f}h", color='white', fontweight='bold')
ax_prog.text(1, 0.7, f"Target: {target_ore:.1f}h", color='#a0b0c0', ha='right')
ax_prog.text(0.5, 0.5, f"{progresso:.1f}%", color='white', ha='center', va='center', fontweight='bold')

# Info Hardware
y = 0.9
ax_info.text(0, y, "CONFIGURAZIONE", color='#00a8ff', fontweight='bold', fontsize=12); y-=0.1
for k, v in [("Ottica", ottica), ("Camera", camera), ("Montatura", montatura)]:
    ax_info.text(0, y, f"{k}: {v}", color='white'); y-=0.1

st.pyplot(fig)