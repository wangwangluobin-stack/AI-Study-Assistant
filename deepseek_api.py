from openai import OpenAI

client = OpenAI(
    api_key="sk-a1a8e85324c94084b290e258ad6f1eaf",
    base_url="https://api.deepseek.com"
)

def ask_ai(question):

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response.choices[0].message.content


def summarize_text(text):

    prompt = f"""
请总结下面学习资料。

要求：

1. 核心知识点
2. 重点内容
3. 考试高频考点
4. 简洁明了

资料内容：

{text[:12000]}
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