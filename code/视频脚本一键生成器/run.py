import subprocess
import webbrowser
import time
import socket
import sys
import os

def get_local_ip():
    """获取本机IP地址"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def check_requirements():
    """检查依赖是否安装"""
    try:
        import streamlit
        return True
    except ImportError:
        print("❌ Streamlit 未安装")
        print("📦 正在安装依赖...")
        subprocess.run([sys.executable, "-m", "pip", "install", "streamlit"])
        return True

def start_app():
    """启动应用"""
    port = 8504
    host = "0.0.0.0"
    
    print("🚀 启动AI脚本生成器...")
    print("🎨 年轻人的创意工具已准备就绪！")
    print(f"📍 本地访问: http://localhost:{port}")
    print(f"🌐 网络访问: http://{get_local_ip()}:{port}")
    print("=" * 50)
    
    # 检查依赖
    if not check_requirements():
        return
    
    # 检查main.py文件是否存在
    main_py_path = os.path.join(os.path.dirname(__file__), "main.py")
    if not os.path.exists(main_py_path):
        print("❌ main.py 文件不存在")
        return
    # 启动streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", main_py_path,
            "--server.address", host,
            "--server.port", str(port)
        ])
    except KeyboardInterrupt:
        print("\n👋 感谢使用AI脚本生成器！")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

if __name__ == "__main__":
    start_app()