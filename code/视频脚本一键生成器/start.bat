@echo off
echo ==========================================
echo      🎬 AI脚本生成器 - 年轻清爽版
echo ==========================================
echo.
echo 🎨 年轻人的创意工具正在启动...
echo.
echo 正在检查依赖...
python -c "import streamlit" 2>nul
if %errorlevel% neq 0 (
    echo 正在安装依赖...
    pip install streamlit
)
echo.
echo 🚀 启动应用...
echo 📱 应用将在浏览器中打开: http://localhost:8504
echo.
streamlit run main.py --server.port 8504
pause
