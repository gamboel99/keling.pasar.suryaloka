import streamlit as st
import pandas as pd
import os
from PIL import Image

st.set_page_config(page_title="Pasar Suryaloka Keling", layout="wide")

st.title("🛒 Pasar Suryaloka Keling")
st.caption("Etalase Iklan Produk & Jasa Warga Desa Keling")

DATA_FILE = "data/iklan.csv"
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs("data", exist_ok=True)

# Fungsi bantu
def load_data():
    try:
        return pd.read_csv(DATA_FILE)
    except:
        return pd.DataFrame(columns=["judul", "deskripsi", "harga", "kategori", "kontak", "gambar"])

def save_data(entry):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# Menu
menu = st.sidebar.radio("Navigasi", ["📝 Posting Iklan", "🛍️ Etalase Pasar"])

if menu == "📝 Posting Iklan":
    st.subheader("Form Iklan Baru")

    with st.form("form_iklan"):
        judul = st.text_input("Judul Iklan")
        deskripsi = st.text_area("Deskripsi")
        harga = st.number_input("Harga (Rp)", min_value=0)
        kategori = st.selectbox("Kategori", ["Pertanian", "Peternakan", "UMKM", "Jasa", "Lainnya"])
        kontak = st.text_input("Kontak WhatsApp")
        gambar = st.file_uploader("Upload Gambar", type=["jpg", "jpeg", "png"])
        submit = st.form_submit_button("Simpan")

    if submit:
        img_path = ""
        if gambar:
            img_path = os.path.join(UPLOAD_DIR, gambar.name)
            with open(img_path, "wb") as f:
                f.write(gambar.getbuffer())

        save_data({
            "judul": judul,
            "deskripsi": deskripsi,
            "harga": harga,
            "kategori": kategori,
            "kontak": kontak,
            "gambar": img_path
        })
        st.success("Iklan berhasil disimpan!")

if menu == "🛍️ Etalase Pasar":
    st.subheader("Etalase Iklan")
    df = load_data()
    if df.empty:
        st.info("Belum ada iklan.")
    else:
        for i, row in df.iterrows():
            with st.container():
                col1, col2 = st.columns([1, 2])
                if isinstance(row.get("gambar"), str) and os.path.exists(row["gambar"]):
                    col1.image(row["gambar"], use_container_width=True)
                else:
                    col1.markdown("*Tidak ada gambar*")

                col2.markdown(f"### {row.get('judul', '-')}")
                col2.markdown(f"**Rp {int(row.get('harga', 0)):,}**")
                col2.markdown(f"Kategori: {row.get('kategori', '-')}")
                col2.markdown(row.get("deskripsi", "-"))
                kontak = str(row.get("kontak", "")).replace("+", "").replace(" ", "")
                if kontak:
                    col2.markdown(f"[📱 Pesan via WhatsApp](https://wa.me/{kontak})")
