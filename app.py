import streamlit as st
import pandas as pd
import os
from PIL import Image
import uuid

# Konfigurasi dasar
st.set_page_config(page_title="Pasar Suryaloka Keling", layout="wide")
st.markdown("<h1 style='text-align:center;'>🛒 Pasar Suryaloka Keling</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Marketplace Warga Desa Keling • Seperti Shopee/Tokopedia</p>", unsafe_allow_html=True)

# Path data
DATA_PATH = "data/iklan.csv"
IMG_DIR = "data/gambar"
os.makedirs(IMG_DIR, exist_ok=True)

# Fungsi bantu
def load_iklan():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    else:
        return pd.DataFrame(columns=["judul", "deskripsi", "harga", "kategori", "kontak", "gambar", "waktu"])

def save_iklan(data):
    df = load_iklan()
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_csv(DATA_PATH, index=False)

def save_image(uploaded_file):
    ext = uploaded_file.name.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join(IMG_DIR, filename)
    image = Image.open(uploaded_file)
    image.save(filepath)
    return filepath

# Tab navigasi
tab1, tab2 = st.tabs(["🛍️ Etalase Produk", "➕ Tambah Iklan"])

# =============== TAMPILKAN ETALASE PRODUK ================
with tab1:
    df = load_iklan()
    if df.empty:
        st.warning("Belum ada iklan yang diposting.")
    else:
        st.markdown("### Produk Terbaru")
        col_count = 3
        cols = st.columns(col_count)
        for idx, (_, row) in enumerate(df[::-1].iterrows()):
            with cols[idx % col_count]:
                try:
                    gambar = row["gambar"] if "gambar" in df.columns and pd.notna(row["gambar"]) else ""
                    judul = row["judul"] if "judul" in df.columns and pd.notna(row["judul"]) else "-"
                    harga = row["harga"] if "harga" in df.columns and pd.notna(row["harga"]) else "-"
                    kontak = row["kontak"] if "kontak" in df.columns and pd.notna(row["kontak"]) else ""
                    nomor = kontak.replace("+", "").replace(" ", "")
                    # Kartu Produk
                    st.markdown(
                        f"""
                        <div style="border:1px solid #ccc; border-radius:10px; padding:10px; margin-bottom:15px">
                            <img src="file://{gambar}" style="width:100%; height:200px; object-fit:cover; border-radius:8px;">
                            <h4>{judul}</h4>
                            <p style="color:green;"><b>{harga}</b></p>
                            <a href="https://wa.me/{nomor}" target="_blank">
                                <button style="background-color:#25D366;color:white;border:none;padding:8px 12px;border-radius:5px;cursor:pointer;">
                                    Chat via WhatsApp
                                </button>
                            </a>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                except Exception as e:
                    st.error(f"❌ Error tampilkan produk: {e}")

# =============== FORM INPUT IKLAN ================
with tab2:
    st.markdown("### Tambah Iklan Baru")
    with st.form("iklan_form", clear_on_submit=True):
        judul = st.text_input("Nama Produk")
        deskripsi = st.text_area("Deskripsi")
        harga = st.text_input("Harga (misal: Rp 10.000)")
        kategori = st.selectbox("Kategori", ["Pertanian", "Peternakan", "Kuliner", "Jasa", "Barang Bekas", "Lainnya"])
        kontak = st.text_input("Nomor WhatsApp (cth: 6281234567890)")
        gambar = st.file_uploader("Gambar Produk", type=["jpg", "jpeg", "png"])
        submit = st.form_submit_button("✅ Posting")

        if submit:
            if not (judul and harga and kontak and gambar):
                st.warning("Mohon lengkapi semua kolom.")
            else:
                image_path = save_image(gambar)
                iklan = {
                    "judul": judul,
                    "deskripsi": deskripsi,
                    "harga": harga,
                    "kategori": kategori,
                    "kontak": kontak,
                    "gambar": image_path,
                    "waktu": pd.Timestamp.now()
                }
                save_iklan(iklan)
                st.success("✅ Iklan berhasil diposting!")
