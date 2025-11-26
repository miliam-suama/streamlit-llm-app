import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
# .env の読み込み
load_dotenv()


# LLM を呼び出す関数

def run_expert_llm(user_text: str, expert_type: str) -> str:
    """入力テキストと選択した専門家タイプをもとに LLM に回答させる"""

    # 専門家ごとの System Message
    expert_prompts = {
        "料理の専門家": "あなたはプロの料理研究家です。分かりやすく、実用的なアドバイスをしてください。",
        "英語学習の専門家": "あなたは英語学習のプロ講師です。初心者にも丁寧に説明してください。",
        "旅行プランナー": "あなたは経験豊富な旅行プランナーです。旅行計画に最適な提案をしてください。",
    }

    system_message = expert_prompts.get(expert_type, "あなたは有能なアシスタントです。")

    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=user_text),
    ]

    result = llm.invoke(messages)
    return result.content



# Streamlit UI

st.title("LLM × Expert Assistant")
st.write("選択した専門家の視点でアドバイスを返す AI アプリです。")
st.write("テキストを入力し、専門家タイプを選んでから送信してください。")

# 専門家タイプの選択
expert_type = st.radio(
    "専門家の種類を選んでください：",
    ["料理の専門家", "英語学習の専門家", "旅行プランナー"],
)

# ユーザー入力フォーム
user_input = st.text_area("質問や相談内容を入力してください：")

# 実行ボタン
if st.button("送信"):
    if user_input.strip() == "":
        st.warning("テキストを入力してください。")
    else:
        with st.spinner("AI が回答を生成中です..."):
            answer = run_expert_llm(user_input, expert_type)
        st.success("回答が生成されました！")
        st.write("### 🧠 AI の回答")
        st.write(answer)

# フッター
st.markdown("---")

