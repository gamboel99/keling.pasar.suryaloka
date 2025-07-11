import os
import pandas as pd
from PIL import Image

DATA_FILE = "data/iklan.csv"
IMAGE_DIR = "data/uploads"
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs("data", exist_ok=True)

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            return pd.read_csv(DATA_FILE)
        except Exception:
            return pd.DataFrame(columns=["judul", "deskripsi", "harga", "kategori", "kontak", "gambar"])
    else:
        return pd.DataFrame(columns=["judul", "deskripsi", "harga", "kategori", "kontak", "gambar"])

def save_data(data):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

def save_image(uploaded_file):
    """Simpan gambar yang diunggah ke folder uploads/"""
    if uploaded_file is not None:
        filepath = os.path.join(IMAGE_DIR, uploaded_file.name)
        image = Image.open(uploaded_file)
        image.save(filepath)
        return filepath
    return ""
