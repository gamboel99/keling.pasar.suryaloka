import streamlit as st
import pandas as pd
import os
from PIL import Image
import uuid

st.set_page_config(page_title="Toko Online Keling", layout="wide")

DATA_PATH = "data/iklan.csv"
IMG_DIR = "data/gambar"
os.makedirs(IMG_DIR, exist_ok=True)

def load_data():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    else:
        return pd.DataFrame(columns=["judul", "deskripsi", "harga", "kategori", "kontak", "gambar", "waktu"])

def save_data(entry):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    df.to_csv(DATA_PATH, index=False)

def save_image(uploaded_file):
    ext = uploaded_file.name.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join(IMG_DIR, filename)
    Image.open(uploaded_file).save(filepath)
    return filepath

st.markdown("""
<div style="background-color:#f63d30; padding:20px; border-radius:5px;">
    <h1 style="color:white; text-align:center;">🛍️ Toko Online Keling</h1>
    <p style="color:white; text-align:center;">Menjual Produk UMKM Warga Desa Keling - Amanah dan Terpercaya</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🛍️ Etalase Produk", "➕ Tambah Produk"])

with tab1:
    df = load_data()
    st.markdown("## 📦 Etalase Produk")
    if df.empty:
        st.info("Belum ada produk yang ditambahkan.")
    else:
        cols = st.columns(3)
        for i, (_, row) in enumerate(df[::-1].iterrows()):
            with cols[i % 3]:
                try:
                    st.markdown("----")
                    img = row["gambar"] if pd.notna(row["gambar"]) else ""
                    judul = row["judul"] if pd.notna(row["judul"]) else "-"
                    harga = row["harga"] if pd.notna(row["harga"]) else "-"
                    kontak = row["kontak"] if pd.notna(row["kontak"]) else ""
                    no_wa = kontak.replace("+", "").replace(" ", "")
                    deskripsi = row["deskripsi"] if pd.notna(row["deskripsi"]) else ""

                    if img and os.path.exists(img):
                        st.image(img, use_container_width=True)
                    st.markdown(f"### {judul}")
                    st.markdown(f"💰 **{harga}**")
                    st.markdown(f"<small>{deskripsi}</small>", unsafe_allow_html=True)
                    if no_wa:
                        st.markdown(
                            f"""
                            <a href="https://wa.me/{no_wa}" target="_blank">
                            <button style="background-color:#25D366; color:white; padding:5px 10px; border:none; border-radius:5px; cursor:pointer;">
                            Chat via WhatsApp
                            </button></a>
                            """,
                            unsafe_allow_html=True,
                        )
                except:
                    st.warning("⚠️ Error menampilkan produk")

with tab2:
    st.markdown("## ➕ Tambah Produk Baru")
    with st.form("form_produk", clear_on_submit=True):
        judul = st.text_input("Nama Produk")
        deskripsi = st.text_area("Deskripsi Produk")
        harga = st.text_input("Harga (cth: Rp 15.000)")
        kategori = st.selectbox("Kategori", ["Pakaian", "Kuliner", "Pertanian", "Jasa", "Lainnya"])
        kontak = st.text_input("Nomor WhatsApp (cth: 6281234567890)")
        gambar = st.file_uploader("Upload Gambar", type=["jpg", "jpeg", "png"])
        kirim = st.form_submit_button("✅ Posting Produk")

        if kirim:
            if not (judul and harga and kontak and gambar):
                st.warning("Harap lengkapi semua kolom.")
            else:
                img_path = save_image(gambar)
                new_data = {
                    "judul": judul,
                    "deskripsi": deskripsi,
                    "harga": harga,
                    "kategori": kategori,
                    "kontak": kontak,
                    "gambar": img_path,
                    "waktu": pd.Timestamp.now()
                }
                save_data(new_data)
                st.success("✅ Produk berhasil ditambahkan!")
