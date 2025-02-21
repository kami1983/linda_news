import unittest
from unittest.mock import patch

# 假设 filterCsvData 在 csv_manager 模块中
from libs.csv_manager import filterCsvData

class TestFilterCsvData(unittest.TestCase):

    @patch('libs.csv_manager.readCsvData')
    def test_filter_with_valid_type_and_value(self, mock_read_csv_data):
        # 模拟 readCsvData 返回的数据
        mock_read_csv_data.return_value = [
            ['apple', 'banana', 'cherry']
        ]

        # 测试过滤功能
        result = filterCsvData(['fruit'], 1, 'apple,blueberry ,strawberry, banana', ',')
        expected_result = ['apple', 'banana']
        self.assertEqual(result, expected_result)

    @patch('libs.csv_manager.readCsvData')
    def test_filter_with_invalid_type(self, mock_read_csv_data):
        mock_read_csv_data.return_value = [
            ['apple', 'banana', 'cherry']
        ]
        with self.assertRaises(ValueError):
            filterCsvData(['fruit'], 3, 'apple')
    
    @patch('libs.csv_manager.readCsvData')
    def test_filter_with_empty_filter_value(self, mock_read_csv_data):
        mock_read_csv_data.return_value = [
            ['apple', 'banana', 'cherry']
        ]
        result = filterCsvData(['fruit'], 1, '')
        self.assertEqual(result, [])
        

if __name__ == '__main__':
    unittest.main() 