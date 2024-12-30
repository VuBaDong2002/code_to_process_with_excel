import os
from PIL import Image
import requests
import pandas as pd
from io import BytesIO
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

path_excel_input = r"C:\Users\dongk\Downloads\cate_dau_goi_xa_1208.xlsx"
df_raw = pd.read_excel(path_excel_input, sheet_name="Sheet1")

list_brand = [
    "rhys man",
    "lavia",
    "namnung",
    "ovychee",
    "voudioty",
    "nguyên xuân",
    "weilaiya",
    "moroccanoil",
    "cỏ cây hoa lá",
    "sao thái dương",
    "spes",
    "lisap",
    "tresemmé",
    "tigi",
    "batious",
    "head & shoulders",
    "shot",
]

data_raw = df_raw.to_dict("records")
headers = {'User-Agent': 'Mozilla/5.0'}
path_folder_input = r"C:\Users\dongk\Downloads\Thư mục brand dầu gội xả"

def process_image(raw):
    for brand in list_brand:
        brand_folder_path = os.path.join(path_folder_input, brand)
        os.makedirs(brand_folder_path, exist_ok=True)
        url_thumbnail = raw["url_thumbnail"]
        product_base_id = raw["product_base_id"]
        brand_gop = raw["brand_clean_final"]
        cate = raw["cate_final"]
        # dieu_kien_them = raw["top_90"]
        if brand == brand_gop and cate != "x":
            try:
                response = requests.get(url_thumbnail, headers=headers, timeout=10)
                response.raise_for_status()
                img = Image.open(BytesIO(response.content))
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                save_path = os.path.join(brand_folder_path, f"{product_base_id}.jpg")
                img.save(save_path, format='JPEG')
            except requests.RequestException as e:
                print(f"Error downloading {url_thumbnail}: {e}")
                raw["error_url_thumbnail"] = "x"
            except Exception as e:
                print(f"Error processing image {product_base_id}: {e}")
                raw["error_url_thumbnail"] = "x"

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(process_image, raw) for raw in data_raw]
    for future in tqdm(as_completed(futures), total=len(futures)):
        try:
            future.result()
        except Exception as e:
            print(f"Error in future: {e}")

df = pd.DataFrame(data_raw)
path_excel_output = r"C:\Users\dongk\Downloads\cleaned_dau_goi_xa_fianl.xlsx"
df.to_excel(path_excel_output,index=False)
