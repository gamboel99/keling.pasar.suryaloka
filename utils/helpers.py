
import os
import pandas as pd
from PIL import Image
from datetime import datetime

DATA_PATH = "data/iklan.csv"
IMAGE_DIR = "images/"

def save_image(uploaded_file):
    os.makedirs(IMAGE_DIR, exist_ok=True)  # <-- tambahkan ini
    filename = datetime.now().strftime("%Y%m%d%H%M%S_") + uploaded_file.name.replace(" ", "_")
    filepath = os.path.join(IMAGE_DIR, filename)
    image = Image.open(uploaded_file)
    image.save(filepath)
    return filepath

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
    filename = datetime.now().strftime("%Y%m%d%H%M%S_") + uploaded_file.name.replace(" ", "_")
    filepath = os.path.join(IMAGE_DIR, filename)
    image = Image.open(uploaded_file)
    image.save(filepath)
    return filepath
