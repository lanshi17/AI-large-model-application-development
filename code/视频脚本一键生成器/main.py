import streamlit as st
from utils import generate_script
import time

# 页面配置
st.set_page_config(
    page_title="脚本生成器",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 年轻清爽的设计样式
st.markdown("""
<style>
/* 全局字体 */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* 主容器 */
.main-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 2rem 0;
}

/* 卡片容器 */
.card {
    background: white;
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    margin-bottom: 2rem;
    backdrop-filter: blur(10px);
}

/* 主标题 */
.main-title {
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(45deg, #667eea, #764ba2);
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 0.5rem;
}

/* 副标题 */
.subtitle {
    font-size: 1.2rem;
    color: #666;
    text-align: center;
    margin-bottom: 3rem;
    font-weight: 400;
}

/* 输入区域样式 */
.input-section {
    background: linear-gradient(135deg, #f8f9ff 0%, #e8f4f8 100%);
    border-radius: 15px;
    padding: 2rem;
    margin-bottom: 2rem;
    border: 1px solid #e1e8ed;
}

/* 按钮样式 */
.stButton > button {
    background: linear-gradient(45deg, #667eea, #764ba2);
    color: white;
    border: none;
    padding: 0.75rem 2rem;
    font-size: 1rem;
    font-weight: 600;
    border-radius: 25px;
    transition: all 0.3s ease;
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    text-transform: uppercase;
    letter-spacing: 1px;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

/* 输入框样式 */
.stTextInput > div > div > input {
    border: 2px solid #e1e8ed;
    border-radius: 15px;
    padding: 1rem;
    font-size: 1rem;
    transition: all 0.3s ease;
    background: white;
}

.stTextInput > div > div > input:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* 滑块样式 */
.stSlider > div > div > div > div {
    background: linear-gradient(45deg, #667eea, #764ba2);
}

/* 标签样式 */
.input-label {
    font-size: 1rem;
    font-weight: 600;
    color: #333;
    margin-bottom: 0.5rem;
    display: block;
}

/* 卡片标题 */
.card-title {
    font-size: 1.5rem;
    font-weight: 600;
    color: #333;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* 状态指示器 */
.status-indicator {
    display: inline-block;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-size: 0.9rem;
    font-weight: 500;
    margin: 0.5rem 0;
}

.status-ready {
    background: linear-gradient(45deg, #4CAF50, #45a049);
    color: white;
}

.status-error {
    background: linear-gradient(45deg, #f44336, #d32f2f);
    color: white;
}

/* 结果展示区 */
.result-container {
    background: linear-gradient(135deg, #fff 0%, #f8f9ff 100%);
    border-radius: 15px;
    padding: 2rem;
    margin-top: 2rem;
    border: 1px solid #e1e8ed;
}

/* 进度条样式 */
.stProgress > div > div > div > div {
    background: linear-gradient(45deg, #667eea, #764ba2);
    border-radius: 10px;
}

/* 操作按钮区域 */
.action-buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
    margin-top: 2rem;
}

/* 下载按钮 */
.stDownloadButton > button {
    background: linear-gradient(45deg, #4CAF50, #45a049);
    color: white;
    border: none;
    padding: 0.75rem 2rem;
    font-size: 1rem;
    font-weight: 600;
    border-radius: 25px;
    transition: all 0.3s ease;
    box-shadow: 0 5px 15px rgba(76, 175, 80, 0.3);
}

.stDownloadButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(76, 175, 80, 0.4);
}

/* 辅助按钮 */
.secondary-button {
    background: linear-gradient(45deg, #ff7043, #f4511e);
    color: white;
    border: none;
    padding: 0.75rem 2rem;
    font-size: 1rem;
    font-weight: 600;
    border-radius: 25px;
    transition: all 0.3s ease;
    box-shadow: 0 5px 15px rgba(255, 112, 67, 0.3);
}

/* 文本区域 */
.stTextArea > div > div > textarea {
    border: 2px solid #e1e8ed;
    border-radius: 15px;
    padding: 1rem;
    font-size: 1rem;
    transition: all 0.3s ease;
    background: white;
}

.stTextArea > div > div > textarea:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* 提示信息 */
.tip-card {
    background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
    border-radius: 15px;
    padding: 1.5rem;
    margin: 1rem 0;
    border-left: 4px solid #ffc107;
}

/* 成功消息 */
.success-message {
    background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
    color: #155724;
    border-radius: 15px;
    padding: 1rem;
    margin: 1rem 0;
    border-left: 4px solid #28a745;
}

/* 错误消息 */
.error-message {
    background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
    color: #721c24;
    border-radius: 15px;
    padding: 1rem;
    margin: 1rem 0;
    border-left: 4px solid #dc3545;
}

/* 特色区域 */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.feature-card {
    background: white;
    border-radius: 15px;
    padding: 1.5rem;
    text-align: center;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
}

.feature-card:hover {
    transform: translateY(-5px);
}

.feature-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
}

/* 隐藏默认元素 */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {visibility: hidden;}

/* 响应式设计 */
@media (max-width: 768px) {
    .main-title {
        font-size: 2.5rem;
    }
    
    .card {
        padding: 1.5rem;
    }
    
    .feature-grid {
        grid-template-columns: 1fr;
    }
}
</style>
""", unsafe_allow_html=True)

# 主标题区域
st.markdown('''
<div class="main-title">🎬 AI脚本生成器</div>
<div class="subtitle">年轻人的创意工具，让视频制作更轻松！</div>
''', unsafe_allow_html=True)

# 特色功能展示
st.markdown('''
<div class="feature-grid">
    <div class="feature-card">
        <div class="feature-icon">🚀</div>
        <h3>快速生成</h3>
        <p>AI驱动，秒级生成专业脚本</p>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🎨</div>
        <h3>创意无限</h3>
        <p>多种风格，满足不同需求</p>
    </div>
    <div class="feature-card">
        <div class="feature-icon">📱</div>
        <h3>简单易用</h3>
        <p>界面友好，操作简单</p>
    </div>
    <div class="feature-card">
        <div class="feature-icon">💎</div>
        <h3>质量保证</h3>
        <p>专业算法，高质量输出</p>
    </div>
</div>
''', unsafe_allow_html=True)

# 主要输入区域
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-title">📝 创作参数</div>', unsafe_allow_html=True)

# 输入参数区域
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    
    # 视频主题输入
    st.markdown('<label class="input-label">🎯 视频主题</label>', unsafe_allow_html=True)
    subject = st.text_input("视频主题", placeholder="输入你的视频主题，比如：人工智能的未来发展...", key="subject", label_visibility="collapsed")
    
    # 参数设置
    col_param1, col_param2 = st.columns(2)
    with col_param1:
        st.markdown('<label class="input-label">⏰ 视频时长</label>', unsafe_allow_html=True)
        video_length = st.slider("视频时长", 1, 30, 5, help="设置视频时长（分钟）", key="length", label_visibility="collapsed")
    
    with col_param2:
        st.markdown('<label class="input-label">✨ 创意系数</label>', unsafe_allow_html=True)
        creativity = st.slider("创意系数", 0.0, 1.0, 0.7, 0.1, help="数值越高，内容越有创意", key="creativity", label_visibility="collapsed")
    
    # API密钥输入
    st.markdown('<label class="input-label">🔑 API密钥</label>', unsafe_allow_html=True)
    api_key = st.text_input("API密钥", placeholder="输入你的API密钥", type="password", key="api_key", label_visibility="collapsed")
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div style="padding: 2rem 0;">', unsafe_allow_html=True)
    
    # 生成按钮
    generate_clicked = st.button("🚀 开始生成", type="primary", use_container_width=True)
    
    # 状态指示
    if subject and api_key:
        st.markdown('<div class="status-indicator status-ready">✅ 准备就绪</div>', unsafe_allow_html=True)
    else:
        missing = []
        if not subject:
            missing.append("主题")
        if not api_key:
            missing.append("API密钥")
        st.markdown(f'<div class="status-indicator status-error">❌ 缺少: {", ".join(missing)}</div>', unsafe_allow_html=True)
    
    # 参数预览
    st.markdown('''
    <div class="tip-card">
        <h4>💡 当前设置</h4>
        <p><strong>时长:</strong> {} 分钟</p>
        <p><strong>创意:</strong> {}</p>
        <p><strong>状态:</strong> {}</p>
    </div>
    '''.format(
        video_length, 
        creativity,
        "就绪" if subject and api_key else "待完善"
    ), unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# 生成逻辑和结果展示
if generate_clicked:
    if not subject:
        st.markdown('<div class="error-message">😅 别忘了输入视频主题哦！</div>', unsafe_allow_html=True)
    elif not api_key:
        st.markdown('<div class="error-message">🔑 还需要输入API密钥才能开始创作</div>', unsafe_allow_html=True)
    else:
        # 生成过程展示
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">🎬 AI正在为你创作...</div>', unsafe_allow_html=True)
        
        # 进度条和状态
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # 生成过程模拟
        stages = [
            (25, "🔍 正在搜索相关资料..."),
            (50, "🧠 AI大脑正在思考..."),
            (75, "✍️ 正在精心创作脚本..."),
            (100, "🎉 即将完成！")
        ]
        
        for progress, message in stages:
            progress_bar.progress(progress)
            status_text.markdown(f'<div style="text-align: center; padding: 1rem; font-size: 1.1rem; color: #667eea;">{message}</div>', unsafe_allow_html=True)
            time.sleep(0.5)
        
        # 调用生成函数
        try:
            search_result, title, script = generate_script(
                subject,
                video_length,
                creativity,
                api_key
            )
            
            # 清理进度指示器
            progress_bar.empty()
            status_text.empty()
            
            # 成功提示
            st.markdown('<div class="success-message">🎉 太棒了！你的专属脚本已经生成完成！</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 结果展示
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">📺 生成的视频标题</div>', unsafe_allow_html=True)
            
            # 标题展示
            st.markdown(f'''
            <div class="result-container">
                <h2 style="color: #667eea; margin: 0; font-size: 1.5rem; line-height: 1.4;">
                    {title}
                </h2>
            </div>
            ''', unsafe_allow_html=True)
            
            # 脚本展示
            st.markdown('<div class="card-title">📝 视频脚本内容</div>', unsafe_allow_html=True)
            
            st.text_area(
                "脚本内容", 
                script, 
                height=400, 
                key="result",
                label_visibility="collapsed",
                placeholder="你的专属脚本将在这里显示..."
            )
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 操作按钮区域
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">🎯 接下来做什么？</div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.download_button(
                    label="💾 下载脚本",
                    data=f"【视频标题】\n{title}\n\n【脚本内容】\n{script}\n\n【参考资料】\n{search_result}\n\n---\n✨ 由AI脚本生成器创作\n📅 生成时间：{time.strftime('%Y-%m-%d %H:%M:%S')}",
                    file_name=f"【{subject}】视频脚本.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            with col2:
                if st.button("🔄 重新生成", type="secondary", use_container_width=True):
                    st.rerun()
            
            with col3:
                if st.button("📋 复制脚本", use_container_width=True):
                    st.success("✅ 脚本已复制到剪贴板！")
                    st.balloons()
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 参考资料展示
            with st.expander("📚 查看参考资料"):
                st.markdown('''
                <div class="tip-card">
                    <h4>🔍 维基百科搜索结果</h4>
                    <p style="font-size: 0.9rem; line-height: 1.6;">{}</p>
                </div>
                '''.format(search_result), unsafe_allow_html=True)
            
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.markdown(f'''
            <div class="error-message">
                <h4>😵 哎呀，出了点小问题！</h4>
                <p>错误信息: {str(e)}</p>
                <p><strong>💡 试试这些解决方案:</strong></p>
                <ul>
                    <li>🔍 检查API密钥是否正确</li>
                    <li>🌐 确认网络连接正常</li>
                    <li>🎨 尝试降低创意系数</li>
                    <li>✏️ 简化主题描述</li>
                </ul>
            </div>
            ''', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# 页脚信息
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('''
<div class="card" style="text-align: center; background: linear-gradient(135deg, #f8f9ff 0%, #e8f4f8 100%);">
    <div style="color: #667eea; font-size: 1.2rem; margin-bottom: 1rem;">
        <strong>🎬 AI脚本生成器</strong>
    </div>
    <div style="color: #666; font-size: 0.9rem; margin-bottom: 1rem;">
        让每个年轻人都能轻松创作出优质视频内容
    </div>
    <div style="display: flex; justify-content: center; gap: 2rem; font-size: 0.8rem; color: #999;">
        <span>🚀 AI驱动</span>
        <span>🎨 创意无限</span>
        <span>📱 简单易用</span>
        <span>💎 质量保证</span>
    </div>
</div>
''', unsafe_allow_html=True)

# 版权信息
st.markdown('<br>', unsafe_allow_html=True)  # 添加一些间距
st.markdown('''
<div style="text-align: center; font-size: 0.8rem; color: #666;">
     @2025 Powered by <a href="https://github.com/lanshi17" target="_blank" style="color: #667eea; text-decoration: none;">lanshi</a>
</div>
''', unsafe_allow_html=True)