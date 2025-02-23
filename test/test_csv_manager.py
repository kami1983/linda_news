import unittest
import os
from unittest.mock import patch

# 假设 filterCsvData 和 getCsvValueByColname 在 csv_manager 模块中
from libs.csv_manager import filterCsvData, getCsvValueByColname

class TestCsvManager(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('libs.csv_manager.readCsvData')
    def test_get_csv_value_by_colname(self, mock_read_csv_data):
        mock_read_csv_data.return_value = [
            ['Alice', '30', 'New York'],
            ['Bob', '25', 'Los Angeles'],
            ['Charlie', '35', 'Chicago']
        ]
        # 测试获取 'name' 列的值
        expected_names = ['25', 'Los Angeles']
        result = getCsvValueByColname('name', 'Bob', ['age', 'city'])
        self.assertEqual(result, expected_names)

    @patch('libs.csv_manager.readCsvData')
    def test_get_csv_value_by_colname_with_nonexistent_colname(self, mock_read_csv_data):
        mock_read_csv_data.return_value = [
            ['New York', '30'],
            ['Los Angeles', '25'],
            ['Chicago', '35'],
            ['New York', '23'],
            ['Los Angeles', '44'],
            ['Chicago', '12'],
        ]
        # 测试获取 'age' 列的值
        expected_ages = ['35']
        result = getCsvValueByColname('city', 'Chicago', ['age'])
        self.assertEqual(result, expected_ages)
    


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