"""
视频脚本生成器核心测试
"""
import unittest
import os
import sys
from unittest.mock import Mock, patch

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import generate_script


class TestVideoScriptGenerator(unittest.TestCase):
    """视频脚本生成器测试"""
    
    def setUp(self):
        """测试前的准备工作"""
        self.test_subject = "人工智能的发展历史"
        self.test_video_length = 5
        self.test_creativity = 0.7
        self.test_api_key = "test_api_key"
    
    def _setup_mocks(self, mock_template, mock_chat_openai, mock_wikipedia):
        """设置Mock对象"""
        # 设置Wikipedia mock
        mock_wiki_instance = Mock()
        mock_wiki_instance.run.return_value = "测试维基百科搜索结果"
        mock_wikipedia.return_value = mock_wiki_instance
        
        # 设置ChatOpenAI mock
        mock_openai_instance = Mock()
        mock_chat_openai.return_value = mock_openai_instance
        
        # 设置ChatPromptTemplate mock - 每次调用都返回新的模板
        def create_template():
            template = Mock()
            chain = Mock()
            response = Mock()
            response.content = "测试内容"
            chain.invoke.return_value = response
            template.__or__ = Mock(return_value=chain)
            return template
        
        mock_template.from_messages.return_value = create_template()
    
    @patch('utils.WikipediaAPIWrapper')
    @patch('utils.ChatOpenAI')
    @patch('utils.ChatPromptTemplate')
    def test_generate_script_basic(self, mock_template, mock_chat_openai, mock_wikipedia):
        """测试基本功能"""
        self._setup_mocks(mock_template, mock_chat_openai, mock_wikipedia)
        
        result = generate_script(
            self.test_subject,
            self.test_video_length,
            self.test_creativity,
            self.test_api_key
        )
        
        # 验证结果
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 3)
        
        search_result, title, script = result
        self.assertEqual(search_result, "测试维基百科搜索结果")
        self.assertEqual(title, "测试内容")
        self.assertEqual(script, "测试内容")
    
    @patch('utils.WikipediaAPIWrapper')
    @patch('utils.ChatOpenAI')
    @patch('utils.ChatPromptTemplate')
    def test_generate_script_parameters(self, mock_template, mock_chat_openai, mock_wikipedia):
        """测试参数传递"""
        self._setup_mocks(mock_template, mock_chat_openai, mock_wikipedia)
        
        # 测试不同参数
        test_cases = [
            ("科技发展", 3, 0.5),
            ("环保知识", 10, 1.0),
        ]
        
        for subject, length, creativity in test_cases:
            with self.subTest(subject=subject):
                result = generate_script(subject, length, creativity, self.test_api_key)
                self.assertIsInstance(result, tuple)
                self.assertEqual(len(result), 3)


if __name__ == '__main__':
    unittest.main(verbosity=2)
