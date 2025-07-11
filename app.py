import streamlit as st
import pandas as pd
import os
from utils.helpers import load_iklan, save_iklan, save_image

st.set_page_config(page_title="Pasar Suryaloka Keling", layout="wide")
st.title("🛍️ Pasar Suryaloka Keling")
st.caption("Platform Iklan Produk & Jasa Warga Desa Keling")

tab1, tab2 = st.tabs(["📝 Posting Iklan", "🛒 Etalase Pasar"])

# ====== FORM POSTING IKLAN ======
with tab1:
    st.subheader("Form Posting Iklan Baru")
    with st.form("iklan_form", clear_on_submit=True):
        judul = st.text_input("Judul Iklan")
        deskripsi = st.text_area("Deskripsi")
        harga = st.number_input("Harga (Rp)", min_value=0, step=1000)
        kategori = st.selectbox("Kategori", ["Pertanian", "Peternakan", "Jasa", "Barang Bekas", "Lainnya"])
        kontak = st.text_input("Kontak (Nomor WA)")
        gambar = st.file_uploader("Upload Gambar", type=["jpg", "jpeg", "png"])
        submit = st.form_submit_button("✅ Posting")

        if submit and judul and gambar:
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

# ====== ETALASE IKLAN ======
with tab2:
    st.subheader("Etalase Iklan Terbaru")
    df = load_iklan()

    if df.empty:
        st.info("Belum ada iklan yang diposting.")
    else:
        for _, row in df[::-1].iterrows():
            with st.container():
                # Ambil semua data dengan aman
                judul = str(row["judul"]) if "judul" in row and pd.notna(row["judul"]) else "-"
                harga = str(row["harga"]) if "harga" in row and pd.notna(row["harga"]) else "-"
                kategori = str(row["kategori"]) if "kategori" in row and pd.notna(row["kategori"]) else "-"
                deskripsi = str(row["deskripsi"]) if "deskripsi" in row and pd.notna(row["deskripsi"]) else "-"
                waktu = str(row["waktu"]) if "waktu" in row and pd.notna(row["waktu"]) else "-"
                kontak = str(row["kontak"]) if "kontak" in row and pd.notna(row["kontak"]) else ""
                gambar = str(row["gambar"]) if "gambar" in row and pd.notna(row["gambar"]) else ""

                # Tampilkan gambar (jika ada)
                try:
                    if gambar:
                        st.image(gambar, use_container_width=True)
                except:
                    pass

                # Tampilkan informasi iklan
                st.markdown(f"### {judul}")
                st.markdown(f"**Harga:** {harga}")
                st.markdown(f"**Kategori:** {kategori}")
                st.markdown(deskripsi)

                # Tampilkan kontak WhatsApp (jika ada)
                if kontak:
                    nomor = kontak.replace("+", "").replace(" ", "")
                    st.markdown("**📞 Pemesanan:**")
                    st.markdown(
                        f"[![WhatsApp](https://img.icons8.com/color/24/000000/whatsapp.png)](https://wa.me/{nomor})"
                    )

                st.caption(f"🕒 {waktu}")
                st.markdown("---")
