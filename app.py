import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Pasar Digital Desa Keling", layout="wide")

st.title("🛒 Pasar Digital Desa Keling")
st.markdown("Selamat datang di etalase UMKM & Iklan Produk Desa Keling!")

# === Load data toko ===
@st.cache_data
def load_data():
    file_path = "data/toko.csv"  # Pastikan file ini ada di folder /data/
    if not os.path.exists(file_path):
        st.warning("File data/toko.csv tidak ditemukan.")
        return pd.DataFrame(columns=['nama_toko', 'alamat', 'deskripsi', 'kontak'])
    df = pd.read_csv(file_path)
    return df.fillna("")

df = load_data()

# === Tampilkan setiap iklan/toko ===
for i, row in df.iterrows():
    st.markdown("---")
    cols = st.columns([4, 1])

    with cols[0]:
        st.subheader(row['nama_toko'])
        st.markdown(f"📍 {row['alamat']}")
        if row['deskripsi']:
            st.markdown(f"📝 {row['deskripsi']}")

    with cols[1]:
        kontak_raw = row.get('kontak', '')
        kontak_str = str(kontak_raw) if pd.notnull(kontak_raw) else ''
        kontak_wa = kontak_str.replace('+', '').replace(' ', '')

        if kontak_wa:
            wa_link = f"https://wa.me/{kontak_wa}"
            wa_button = f"""
            <a href="{wa_link}" target="_blank" style="text-decoration: none;">
                <button style="
                    background-color: #25D366;
                    color: white;
                    padding: 8px 12px;
                    border: none;
                    border-radius: 6px;
                    font-size: 16px;
                    cursor: pointer;
                ">
                    📱 WhatsApp
                </button>
            </a>
            """
            st.markdown(wa_button, unsafe_allow_html=True)
        else:
            st.markdown("📵 Kontak tidak tersedia")

st.markdown("---")
st.caption("Developed by CV. Mitra Utama Consultindo (MUC)")
