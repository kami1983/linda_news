import os
import csv

UPLOAD_FOLDER = os.getenv('CSV_UPLOAD_FOLDER')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def getCsvFilePath(type):
    if type not in [1, 2]:
        raise ValueError('Invalid type parameter')

    if type == 1:
        return os.path.join(UPLOAD_FOLDER, 'concept.csv')
    elif type == 2:
        return os.path.join(UPLOAD_FOLDER, 'category.csv')

def readCsvData(columns, type):
    if type not in [1, 2]:
        raise ValueError('Invalid type parameter')

    if type == 1:
        filename = 'concept.csv'
    elif type == 2:
        filename = 'category.csv'

    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'File {filename} not found')

    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        # 获取所有行的  columns 列 
        data = []
        for row in reader:
            data.append([row[col] for col in columns])
            
    return data