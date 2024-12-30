import re

def replace_and_merge_special_chars(row, lst_gop):
    product_name = row["product_name"]
    pattern = r'[^\w\s+\/\-,%]'
    replaced_text = re.sub(pattern, '+', product_name)
    replaced_text = replaced_text.replace("+ +", "+")
    merged_text = re.sub(r'\++', '+', replaced_text)

    if merged_text.endswith("+"):
        merged_text = merged_text[:-1].strip()
    
    if merged_text.startswith("+"):
        plus_indexes = [i for i, char in enumerate(merged_text) if char == '+']
        if len(plus_indexes) > 1:
            delete_text = merged_text[plus_indexes[0]:plus_indexes[1]]
            for gop in lst_gop:
                if gop in delete_text:
                    result_text = re.sub(r"[^a-zA-Zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ\s\d]", " ", merged_text).strip()
                    result_text = re.sub(r'\+', '', result_text)
                    break
            else:
                result_text = merged_text[:plus_indexes[0]] + merged_text[plus_indexes[1]:]
                result_text = re.sub(r'\+', '', result_text)
                result_text = re.sub(r'\s+', ' ', result_text).strip()
        elif len(plus_indexes) == 1:
            result_text = re.sub(r'\+', '', merged_text)
            result_text = re.sub(r'\s+', ' ', result_text).strip()
        else:
            result_text = re.sub(r'\+', '', merged_text).strip()
            result_text = re.sub(r'\s+', ' ', result_text)
    else:
        result_text = re.sub(r'\+', '', merged_text).strip()
        result_text = re.sub(r'\s+', ' ', result_text)

    return result_text
