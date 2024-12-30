import os
from pprint import pprint
import cv2
import numpy as np
from PIL import Image
import requests
import pandas as pd
from io import BytesIO
from sympy.concrete import products
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed



# folder_check = r
folder_img = r"D:\tag_cate_sữa"

# lấy id từ hình ảnh
dict_img = {}
for root, dirs, files in os.walk(folder_img):
    for dir in dirs:
        path_folder_child = os.path.join(root, dir)
        dict_img[dir] = path_folder_child

list_dict = []
dict_result = {}
for key, path_value in dict_img.items():
    list_id_img = []
    for root, dirs, files in os.walk(path_value):
        for file in files:
            id_img = file.split(".")[0]
            list_id_img.append(id_img)

    join_list_id_img = ",".join(list_id_img)
    dict_result = {
        "brand": key,
        "product_base" : join_list_id_img
    }
    list_dict.append(dict_result)

path_excel_input = r"C:\Users\dongk\Downloads\sữa nước ko lấy được ảnh.xlsx"
df_data = pd.read_excel(path_excel_input, sheet_name="Sheet1")
data_raw = df_data.to_dict("records")

for raw in data_raw:
    product_base_id = str(raw["product_base_id"])
    brand = None
    for result in list_dict:
        key_brand = result["brand"]
        key_value = result["product_base"]
        if product_base_id in key_value:
            brand = key_brand
    raw["check_no_brand"] = brand


path_excel_output = r"C:\Users\dongk\Downloads\sữa nước tag_cate_image_code.xlsx"
df = pd.DataFrame(data_raw)
with pd.ExcelWriter(path_excel_output, engine="xlsxwriter",engine_kwargs={"options": {"strings_to_urls": False}}) as writer2:
    df.to_excel(writer2, index=False, sheet_name="data_sample")


# # tag id hình ảnh lọc
# path_folder_input = r"D:\Python_code\Data_về\máy hút bụi\tag thêm brand"
# path_excel_input = r"C:\Users\dongk\Downloads\máy hút bụi all v2_ (1).xlsx"
# df_raw = pd.read_excel(path_excel_input, sheet_name="Sheet1")
# data_raw = df_raw.to_dict("records")
#
# list_id = set()
# for root, dirs, files in os.walk(path_folder_input):
#     for file in files:
#         id_img = file.split(".")[0]
#         list_id.add(id_img)
#
# for raw in data_raw:
#     product_base_id = raw["product_base_id"]
#     if product_base_id in list_id:
#         raw["loại"] = "x"
#
# path_excel_output = r"C:\Users\dongk\Downloads\máy hút bụi 1306.xlsx"
# df = pd.DataFrame(data_raw)
# with pd.ExcelWriter(path_excel_output, engine="xlsxwriter",engine_kwargs={"options": {"strings_to_urls": False}}) as writer2:
#     df.to_excel(writer2, index=False)

