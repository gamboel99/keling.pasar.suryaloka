import os
import pandas as pd
from PIL import Image, UnidentifiedImageError
from datetime import datetime

DATA_PATH = "data/iklan.csv"

def load_iklan():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    else:
        return pd.DataFrame(columns=["judul", "deskripsi", "harga", "kategori", "kontak", "gambar", "waktu"])

def save_iklan(data):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    df = load_iklan()
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_csv(DATA_PATH, index=False)

def save_image(uploaded_file):
    try:
        filename = datetime.now().strftime("uploaded_%Y%m%d%H%M%S_") + uploaded_file.name.replace(" ", "_")
        filepath = filename  # Simpan langsung di root folder
        image = Image.open(uploaded_file)
        image.save(filepath)
        return filepath
    except UnidentifiedImageError:
        return None
