import clickhouse_connect
import pandas as pd
import re


clickhouse_config = {
    'Host': '',
    'Port': '',
    'User': '',
    'Password': ''
}

# path_csv = r"C:\Users\dongv\Downloads\brand_ereport.txt"
#
# lst_brand = []
# with open(path_csv, 'r', encoding='utf-8') as f:
#     data = f.readlines()
#     for i in range(len(data)):
#         data[i] = data[i].replace('\n', '')
#         if data[i] != "":
#             lst_brand.append(data[i])
path_excel_input = r"C:\Users\dongv\Downloads\tra_update_to_15112024 (1).xlsx"
df_brand = pd.read_excel(path_excel_input, sheet_name='Sheet1')
lst_brand = df_brand[df_brand["product_base_id"].notna()]["product_base_id"].str.strip().str.lower().tolist()
# print(len(lst_brand))
# for idx, row in df_brand.iterrows():
#     brand_clean = str(row['brand_clean']).lower().strip()
#     if brand_clean != 'x':
#         lst_brand.add(brand_clean)

print(len(lst_brand))
# Hàm chuẩn hóa tên brand
def normalize_brand(brand):
    return f"'{brand}'"

def normalize_like_brand(brand):
    return f"'%{brand}%'"

# Hàm xây dựng query cho ClickHouse
def build_query_clickhouse(brand):
    normalize = normalize_brand(brand)
    query_clickhouse = f"""
    SELECT product_base_id, product_name FROM tmp.ereport_product_final_2024M10 WHERE  product_base_id = {normalize_brand(brand)}
    """
    return query_clickhouse
def clean_invalid_characters(value):
    if isinstance(value, str):
        return re.sub(r'[\x00-\x1F\x7F]', '', value)
    return value
def run():
    client = clickhouse_connect.get_client(
        host=clickhouse_config['Host'],
        port=clickhouse_config['Port'],
        user=clickhouse_config['User'],
        password=clickhouse_config['Password']
    )

    all_results = []

    for brand in lst_brand:
        query = build_query_clickhouse(brand)

        print(f"Generated query: {query}")

        try:
            aggs = client.query(query)
            result = aggs.result_rows
            column_names = aggs.column_names
            print(f"Columns returned: {column_names}")

            if result:
                print("Query Result:")
                print(result)
                cleaned_result = [
                    [clean_invalid_characters(cell) for cell in row]
                    for row in result
                ]
                df = pd.DataFrame(cleaned_result, columns=column_names)

                all_results.append(df)
            else:
                print("No results returned.")

        except Exception as e:
            print(f"An error occurred: {e}")

    if all_results:
        final_df = pd.concat(all_results, ignore_index=True)
        output_file = r"C:\Users\dongv\Downloads\qc_da_nganh_hang.xlsx"
        final_df.to_excel(output_file, index=False)
        print(f"Results have been saved to {output_file}")
    else:
        print("No results to save.")

if __name__ == '__main__':
    run()
