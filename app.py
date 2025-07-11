import streamlit as st
import pandas as pd
import os
from PIL import Image
import uuid

# Konfigurasi dasar
st.set_page_config(page_title="Pasar Suryaloka Keling", layout="wide")
st.title("🛍️ Pasar Suryaloka Keling")
st.caption("Marketplace Digital Warga Desa Keling")

# Path data & gambar
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

# Tab
tab1, tab2 = st.tabs(["📦 Etalase Produk", "➕ Tambah Iklan"])

# =====================
# TAB 1: ETALASE IKLAN
# =====================
with tab1:
    df = load_iklan()
    st.subheader("Etalase Produk")
    if df.empty:
        st.info("Belum ada produk yang diposting.")
    else:
        cols = st.columns(2)
        for i, (_, row) in enumerate(df[::-1].iterrows()):
            with cols[i % 2]:
                st.markdown("----")
                gambar = row["gambar"] if "gambar" in df.columns and pd.notna(row["gambar"]) else ""
                judul = row["judul"] if "judul" in df.columns and pd.notna(row["judul"]) else "-"
                harga = row["harga"] if "harga" in df.columns and pd.notna(row["harga"]) else "-"
                kategori = row["kategori"] if "kategori" in df.columns and pd.notna(row["kategori"]) else "-"
                deskripsi = row["deskripsi"] if "deskripsi" in df.columns and pd.notna(row["deskripsi"]) else "-"
                kontak = row["kontak"] if "kontak" in df.columns and pd.notna(row["kontak"]) else ""

                # Gambar
                try:
                    if gambar and os.path.exists(gambar):
                        st.image(gambar, use_container_width=True)
                except:
                    st.warning("📷 Gambar tidak ditemukan.")

                st.markdown(f"### {judul}")
                st.markdown(f"💰 **{harga}**  |  🏷️ *{kategori}*")
                st.markdown(deskripsi)

                if kontak:
                    nomor = kontak.replace("+", "").replace(" ", "")
                    st.markdown(
                        f"[📲 Hubungi via WhatsApp](https://wa.me/{nomor})"
                    )

# =====================
# TAB 2: FORM IKLAN
# =====================
with tab2:
    st.subheader("Tambah Iklan Baru")
    with st.form("form_iklan", clear_on_submit=True):
        judul = st.text_input("Nama Produk")
        deskripsi = st.text_area("Deskripsi Produk")
        harga = st.text_input("Harga (contoh: Rp 10.000)")
        kategori = st.selectbox("Kategori", ["Pertanian", "Peternakan", "Kuliner", "Jasa", "Barang Bekas", "Lainnya"])
        kontak = st.text_input("Nomor WhatsApp (misal: 6281234567890)")
        gambar = st.file_uploader("Upload Gambar Produk", type=["jpg", "jpeg", "png"])
        submit = st.form_submit_button("✅ Posting Iklan")

        if submit:
            if not (judul and harga and kontak and gambar):
                st.warning("Harap lengkapi semua kolom wajib.")
            else:
                filepath = save_image(gambar)
                iklan = {
                    "judul": judul,
                    "deskripsi": deskripsi,
                    "harga": harga,
                    "kategori": kategori,
                    "kontak": kontak,
                    "gambar": filepath,
                    "waktu": pd.Timestamp.now()
                }
                save_iklan(iklan)
                st.success("✅ Iklan berhasil diposting.")
