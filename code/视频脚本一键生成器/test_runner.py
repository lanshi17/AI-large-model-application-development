"""
简化的测试运行脚本
"""
import unittest
import sys
import os


def run_tests():
    """运行测试"""
    print("🧪 运行测试...")
    
    # 发现并运行测试
    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test_*.py')
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出结果
    print(f"\n{'='*50}")
    print(f"测试结果:")
    print(f"总测试数: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print(f"状态: {'✅ 通过' if result.wasSuccessful() else '❌ 失败'}")
    print(f"{'='*50}")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
