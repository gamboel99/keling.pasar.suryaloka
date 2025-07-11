import streamlit as st
import pandas as pd
import os
from utils.helpers import load_iklan, save_iklan, save_image

st.set_page_config(page_title="Pasar Suryaloka Keling", layout="wide")
st.title("🛍️ Pasar Suryaloka Keling")
st.caption("Platform Iklan Produk & Jasa Warga Desa Keling")

tab1, tab2 = st.tabs(["📝 Posting Iklan", "🛒 Etalase Pasar"])

# Form posting iklan
with tab1:
    st.subheader("Form Posting Iklan Baru")
    with st.form("iklan_form", clear_on_submit=True):
        judul = st.text_input("Judul Iklan")
        deskripsi = st.text_area("Deskripsi")
        harga = st.number_input("Harga (Rp)", min_value=0, step=1000)
        kategori = st.selectbox("Kategori", ["Pertanian", "Peternakan", "Jasa", "Barang Bekas", "Lainnya"])
        kontak = st.text_input("Kontak (Nomor WA)")
        gambar = st.file_uploader("Upload Gambar", type=["jpg", "png", "jpeg"])
        submitted = st.form_submit_button("✅ Posting")

        if submitted and judul and gambar:
            image_path = save_image(gambar)
            iklan = {
                "judul": judul,
                "deskripsi": deskripsi,
                "harga": f"Rp {harga:,.0f}".replace(",", "."),
                "kategori": kategori,
                "kontak": kontak,
                "gambar": image_path,
                "waktu": pd.Timestamp.now()
            }
            save_iklan(iklan)
            st.success("✅ Iklan berhasil diposting!")

# Tampilkan etalase
with tab2:
    st.subheader("Etalase Iklan Terbaru")
    df = load_iklan()
    if df.empty:
        st.info("Belum ada iklan yang diposting.")
    else:
        for _, row in df[::-1].iterrows():
            with st.container():
    # Gambar (jika ada)
    try:
        gambar = str(row["gambar"]).strip() if pd.notna(row["gambar"]) else ""
        if gambar and os.path.isfile(gambar):
            st.image(gambar, use_container_width=True)
    except:
        pass  # gambar error, diamkan saja

    # Informasi iklan
    judul = str(row["judul"]).strip() if pd.notna(row["judul"]) else "-"
    harga = str(row["harga"]).strip() if pd.notna(row["harga"]) else "-"
    kategori = str(row["kategori"]).strip() if pd.notna(row["kategori"]) else "-"
    deskripsi = str(row["deskripsi"]).strip() if pd.notna(row["deskripsi"]) else "-"
    waktu = str(row["waktu"]).strip() if pd.notna(row["waktu"]) else "-"

    st.markdown(f"### {judul}")
    st.markdown(f"**Harga:** {harga}")
    st.markdown(f"**Kategori:** {kategori}")
    st.markdown(deskripsi)

    kontak = str(row["kontak"]).strip() if pd.notna(row["kontak"]) else ""
    if kontak:
        nomor = kontak.replace("+", "").replace(" ", "")
        st.markdown("**📞 Pemesanan:**")
        st.markdown(
            f"[![WhatsApp](https://img.icons8.com/color/24/000000/whatsapp.png)](https://wa.me/{nomor})"
        )

    st.caption(f"🕒 {waktu}")
    st.markdown("---")
    
