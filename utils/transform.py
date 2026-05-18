import pandas as pd
import numpy as np

def clean_title_column(df):
    """
    Membersihkan kolom Title dari nilai invalid seperti 'Unknown Product'.
    """
    try:
        if "Title" in df.columns:
            # Mengubah string kosong menjadi NaN agar bisa didrop
            df["Title"] = df["Title"].replace(["Unknown Product", ""], np.nan)
        return df
    except Exception as e:
        print(f"Error in clean_title_column: {e}")
        return df

def clean_price_column(df):
    """
    Membersihkan kolom Price: menghilangkan simbol '$', mengubah ke float64,
    konversi dari USD ke IDR (dikalikan Rp16.000 per USD).
    """
    try:
        if "Price" in df.columns:
            # Buang baris yang bertuliskan 'Price Unavailable'
            df["Price"] = df["Price"].replace(["Price Unavailable", ""], np.nan)
            
            # Ekstrak angka menggunakan regex (misal dari '$100.00' menjadi '100.00')
            df["Price"] = df["Price"].astype(str).str.extract(r'([\d\.]+)')
            
            # Ubah ke float
            df["Price"] = pd.to_numeric(df["Price"], errors='coerce')
            
            # Konversi mata uang ke Rupiah dengan asumsi kurs Rp16.000 per USD
            df["Price"] = df["Price"] * 16000
        return df
    except Exception as e:
        print(f"Error in clean_price_column: {e}")
        return df

def clean_rating_column(df):
    """
    Membersihkan kolom Rating: mengambil nilai desimal (float64) 
    dan membuang teks pengotor serta status invalid seperti 'Invalid Rating'/'Not Rated'.
    """
    try:
        if "Rating" in df.columns:
            # Ganti teks status invalid dengan NaN
            df["Rating"] = df["Rating"].replace(["Invalid Rating", "Not Rated", ""], np.nan)
            
            # Ekstrak angka desimal (misal dari 'Rating: ⭐ 3.9 / 5' menjadi '3.9')
            df["Rating"] = df["Rating"].astype(str).str.extract(r'(\d+\.\d+|\d+)')
            
            # Ubah tipe data ke float64
            df["Rating"] = pd.to_numeric(df["Rating"], errors='coerce')
        return df
    except Exception as e:
        print(f"Error in clean_rating_column: {e}")
        return df

def clean_colors_column(df):
    """
    Membersihkan kolom Colors: menyisakan angka saja dan mengubah tipe data menjadi int64.
    """
    try:
        if "Colors" in df.columns:
            # Ekstrak angka saja (misal dari '3 Colors' menjadi '3')
            df["Colors"] = df["Colors"].astype(str).str.extract(r'(\d+)')
            
            # Isi NaN sementara dengan 0 atau drop (gunakan coerce lalu ubah ke int setelah dropna di fungsi main)
            df["Colors"] = pd.to_numeric(df["Colors"], errors='coerce')
        return df
    except Exception as e:
        print(f"Error in clean_colors_column: {e}")
        return df

def clean_categorical_columns(df):
    """
    Membersihkan kolom Size dan Gender dari teks bawaan (Prefix).
    """
    try:
        # Bersihkan kolom Size (misal dari 'Size: M' menjadi 'M')
        if "Size" in df.columns:
            df["Size"] = df["Size"].astype(str).str.replace("Size: ", "", case=False, regex=False).str.strip()
            df["Size"] = df["Size"].replace(["None", "nan", ""], np.nan)
            
        # Bersihkan kolom Gender (misal dari 'Gender: Men' menjadi 'Men')
        if "Gender" in df.columns:
            df["Gender"] = df["Gender"].astype(str).str.replace("Gender: ", "", case=False, regex=False).str.strip()
            df["Gender"] = df["Gender"].replace(["None", "nan", ""], np.nan)
            
        return df
    except Exception as e:
        print(f"Error in clean_categorical_columns: {e}")
        return df

def transform_main(df_raw):
    """
    Fungsi utama tahapan Transform yang menggabungkan seluruh fungsi pembersihan,
    menghapus nilai null, membuang duplikasi, dan memastikan tipe data akhir sesuai ekspektasi.
    """
    try:
        if df_raw.empty:
            print("Warning: Input DataFrame to Transform is empty.")
            return df_raw
            
        # Melakukan salinan DataFrame agar tidak merubah data asli
        df_cleaned = df_raw.copy()
        
        # Jalankan urutan fungsi pembersihan modular
        df_cleaned = clean_title_column(df_cleaned)
        df_cleaned = clean_price_column(df_cleaned)
        df_cleaned = clean_rating_column(df_cleaned)
        df_cleaned = clean_colors_column(df_cleaned)
        df_cleaned = clean_categorical_columns(df_cleaned)
        
        # 1. Hapus baris yang mengandung nilai Null/NaN di kolom mana pun akibat data invalid
        df_cleaned = df_cleaned.dropna()
        
        # 2. Hapus data yang terduplikasi (Kriteria Basic - 2 Pts)
        df_cleaned = df_cleaned.drop_duplicates()
        
        # 3. Memastikan tipe data akhir mutlak sesuai dengan skema penafsiran Dicoding
        df_cleaned["Price"] = df_cleaned["Price"].astype("float64")
        df_cleaned["Rating"] = df_cleaned["Rating"].astype("float64")
        df_cleaned["Colors"] = df_cleaned["Colors"].astype("int64")
        df_cleaned["Title"] = df_cleaned["Title"].astype("object")
        df_cleaned["Size"] = df_cleaned["Size"].astype("object")
        df_cleaned["Gender"] = df_cleaned["Gender"].astype("object")
        
        # Mengatur susunan kolom agar rapi kembali
        columns_order = ["Title", "Price", "Rating", "Colors", "Size", "Gender", "Timestamp"]
        df_cleaned = df_cleaned[columns_order]
        
        return df_cleaned
        
    except Exception as e:
        print(f"An error occurred in transform_main: {e}")
        return pd.DataFrame()