import streamlit as st
import pandas as pd
import os
from utils.helpers import load_iklan, save_iklan, save_image

st.set_page_config(page_title="Pasar Suryaloka Keling", layout="wide")

st.title("🛍️ Pasar Suryaloka Keling")
st.caption("Platform Iklan Produk & Jasa Warga Desa Keling")

tab1, tab2 = st.tabs(["📝 Posting Iklan", "🛒 Etalase Pasar"])

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

with tab2:
    st.subheader("Etalase Iklan Terbaru")
    try:
        df = load_iklan()
    except:
        st.warning("⚠️ Gagal memuat data iklan.")
        df = pd.DataFrame()

    if df.empty:
        st.info("Belum ada iklan yang diposting.")
    else:
        for _, row in df[::-1].iterrows():
            with st.container():
                cols = st.columns([1, 3])

                # Gambar
                try:
                    if os.path.exists(str(row["gambar"])):
                        cols[0].image(str(row["gambar"]), use_container_width=True)
                except:
                    pass

                # Info
                def safe(val):
                    try:
                        return str(val).strip() if pd.notna(val) else "-"
                    except:
                        return "-"

                judul = safe(row.get("judul"))
                harga = safe(row.get("harga"))
                kategori = safe(row.get("kategori"))
                deskripsi = safe(row.get("deskripsi"))
                waktu = safe(row.get("waktu"))

                cols[1].markdown(f"### {judul}")
                cols[1].markdown(f"**Harga:** {harga}")
                cols[1].markdown(f"**Kategori:** {kategori}")
                cols[1].markdown(deskripsi)

                # Kontak
                try:
                    kontak = safe(row.get("kontak"))
                    if kontak and kontak.lower() != "nan":
                        nomor = kontak.replace("+", "").replace(" ", "")
                        cols[1].markdown("**📞 Pemesanan:**")
                        cols[1].markdown(
                            f"[![WhatsApp](https://img.icons8.com/color/24/000000/whatsapp.png)](https://wa.me/{nomor})"
                        )
                except:
                    pass

                cols[1].caption(f"🕒 {waktu}")
                st.markdown("---")
