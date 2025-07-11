import os
import pandas as pd
from PIL import Image
import uuid

DATA_PATH = "data/iklan.csv"
IMG_DIR = "data/gambar"
os.makedirs(IMG_DIR, exist_ok=True)

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
