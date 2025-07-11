import streamlit as st
import pandas as pd
import os
from PIL import Image

DATA_FILE = "data/iklan.csv"
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.set_page_config(page_title="Pasar Suryaloka Keling", layout="wide")

st.markdown("<h1>🛒 Pasar Suryaloka Keling</h1>", unsafe_allow_html=True)
st.caption("Platform Iklan Produk & Jasa Warga Desa Keling")

menu = st.sidebar.radio("📌 Navigasi", ["📤 Posting Iklan", "🛍️ Etalase Pasar"])

# ----------------------------
# Fungsi bantu
# ----------------------------
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["judul", "deskripsi", "harga", "kategori", "kontak", "gambar"])

def save_data(data):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# ----------------------------
# Posting Iklan
# ----------------------------
if menu == "📤 Posting Iklan":
    st.subheader("Form Posting Iklan Baru")

    with st.form("form_iklan"):
        judul = st.text_input("Judul Iklan")
        deskripsi = st.text_area("Deskripsi")
        harga = st.number_input("Harga (Rp)", min_value=0)
        kategori = st.selectbox("Kategori", ["Pertanian", "Peternakan", "Perikanan", "Kuliner", "Jasa", "Lainnya"])
        kontak = st.text_input("Kontak (Nomor WA)")
        gambar = st.file_uploader("Upload Gambar", type=["jpg", "jpeg", "png"])

        submitted = st.form_submit_button("✅ Simpan Iklan")

        if submitted:
            if judul and deskripsi and kontak:
                # Simpan gambar
                filename = ""
                if gambar:
                    filename = os.path.join(UPLOAD_DIR, gambar.name)
                    with open(filename, "wb") as f:
                        f.write(gambar.read())

                save_data({
                    "judul": judul,
                    "deskripsi": deskripsi,
                    "harga": harga,
                    "kategori": kategori,
                    "kontak": kontak,
                    "gambar": filename
                })
                st.success("Iklan berhasil diposting!")
            else:
                st.warning("Silakan lengkapi semua field yang diperlukan!")

# ----------------------------
# Etalase Pasar
# ----------------------------
if menu == "🛍️ Etalase Pasar":
    st.subheader("Etalase Pasar Warga Desa")

    df = load_data()

    if df.empty:
        st.info("Belum ada iklan ditambahkan.")
    else:
        for i, row in df.iterrows():
            with st.container():
                cols = st.columns([1, 2])
                if row["gambar"] and os.path.exists(str(row["gambar"])):
                    cols[0].image(row["gambar"], use_container_width=True)
                else:
                    cols[0].markdown("*[Gambar tidak tersedia]*")

                # Info Iklan
                with cols[1]:
                    st.markdown(f"### {row['judul']}")
                    st.markdown(f"**Kategori:** {row['kategori']}")
                    st.markdown(f"**Harga:** Rp {int(row['harga']):,}")
                    st.markdown(f"**Deskripsi:** {row['deskripsi']}")
                    nomor = str(row['kontak']).replace("+", "").replace(" ", "")
                    st.markdown(f"[📱 Pemesanan via WhatsApp](https://wa.me/{nomor})")
                st.markdown("---")
