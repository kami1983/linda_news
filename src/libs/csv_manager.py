import os
import csv

from dotenv import load_dotenv
from .constants import CSV_TYPE_CATEGORY, CSV_TYPE_CONCEPT

# 加载环境变量
load_dotenv()

UPLOAD_FOLDER = os.getenv('CSV_UPLOAD_FOLDER')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def getCsvFilePath(type)->str:
    if type not in [1, 2]:
        raise ValueError('Invalid type parameter')

    if type == CSV_TYPE_CATEGORY:
        return os.path.join(UPLOAD_FOLDER, 'category.csv')
    elif type == CSV_TYPE_CONCEPT:
        return os.path.join(UPLOAD_FOLDER, 'concept.csv')
    
def makeCsvLablePath(type, label)->str:
    label = int(label)
    if label <= 0:
        raise ValueError('Invalid label parameter')
    
    if type not in [1, 2]:
        raise ValueError('Invalid type parameter')

    if type == CSV_TYPE_CATEGORY:
        return os.path.join(UPLOAD_FOLDER, f'{label}.category.csv')
    elif type == CSV_TYPE_CONCEPT:
        return os.path.join(UPLOAD_FOLDER, f'{label}.concept.csv')

def readCsvData(columns, type)->list[list[str]]:
    if type not in [1, 2]:
        raise ValueError('Invalid type parameter')

    # if type == 1:
    #     filename = 'concept.csv'
    # elif type == 2:
    #     filename = 'category.csv'

    # file_path = os.path.join(UPLOAD_FOLDER, filename)

    file_path = getCsvFilePath(type)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'File {file_path} not found')

    # 获取所有行的  columns 列 
    data = []
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append([row[col] for col in columns])
    
    # print(type, data)
    return data

# 根据列名和类型过滤数据
# columns: 列名
# type: 类型
# filter_value: 过滤值, 多个值用|分开
def filterCsvData(columns, type, filter_value: str, split_symbol='|') -> list[str]:
    if type not in [CSV_TYPE_CATEGORY, CSV_TYPE_CONCEPT]:
        raise ValueError('Invalid type parameter')
    # 过滤值需要根据 split_symbol 分割
    filter_list = filter_value.split(split_symbol)
    # 获取二维数组列
    data = readCsvData(columns, type)
    # 过滤数据
    filtered_data = []
    for row in data:
        for check_value in filter_list:
            if check_value.strip() in row:
                filtered_data.append(check_value.strip())
    return filtered_data



def modifyCsvHeaders(input_file, output_file):
    with open(input_file, mode='r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        headers = next(reader)

        # 修改重复的列名
        new_headers = []
        previous_header = None

        for header in headers:
            if header == '百分位':
                if previous_header:
                    new_headers.append(f'{previous_header}.百分位')
                else:
                    new_headers.append(header)
            else:
                new_headers.append(header)
            previous_header = header

        # 写入新的 CSV 文件
        with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(new_headers)
            for row in reader:
                writer.writerow(row)