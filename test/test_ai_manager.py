import unittest
from unittest.mock import patch
from libs.ai_manager import getConfigValueWithConfigBeatNum

class TestAiManager(unittest.TestCase):

    @patch('libs.ai_manager.getConfBeatNum')
    def test_get_config_value_with_config_beat_num(self, mock_get_conf_beat_num):
        # 模拟 getConfBeatNum 的返回值
        mock_get_conf_beat_num.return_value = 1

        # 测试用例1：多个值
        config_value = "key1|key2|key3"
        result = getConfigValueWithConfigBeatNum(config_value)
        self.assertEqual(result, "key2")

        # 测试用例2：单个值
        mock_get_conf_beat_num.return_value = 5
        config_value = "singlekey"
        result = getConfigValueWithConfigBeatNum(config_value)
        self.assertEqual(result, "singlekey")

        # 测试用例3：空字符串
        mock_get_conf_beat_num.return_value = 0
        config_value = ""
        result = getConfigValueWithConfigBeatNum(config_value)
        self.assertEqual(result, "")
    pass

if __name__ == '__main__':
    unittest.main() 