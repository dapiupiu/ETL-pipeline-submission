import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def fetching_content(url, session=None):
    """
    Fungsi untuk mengambil konten HTML mentah dari URL tertentu.
    Dibungkus terpisah agar mudah dilakukan Mock Testing.
    """
    if session is None:
        session = requests.Session()
        
    try:
        response = session.get(url, timeout=10)
        # Melempar HTTPError jika status code bukan 2xx
        response.raise_for_status() 
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching website: {e}")
        return None
    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        return None

def scrape_main(base_url, start_page=1, end_page=50):
    """
    Fungsi utama untuk melakukan iterasi dari halaman 1 sampai 50,
    mengekstrak data mentah, dan menambahkan kolom timestamp.
    """
    products = []
    session = requests.Session()
    
    try:
        for page in range(start_page, end_page + 1):
            # Membentuk URL per halaman, misalnya: https://fashion-studio.dicoding.dev/?page=1
            url = f"{base_url}?page={page}" if "?" not in base_url else f"{base_url}&page={page}"
            
            html_content = fetching_content(url, session)
            if html_content is None:
                print(f"Skipping page {page} due to connection error.")
                continue
                
            soup = BeautifulSoup(html_content, "html.parser")
            
            # Mencari semua kartu produk berdasarkan struktur HTML website
            cards = soup.find_all(class_="collection-card")
            
            # Jika halaman kosong atau tidak ditemukan kartu produk, hentikan loop
            if not cards:
                break
                
            for card in cards:
                # Mengambil Title
                title_tag = card.find("h3", class_="product-title")
                title = title_tag.get_text(strip=True) if title_tag else None
                
                # Mengambil Price (Mengantisipasi dua variasi tag HTML dari hasil analisis gambar)
                price = None
                # Pola 1: Berada di price-container -> span price
                price_container = card.find(class_="price-container")
                if price_container:
                    price_tag = price_container.find("span", class_="price")
                    if price_tag:
                        price = price_tag.get_text(strip=True)
                
                # Jika pola 1 tidak ketemu, cari tag p dengan class price ("Price Unavailable")
                if not price:
                    price_tag = card.find("p", class_="price")
                    if price_tag:
                        price = price_tag.get_text(strip=True)
                
                # Mencari informasi tambahan di dalam tag p biasa
                rating, colors, size, gender = None, None, None, None
                p_tags = card.find_all("p")
                
                for p in p_tags:
                    text = p.get_text(strip=True)
                    if "Rating:" in text:
                        rating = text
                    elif "Colors" in text:
                        colors = text
                    elif "Size:" in text:
                        size = text
                    elif "Gender:" in text:
                        gender = text
                
                # Mencatat waktu pengambilan data
                timestamp = datetime.now().isoformat()
                
                # Memasukkan data mentah apa adanya ke dalam list (pembersihan dilakukan di tahap Transform)
                products.append({
                    "Title": title,
                    "Price": price,
                    "Rating": rating,
                    "Colors": colors,
                    "Size": size,
                    "Gender": gender,
                    "Timestamp": timestamp
                })
                
        # Mengubah hasil akhir menjadi DataFrame Pandas
        df_raw = pd.DataFrame(products)
        return df_raw
        
    except Exception as e:
        print(f"An error occurred in scrape_main: {e}")
        return pd.DataFrame()