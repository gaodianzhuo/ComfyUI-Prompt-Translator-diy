import json
import re
import os
import csv
import string
from collections import OrderedDict
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast,MarianMTModel,MarianTokenizer


# model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
# tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")

# my_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')
my_dir = os.path.dirname(os.path.abspath(__file__))

parent_directory_path = os.path.dirname(my_dir)  # 获取上一级目录的路径

# print(parent_directory_path)


my_translations = parent_directory_path + "/translations.csv"


# 速度慢,文件大
# model_id = os.path.dirname(os.path.dirname(parent_directory_path)) + "/mbart-large-50-many-to-one-mmt"
# model = MBartForConditionalGeneration.from_pretrained(model_id)
# tokenizer = MBart50TokenizerFast.from_pretrained(model_id)

# def translate(text):
#     try:
#         encoded = tokenizer(text, return_tensors="pt")
#         generated_tokens = model.generate(
#             **encoded,
#             forced_bos_token_id=tokenizer.lang_code_to_id["en_XX"]
#         )
#         return tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
#     except:
#         print("文本翻译错误" )
#         return text



model_id = os.path.dirname(os.path.dirname(parent_directory_path)) + "/opus-mt-zh-en"
model = MarianMTModel.from_pretrained("./opus-mt-zh-en")
tokenizer = MarianTokenizer.from_pretrained("./opus-mt-zh-en")



tokenizer.src_lang = "zh_CN"


def translate(chinese_str: str) -> str:
    # 对中文句子进行分词
    input_ids = tokenizer.encode(chinese_str, return_tensors="pt")

    # 进行翻译
    output_ids = model.generate(input_ids)

    # 将翻译结果转换为字符串格式
    english_str = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    #如果最后有一个.，则去掉
    if english_str[-1] == '.':
        english_str = english_str[:-1]
    return english_str



def sort_dict_by_key_length(d):
    sorted_keys = sorted(d.keys(), key=lambda x: len(x),reverse=True)
    sorted_dict = OrderedDict()
    for key in sorted_keys:
        sorted_dict[key] = d[key]
    return sorted_dict




# 读取 csv 文件到内存中缓存起来
def load_csv(csv_file):
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        cache = OrderedDict(reader)
        cache = sort_dict_by_key_length(cache)

    return cache




def contains_chinese(text):
    pattern = re.compile(r'[\u4e00-\u9fa5]')
    return bool(pattern.search(text))




def remove_unnecessary_spaces(text):
    """Removes unnecessary spaces between characters."""
    pattern = r"\)\s*\+\+|\)\+\+\s*"
    replacement = r")++"
    return re.sub(pattern, replacement, text)


def process_text(text):
    # 将中文全角标点符号替换为半角标点符号
    text = text.translate(str.maketrans('，。！？；：‘’“”（）【】', ',.!?;:\'\'\"\"()[]'))
    # 按逗号分割成数组
    text_array = text.split(',')
    # 对数组中每个字符串进行处理
    for i in range(len(text_array)):
        # 如果字符串以 < 开头 > 结尾，则是Lora，跳过不处理
        if text_array[i].startswith('<') and text_array[i].endswith('>'):
            continue
        # 判断是否只包含英文字符
        if all(char in string.printable + ' ' for char in text_array[i]):
            continue
        else:
            # 调用 transfer 函数进行翻译
            text_array[i] = translate(text_array[i])
    # 重新用逗号连接成字符串并返回
    return ','.join(text_array)



def replace_text(text, cache):
    for key, value in cache.items():
        if key in text:
            text = text.replace(key, value + ' ')
    return text




class PromptTextTranslation:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text_trans": ("STRING", {"multiline": True, "default": "海边，日出"}),
                # "trans_switch": (["enabled", "disabled"],),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "translation"
    CATEGORY = "utils"

    def translation(self, text_trans, ):

        if text_trans == "undefined":
            text_trans = ""


        target_text = ""

        print("prompt: ", text_trans)


        cache = load_csv(my_translations)


        # if trans_switch == "enabled" and contains_chinese(text_trans):
        if contains_chinese(text_trans):
            text_trans = remove_unnecessary_spaces(text_trans)
            modified_text = replace_text(text_trans, cache)
            print("modified_text: " + modified_text)

            target_text = process_text(modified_text)
        else:
            target_text = text_trans

        print("target: " + target_text)

        return (target_text,)



