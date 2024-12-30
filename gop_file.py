import os
from pprint import pprint
import openpyxl
import pandas as pd
import numpy

folder_path = r"C:\Users\dongv\Downloads\gọp brand"
output_file_path = r"C:\Users\dongv\Downloads\Trà_29_11_2024_gop_brand.xlsx"
# output_root_excel_path = r"D:\Mỹ Phẩm\product_Cosmeceuticals_goc.xlsx"
# out_put_merged_df = r"D:\Mỹ Phẩm\out_merged_df.xlsx"

lst_id_error = []

wb_output = openpyxl.Workbook()

# merge file excel from folder
def merge_excel(path_folder, output_excel_path):
    combined_df = pd.DataFrame()

    for root, dirs, files in os.walk(path_folder):
        for file in files:
            if file.endswith(".xlsx"):
                file_path = os.path.join(root, file)
                df = pd.read_excel(file_path, sheet_name="Sheet1")
                combined_df = pd.concat([combined_df, df], ignore_index=True)

    with pd.ExcelWriter(output_file_path, engine="xlsxwriter",engine_kwargs={"options": {"strings_to_urls": False}}) as writer2:
        combined_df.to_excel(writer2, index=False)

    print(f"Gộp thành công! File tổng hợp đã được lưu tại: {output_excel_path}")
    return combined_df
merge_excel(folder_path, output_file_path)
