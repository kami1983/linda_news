import os
import csv

from dotenv import load_dotenv
from libs.constants import CSV_TYPE_CATEGORY, CSV_TYPE_CONCEPT

# 加载环境变量
load_dotenv()

UPLOAD_FOLDER = os.getenv('CSV_UPLOAD_FOLDER')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def getCsvFilePath(type)->str:
    return makeCsvLablePath(type, label=0)
    
def makeCsvLablePath(type, label=0)->str:
    label = int(label)
    if label < 0:
        raise ValueError('Invalid label parameter')
    
    if type not in [1, 2]:
        raise ValueError('Invalid type parameter')

    if type == CSV_TYPE_CATEGORY:
        if label > 0:
            return os.path.join(UPLOAD_FOLDER, f'{label}.category.csv') 
        else:
            return os.path.join(UPLOAD_FOLDER, 'category.csv')
    elif type == CSV_TYPE_CONCEPT:
        if label > 0:
            return os.path.join(UPLOAD_FOLDER, f'{label}.concept.csv')
        else:
            return os.path.join(UPLOAD_FOLDER, 'concept.csv')

def readCsvData(columns, type, label=0)->list[list[str]]:
    if type not in [1, 2]:
        raise ValueError('Invalid type parameter')

    file_path = makeCsvLablePath(type, label)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'File {file_path} not found')

    # 获取所有行的  columns 列 
    data = []
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append([row[col] for col in columns])
    
    return data

# 根据列名和类型过滤数据
# columns: 列名
# type: 类型
# filter_value: 过滤值, 多个值用|分开
def filterCsvData(columns, type, filter_value: str, split_symbol='|', label=0) -> list[str]:
    if type not in [CSV_TYPE_CATEGORY, CSV_TYPE_CONCEPT]:
        raise ValueError('Invalid type parameter')
    # 过滤值需要根据 split_symbol 分割
    filter_list = filter_value.split(split_symbol)
    # 获取二维数组列
    data = readCsvData(columns, type, label)
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

def getCsvValueByColname(find_colname, find_value, output_colnames=['PE.等权', 'PB.等权'], type=1, label=0)->list[str]:
    '''
    根据列名和值获取对应的值
    find_colname: 需要查找的列名
    key_colname: 关键列名
    key_value: 关键列的值
    type: 类型
    '''
    data = readCsvData([find_colname, *output_colnames], type, label)
    for row in data:
        if row[0] == find_value:
            
            return row[1:]
    return []
