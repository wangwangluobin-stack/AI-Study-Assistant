from openai import OpenAI
from dotenv import load_dotenv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(BASE_DIR, ".env")

load_dotenv(env_path)

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

def ask_ai(question):

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": question}
        ]
    )

    return response.choices[0].message.content


def summarize_text(text):

    prompt = f"""
请总结下面学习资料：

{text[:12000]}
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

def generate_exam_questions(text):

    prompt = f"""
你是一名大学课程老师。

请根据下面学习资料生成：

1. 核心知识点总结（5条）

2. 高频考点（5条）

3. 预测选择题（5道）
格式：
题目
A.
B.
C.
D.
答案：

4. 预测简答题（3道）

5. 考前复习建议

资料：

{text[:12000]}
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    return response.choices[0].message.content

def ask_with_document(question, document_text):

    prompt = f"""
你是一名学习助手。

请严格根据下面资料回答问题。

资料：

{document_text[:10000]}

问题：

{question}

如果资料中没有相关内容，请明确说明。
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content