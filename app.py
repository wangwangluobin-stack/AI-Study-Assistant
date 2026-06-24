import streamlit as st

from deepseek_api import (
    ask_ai,
    ask_ai_with_history,
    ask_with_document,
    summarize_text,
    generate_exam_questions
    
)

from pdf_reader import read_pdf
from word_reader import read_word


# =========================
# 页面配置
# =========================

st.set_page_config(
    page_title="AI学习助手",
    page_icon="📚",
    layout="wide"
)

# =========================
# Session 初始化
# =========================

if "chats" not in st.session_state:

    st.session_state.chats = {
        "默认对话": []
    }

if "current_chat" not in st.session_state:

    st.session_state.current_chat = "默认对话"

if "knowledge_base" not in st.session_state:
    st.session_state.knowledge_base = ""

if "document_names" not in st.session_state:
    st.session_state.document_names = []

st.title("📚 AI学习助手 V2.4")
with st.sidebar:

    st.header("💬 对话管理")

    new_chat_name = st.text_input(
        "新建对话名称"
    )

    if st.button("➕ 创建对话"):

        if (
            new_chat_name
            and new_chat_name
            not in st.session_state.chats
        ):

            st.session_state.chats[
                new_chat_name
            ] = []

            st.session_state.current_chat = (
                new_chat_name
            )

            st.rerun()

    selected_chat = st.radio(
        "选择对话",
        list(st.session_state.chats.keys())
    )

    st.session_state.current_chat = (
        selected_chat
    )




# =========================
# 顶部按钮
# =========================

col1, col2 = st.columns(2)

with col1:

    if st.button("🗑️ 清空聊天记录"):

        st.session_state.chats[
    st.session_state.current_chat
] = []
        st.session_state.knowledge_base = ""
        st.session_state.document_names = []

        st.rerun()

with col2:

    chat_text = "AI学习助手聊天记录\n\n"

    for msg in st.session_state.chats[
    st.session_state.current_chat
]:

        role = "用户" if msg["role"] == "user" else "AI"

        chat_text += f"{role}：\n"
        chat_text += msg["content"]
        chat_text += "\n\n"
        chat_text += "=" * 40
        chat_text += "\n\n"

    st.download_button(
        label="📥 导出聊天记录",
        data=chat_text,
        file_name="chat_history.txt",
        mime="text/plain"
    )


# =========================
# 文件上传
# =========================

st.divider()

st.subheader("📄 多文档知识库")

uploaded_files = st.file_uploader(
    "上传PDF或Word资料",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

if uploaded_files:

    all_text = ""
    file_names = []

    with st.spinner("正在加载资料..."):

        for file in uploaded_files:

            try:

                file_name = file.name.lower()

                if file_name.endswith(".pdf"):

                    text = read_pdf(file)

                elif file_name.endswith(".docx"):

                    text = read_word(file)

                else:

                    text = ""

                all_text += f"\n\n===== {file.name} =====\n\n"
                all_text += text

                file_names.append(file.name)

            except Exception as e:

                st.error(
                    f"{file.name} 读取失败：{e}"
                )

    st.session_state.knowledge_base = all_text
    st.session_state.document_names = file_names

    st.success(
        f"成功加载 {len(file_names)} 个文件"
    )


# =========================
# 显示知识库状态
# =========================

if st.session_state.document_names:

    st.info(
        "📚 当前知识库：\n\n"
        + "\n".join(st.session_state.document_names)
    )


# =========================
# AI聊天模块
# =========================

st.divider()

st.subheader("🤖 AI问答")
st.caption(
    f"当前对话：{st.session_state.current_chat}"
)

messages = st.session_state.chats[
    st.session_state.current_chat
]

for message in messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


prompt = st.chat_input(
    "请输入你的问题..."
)

if prompt:

    st.session_state.chats[
        st.session_state.current_chat
    ].append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("AI思考中..."):

            if st.session_state.knowledge_base:

                answer = ask_with_document(
                    prompt,
                    st.session_state.knowledge_base
                )

            else:

                current_messages = st.session_state.chats[
                    st.session_state.current_chat
                ]

                history = current_messages[-10:]

                answer = ask_ai_with_history(
                    history
                )

            st.markdown(answer)

    st.session_state.chats[
        st.session_state.current_chat
    ].append(
        {
            "role": "assistant",
            "content": answer
        }
    )

# =========================
# 学习资料分析
# =========================

if st.session_state.knowledge_base:

    st.divider()

    st.subheader("📚 学习资料智能分析")

    if st.button("开始分析"):

        with st.spinner("AI分析中..."):

            result = summarize_text(
                st.session_state.knowledge_base
            )

            st.markdown("### 分析结果")

            st.write(result)


# =========================
# AI考试预测
# =========================

if st.session_state.knowledge_base:

    st.divider()

    st.subheader("📝 AI智能错题本生成")

    if st.button("生成考试预测"):

        with st.spinner("AI正在分析考点..."):

            exam_result = generate_exam_questions(
                st.session_state.knowledge_base
            )

            st.markdown(exam_result)