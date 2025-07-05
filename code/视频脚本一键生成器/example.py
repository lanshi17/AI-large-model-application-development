"""
🎬 AI脚本生成器 - 使用示例

这个文件展示了如何使用 generate_script 函数来生成视频脚本。
适合开发者测试和集成使用。
"""

from utils import generate_script
import os

def example_usage():
    """📝 基础使用示例"""
    print("🎬 AI脚本生成器 - 基础示例")
    print("=" * 50)
    
    # 示例参数
    subject = "人工智能如何改变我们的生活"
    video_length = 5
    creativity = 0.7
    api_key = os.getenv("OPENAI_API_KEY", "your-api-key-here")
    
    print(f"📝 主题: {subject}")
    print(f"⏰ 时长: {video_length} 分钟")
    print(f"✨ 创意: {creativity}")
    print(f"🔑 API: {'已配置' if api_key != 'your-api-key-here' else '需要配置'}")
    print("-" * 50)
    
    if api_key == "your-api-key-here":
        print("⚠️  请先配置API密钥:")
        print("   1. 设置环境变量: OPENAI_API_KEY=your_key")
        print("   2. 或直接修改本文件中的 api_key 变量")
        return
    
    try:
        print("🚀 开始生成脚本...")
        
        # 调用生成函数
        search_result, title, script = generate_script(
            subject=subject,
            video_length=video_length,
            creativity=creativity,
            api_key=api_key
        )
        
        print("✅ 生成成功！")
        print("=" * 50)
        
        print(f"\n📺 视频标题:")
        print(f"   {title}")
        
        print(f"\n📝 视频脚本:")
        print(f"   {script[:200]}..." if len(script) > 200 else f"   {script}")
        
        print(f"\n📚 参考信息:")
        print(f"   {search_result[:150]}..." if len(search_result) > 150 else f"   {search_result}")
        
        print("\n" + "=" * 50)
        print("🎉 示例完成！")
        
        # 保存到文件
        filename = f"生成示例_{subject[:10]}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"【标题】\n{title}\n\n【脚本】\n{script}\n\n【参考】\n{search_result}")
        print(f"💾 结果已保存到: {filename}")
        
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        print("💡 请检查:")
        print("   1. API密钥是否正确")
        print("   2. 网络连接是否正常")
        print("   3. API服务是否可用")

def batch_example():
    """📚 批量生成示例"""
    print("\n🎬 AI脚本生成器 - 批量示例")
    print("=" * 50)
    
    subjects = [
        "5G技术对未来生活的影响",
        "环保小贴士：从日常做起",
        "学习编程的最佳方法"
    ]
    
    api_key = os.getenv("OPENAI_API_KEY", "your-api-key-here")
    
    if api_key == "your-api-key-here":
        print("⚠️  批量生成需要API密钥，请先配置")
        return
    
    for i, subject in enumerate(subjects, 1):
        print(f"\n🎯 正在生成第 {i}/{len(subjects)} 个脚本...")
        print(f"📝 主题: {subject}")
        
        try:
            search_result, title, script = generate_script(
                subject=subject,
                video_length=3,
                creativity=0.6,
                api_key=api_key
            )
            
            print(f"✅ 标题: {title}")
            print(f"📄 脚本长度: {len(script)} 字符")
            
        except Exception as e:
            print(f"❌ 失败: {e}")

if __name__ == "__main__":
    # 运行基础示例
    example_usage()
    
    # 询问是否运行批量示例
    print("\n" + "=" * 50)
    choice = input("🤔 是否运行批量生成示例？(y/N): ").lower()
    if choice in ['y', 'yes']:
        batch_example()
    
    print("\n👋 感谢使用 AI脚本生成器！")
