import time
import streamlit as st

from src.utils.helpers import get_base64_image, normalize_query
from src.services.rag_service import setup_rag_chain

def show_loading_page():
    pepe_base64 = get_base64_image("public/static/image/pepe.gif")
    
    loading_html = f"""
    <style>
        .loading-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 80vh;
        }}
        .pepe-gif {{
            width: 150px;
            margin-bottom: 20px;
        }}
        .progress-bar {{
            width: 300px;
            height: 20px;
            background: #f0f0f0;
            border-radius: 10px;
            overflow: hidden;
            margin-top: 20px;
        }}
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #FF9900 0%, #FF6600 100%);
            animation: progress 2s ease-in-out;
        }}
        @keyframes progress {{
            from {{ width: 0%; }}
            to {{ width: 100%; }}
        }}
    </style>
    <div class="loading-container">
        <img src="data:image/gif;base64,{pepe_base64}" class="pepe-gif">
        <h2>Đang khởi động FCAJ Assistant...</h2>
        <div class="progress-bar">
            <div class="progress-fill"></div>
        </div>
    </div>
    """
    
    placeholder = st.empty()
    placeholder.markdown(loading_html, unsafe_allow_html=True)
    time.sleep(2)
    placeholder.empty()

def get_response(question: str) -> str:
    try:
        normalized = normalize_query(question)
        rag_chain = setup_rag_chain()
        
        if "messages" in st.session_state and len(st.session_state.messages) > 1:
            history = "\n".join([f"{msg['role'].upper()}: {msg['content']}" for msg in st.session_state.messages[:-1]])
            context_question = f"Lịch sử cuộc trò chuyện:\n{history}\n\nCâu hỏi hiện tại: {normalized}"
            return rag_chain.invoke(context_question)
        
        return rag_chain.invoke(normalized)
    except Exception as e:
        return f"⚠️ Lỗi: {str(e)}"

st.set_page_config(
    page_title="FCAJ Assistant",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://rules.fcjuni.com/",
        "About": "# FCAJ Chatbot v1.0",
    },
)

if "loaded" not in st.session_state:
    show_loading_page()
    st.session_state.loaded = True

if "user_avatar" not in st.session_state:
    st.session_state.user_avatar = "👤"
if "bot_avatar" not in st.session_state:
    st.session_state.bot_avatar = "🤖"

st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stSidebar {
        background-color: #0e1117;
    }
    .stMarkdown, .stText, p, span, div, label, h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    .stChatMessage {
        background-color: #1e1e1e !important;
        color: #ffffff !important;
    }
    .stChatMessage p, .stChatMessage span, .stChatMessage div {
        color: #ffffff !important;
    }
    .stButton > button {
        background-color: #262730 !important;
        color: #ffffff !important;
        border: 1px solid #444 !important;
    }
    .warning-box {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #c92a2a;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .warning-box p {
        color: white !important;
        margin: 0;
        font-weight: 600;
        font-size: 0.9em;
    }
</style>
""", unsafe_allow_html=True)

st.header("☁️ First Cloud AI Journey Assistant")
st.markdown(
    """
<div style='background: #0e1117; 
            padding: 10px; border-radius: 10px; margin-bottom: 20px;'>
    <p style='color: #ffffff; text-align: center; margin: 0; font-size: 1.1em; font-weight: bold;'>
        🚀 Chatbot hỗ trợ cộng đồng FCAJ - AWS Vietnam
    </p>
</div>
""",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### 📚 Tài nguyên FCAJ")
    st.markdown(
        """
    📜 [Quy định FCAJ](https://rules.fcjuni.com/)
    
    🎥 [Kênh YouTube](https://www.youtube.com/@AWSStudyGroup)
    
    📚 [Tài liệu học tập](https://cloudjourney.awsstudygroup.com/)
    """
    )

    st.markdown("---")
    st.markdown("### 🛠️ Công cụ")

    if st.button("🔄 Làm mới cuộc trò chuyện"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown(
        """
    <div style='text-align: center; color: #666; font-size: 0.8em;'>
    🚀 Powered by FCAJ Team<br>
    © 2026 First Cloud AI Journey
    </div>
    """,
        unsafe_allow_html=True,
    )
    
    st.markdown(
        """
    <div class='warning-box'>
        <p>⚠️ <b>Lưu ý quan trọng:</b></p>
        <p>Chatbot có thể mắc sai lầm. Vui lòng xem kỹ lại thông tin hoặc liên hệ đội admin để xác minh.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

if len(st.session_state.messages) == 0:
    with st.chat_message("assistant", avatar=st.session_state.bot_avatar):
        st.markdown(
            """
👋 Xin chào! Tôi là trợ lý AI của cộng đồng **First Cloud AI Journey (FCAJ)**.

Tôi có thể giúp bạn:
- 📚 Tìm hiểu về AWS và Cloud Computing
- 👥 Thông tin về FCAJ và đội admin
- 📊 Cách tính điểm và quy định chương trình
- ⚠️ Xử lý vi phạm và nội quy

Hãy thử các câu hỏi gợi ý bên dưới! 👇
        """
        )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("👥 Đội admin FCAJ gồm những ai?"):
            st.session_state.messages.append(
                {"role": "user", "content": "Đội admin FCAJ gồm những ai?"}
            )
            st.rerun()

        if st.button("📊 Cách tính điểm như thế nào?"):
            st.session_state.messages.append(
                {"role": "user", "content": "Cách tính điểm như thế nào?"}
            )
            st.rerun()

    with col2:
        if st.button("☁️ FCAJ là gì?"):
            st.session_state.messages.append({"role": "user", "content": "FCAJ là gì?"})
            st.rerun()

        if st.button("📝 Nội dung project là gì?"):
            st.session_state.messages.append(
                {"role": "user", "content": "Nội dung project là gì?"}
            )
            st.rerun()

for m in st.session_state.messages:
    avatar = st.session_state.user_avatar if m["role"] == "user" else st.session_state.bot_avatar
    with st.chat_message(m["role"], avatar=avatar):
        st.markdown(m["content"])

if len(st.session_state.messages) > 0:
    last_msg = st.session_state.messages[-1]
    if last_msg["role"] == "user":
        if (
            len(st.session_state.messages) == 1
            or st.session_state.messages[-2]["role"] == "assistant"
        ):
            with st.chat_message("assistant", avatar=st.session_state.bot_avatar):
                pepe_base64 = get_base64_image("public/static/image/pepe.gif")
                st.markdown(f'<img src="data:image/gif;base64,{pepe_base64}" width="30" style="display:inline; margin-right:10px;"><b>Đang tìm kiếm thông tin...</b>', unsafe_allow_html=True)
                answer = get_response(last_msg["content"])
                st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()

user_input = st.chat_input("Hỏi về AWS, FCAJ...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar=st.session_state.user_avatar):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar=st.session_state.bot_avatar):
        pepe_base64 = get_base64_image("public/static/image/pepe.gif")
        st.markdown(f'<img src="data:image/gif;base64,{pepe_base64}" width="30" style="display:inline; margin-right:10px;"><b>Đang tìm kiếm thông tin...</b>', unsafe_allow_html=True)
        answer = get_response(user_input)
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
