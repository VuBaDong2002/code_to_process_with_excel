import ast


def dong_txt(path, dict=None, regime=None):
    if regime not in ['write', 'read']:
        raise ValueError("Chế độ phải là 'write' hoặc 'read'")
    if regime == 'write':
        if dict is None:
            raise ValueError("Cần cung cấp một từ điển khi chế độ là 'write'.")

        with open(path, 'w', encoding='utf-8') as file:
            for key, value in dict.items():
                if isinstance(value, set):
                    file.write(f"'{key}': {value}\n")
                else:
                    print(f"Cảnh báo: Giá trị của {key} không phải là set. Bỏ qua.")
    elif regime == 'read':
        with open(path, 'r', encoding='utf-8') as file:
            text = file.read()
        dict_brand_variable_v2 = {}
        lines = text.splitlines()

        for line in lines:
            line = line.strip()
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().strip("'")
                value = value.strip()
                try:
                    value_set = ast.literal_eval(value)
                    if isinstance(value_set, set):
                        dict_brand_variable_v2[key] = value_set
                    else:
                        print(f"Cảnh báo: Giá trị của {key} không phải là set.")
                except (ValueError, SyntaxError) as e:
                    print(f"Lỗi khi phân tích giá trị cho {key}: {e}")

        return dict_brand_variable_v2


