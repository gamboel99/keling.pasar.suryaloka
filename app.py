import streamlit as st
import pandas as pd
import os
from PIL import Image

st.set_page_config(page_title="Pasar Suryaloka Keling", layout="wide")
st.title("🛒 Pasar Suryaloka Keling")
st.caption("Platform Iklan Produk & Jasa Warga Desa Keling")

menu = st.tabs(["📢 Posting Iklan", "🛍️ Etalase Pasar"])

DATA_FILE = "data/iklan.csv"
IMAGE_DIR = "gambar"

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["judul", "deskripsi", "harga", "kategori", "kontak", "gambar"])

def save_data(data):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

with menu[0]:
    st.subheader("Form Posting Iklan Baru")
    with st.form("form_iklan"):
        judul = st.text_input("Judul Iklan")
        deskripsi = st.text_area("Deskripsi")
        harga = st.number_input("Harga (Rp)", min_value=0)
        kategori = st.selectbox("Kategori", ["Pertanian", "Peternakan", "UMKM", "Jasa", "Lainnya"])
        kontak = st.text_input("Kontak (Nomor WA)")
        gambar = st.file_uploader("Upload Gambar", type=["jpg", "png", "jpeg"])
        submitted = st.form_submit_button("💾 Simpan Iklan")

        if submitted:
            filename = ""
            if gambar:
                filename = os.path.join(IMAGE_DIR, gambar.name)
                with open(filename, "wb") as f:
                    f.write(gambar.getbuffer())
            save_data({
                "judul": judul,
                "deskripsi": deskripsi,
                "harga": harga,
                "kategori": kategori,
                "kontak": kontak,
                "gambar": filename
            })
            st.success("Iklan berhasil disimpan!")

with menu[1]:
    st.subheader("Etalase Pasar Desa")
    df = load_data()
    if df.empty:
        st.info("Belum ada iklan yang ditampilkan.")
    else:
        for _, row in df.iterrows():
            with st.container():
                cols = st.columns([1, 2])
                if os.path.exists(row["gambar"]):
                    cols[0].image(row["gambar"], use_container_width=True)
                else:
                    cols[0].markdown("*Tidak ada gambar*")

                cols[1].markdown(f"### {row['judul']}")
                cols[1].markdown(f"**Rp {int(row['harga']):,}**")
                cols[1].markdown(f"**Kategori:** {row['kategori']}")
                cols[1].markdown(row['deskripsi'])
                if row['kontak']:
                    kontak_clean = str(row['kontak']).replace("+", "").replace(" ", "")
                    wa_link = f"https://wa.me/{kontak_clean}"
                    cols[1].markdown(f"[📱 Hubungi via WhatsApp]({wa_link})")
