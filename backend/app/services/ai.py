"""
AI 服务
封装 DeepSeek API 调用，提供问答能力
"""

from openai import OpenAI
from app.config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL

# 创建 OpenAI 客户端，指向 DeepSeek 的服务器地址
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL,
)


def ask_ai(
    pdf_text: str,
    question: str,
    history: list[dict] | None = None,
) -> str:
    """将 PDF 文本、历史对话和用户问题发送给 DeepSeek，返回 AI 的回答

    参数:
        pdf_text: 已提取的 PDF 文本内容
        question: 用户当前的问题
        history:  之前的对话记录，格式 [{"role":"user","content":"..."},
                                          {"role":"assistant","content":"..."}]
    """

    system_prompt = """# 身份
你是一位资深的考研辅导老师，擅长帮助考生理解知识点、梳理解题思路、制定复习策略。
你的回答风格专业、清晰、有耐心，像一位老师在给考研学生讲解。

# 核心规则：如何对待资料与知识
1. 优先使用提供的资料内容回答问题。如果资料中有直接相关的定义、公式、例题，以此为准。
2. 如果资料内容不完整或缺失，你可以用自己的知识进行补充，但必须：
   - 在内容末尾标注 【来自资料】或【来自模型补充知识】
   - 【来自资料】= 资料中明确包含的内容
   - 【来自模型补充知识】= 资料中没有、但你知道的标准知识点
3. 如果用户的问题与资料完全无关，先回答资料范围内的部分，再补充你的知识。

# 回答风格
- 先给出简洁的核心答案，再展开详细讲解
- 涉及计算的题目，分步骤展示解题过程
- 重要的定义、公式使用清晰格式突出显示
- 可以用表格对比相似概念
- 可以在回答末尾给出 1-2 条复习建议或记忆技巧

# 禁止事项
- 严禁编造资料中不存在的数据、人名、年份、引用
- 不要假装资料中有某段内容——不确定时诚实说"资料未提供此信息"
- 不要用模糊表述（如"从前有个定理"），给出具体的定理名称和条件
- 不要一次输出过多内容，聚焦在用户问的问题上"""

    # 构建消息列表：system + 历史对话 + PDF上下文 + 新问题
    messages = [{"role": "system", "content": system_prompt}]

    # 如果有历史对话，先追加历史
    if history:
        for msg in history:
            messages.append({"role": msg["role"], "content": msg["content"]})

    # 最后追加包含 PDF 上下文和当前问题的 user 消息
    user_prompt = f"""## 考研资料内容
以下是用户上传的考研资料中检索到的相关内容：

---
{pdf_text}
---

## 用户提问
{question}

## 回答要求
1. 先判断资料中是否包含与问题相关的内容
2. 优先基于资料回答，资料不足时用自己的知识补充
3. 回答末尾用括号标注信息来源
4. 如果涉及公式或计算，请分步骤展示"""

    messages.append({"role": "user", "content": user_prompt})

    # ---- 调试日志：最终发送给 LLM 的 Prompt ----
    print(f"\n{'='*60}")
    print(f"[LLM] 即将发送给 DeepSeek 的消息 ({len(messages)} 条):")
    for i, msg in enumerate(messages):
        role = msg["role"]
        content = msg["content"]
        # 截断过长的内容，只打前 300 和后 100 字符
        if len(content) > 500:
            preview = content[:300] + f"\n... [省略 {len(content)-400} 字符] ...\n" + content[-100:]
        else:
            preview = content
        print(f"  [{i+1}] role={role}, 长度={len(content)} 字符")
        print(f"      内容: {preview}")
        print()
    print(f"{'='*60}\n")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        temperature=0.3,
        max_tokens=3000,
    )

    return response.choices[0].message.content or ""
