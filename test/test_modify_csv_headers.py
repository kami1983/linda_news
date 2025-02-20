import unittest
import os
import csv
from src.libs.csv_manager import modifyCsvHeaders

class TestModifyCsvHeaders(unittest.TestCase):

    def setUp(self):
        # 创建一个临时的输入 CSV 文件
        self.input_file = 'test_input.csv'
        self.output_file = 'test_output.csv'
        with open(self.input_file, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['序', '代码', '行业', 'PE.加权', '百分位', 'PE.等权', '百分位', 'PB.加权', '百分位'])
            writer.writerow(['1', '0474', '保险', '8.83', '1.88%', '8.03', '0.52%', '1.36', '24.50%'])

    def tearDown(self):
        # 删除临时文件
        if os.path.exists(self.input_file):
            os.remove(self.input_file)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_modifyCsvHeaders(self):
        # 调用函数
        modifyCsvHeaders(self.input_file, self.output_file)

        # 验证输出文件
        with open(self.output_file, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            expected_headers = ['序', '代码', '行业', 'PE.加权', 'PE.加权.百分位', 'PE.等权', 'PE.等权.百分位', 'PB.加权', 'PB.加权.百分位']
            self.assertEqual(headers, expected_headers)

if __name__ == '__main__':
    unittest.main() 