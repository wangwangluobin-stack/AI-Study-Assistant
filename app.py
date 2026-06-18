import streamlit as st

from deepseek_api import ask_ai
from deepseek_api import summarize_text

from pdf_reader import read_pdf
from word_reader import read_word


st.set_page_config(
    page_title="AI学习助手",
    page_icon="📚",
    layout="wide"
)

st.title("📚 AI学习助手 V1.3")

# =========================
# 聊天记录初始化
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================
# 清空聊天
# =========================

if st.button("🗑️ 清空聊天记录"):
    st.session_state.messages = []
    st.rerun()


# =========================
# AI聊天模块
# =========================

st.subheader("🤖 AI问答")

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


prompt = st.chat_input("请输入你的问题...")


if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("AI思考中..."):

            answer = ask_ai(prompt)

            st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


# =========================
# 学习资料分析
# =========================

st.divider()

st.subheader("📄 学习资料智能分析")

uploaded_file = st.file_uploader(
    "上传学习资料",
    type=["pdf", "docx"]
)

if uploaded_file:

    st.success(f"已上传：{uploaded_file.name}")

    if st.button("开始分析"):

        with st.spinner("AI分析中..."):

            file_name = uploaded_file.name.lower()

            text = ""

            if file_name.endswith(".pdf"):

                text = read_pdf(uploaded_file)

            elif file_name.endswith(".docx"):

                text = read_word(uploaded_file)

            result = summarize_text(text)

            st.markdown("## 📚 分析结果")

            st.write(result)

            