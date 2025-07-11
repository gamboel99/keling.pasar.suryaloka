import streamlit as st
import pandas as pd
import os
from PIL import Image

# Pengaturan Awal
st.set_page_config(page_title="Pasar Suryaloka Keling", layout="wide")
st.title("🛒 Pasar Suryaloka Keling")
st.caption("Platform Iklan Produk & Jasa Warga Desa Keling")

# File & Folder
DATA_FILE = "data/iklan.csv"
IMAGE_DIR = "gambar"
os.makedirs("data", exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)

# Fungsi Utama
def load_data():
    try:
        return pd.read_csv(DATA_FILE)
    except:
        return pd.DataFrame(columns=["judul", "deskripsi", "harga", "kategori", "kontak", "gambar"])

def save_data(entry):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# Tab Menu
menu = st.tabs(["📢 Posting Iklan", "🛍️ Etalase Pasar"])

# -------------------------------
# Tab 1: Posting Iklan
# -------------------------------
with menu[0]:
    st.subheader("Form Posting Iklan Baru")
    with st.form("form_iklan"):
        judul = st.text_input("Judul Iklan")
        deskripsi = st.text_area("Deskripsi")
        harga = st.number_input("Harga (Rp)", min_value=0)
        kategori = st.selectbox("Kategori", ["Pertanian", "Peternakan", "UMKM", "Jasa", "Lainnya"])
        kontak = st.text_input("Kontak (Nomor WA)")
        gambar = st.file_uploader("Upload Gambar", type=["jpg", "jpeg", "png"])

        submitted = st.form_submit_button("💾 Simpan Iklan")
        if submitted:
            # Simpan gambar
            img_path = ""
            if gambar is not None:
                img_path = os.path.join(IMAGE_DIR, gambar.name)
                with open(img_path, "wb") as f:
                    f.write(gambar.getbuffer())

            # Simpan data
            save_data({
                "judul": judul,
                "deskripsi": deskripsi,
                "harga": harga,
                "kategori": kategori,
                "kontak": kontak,
                "gambar": img_path
            })
            st.success("✅ Iklan berhasil disimpan!")

# -------------------------------
# Tab 2: Etalase Pasar
# -------------------------------
with menu[1]:
    st.subheader("Etalase Pasar Warga Desa")

    df = load_data()
    if df.empty:
        st.info("Belum ada iklan yang diposting.")
    else:
        for idx, row in df.iterrows():
            with st.container():
                cols = st.columns([1, 2])
                # Gambar
                if isinstance(row["gambar"], str) and os.path.exists(row["gambar"]):
                    cols[0].image(row["gambar"], use_container_width=True)
                else:
                    cols[0].markdown("*[Tidak ada gambar]*")

                # Info Iklan
                judul = str(row.get("judul", "-"))
                harga = int(float(row.get("harga", 0)))
                deskripsi = str(row.get("deskripsi", "-"))
                kategori = str(row.get("kategori", "-"))
                kontak = str(row.get("kontak", "")).replace("+", "").replace(" ", "")
                wa_link = f"https://wa.me/{kontak}" if kontak else "#"

                cols[1].markdown(f"### {judul}")
                cols[1].markdown(f"**Rp {harga:,.0f}**")
                cols[1].markdown(f"**Kategori:** {kategori}")
                cols[1].markdown(f"{deskripsi}")
                if kontak:
                    cols[1].markdown(f"[📱 Hubungi via WhatsApp]({wa_link})")
