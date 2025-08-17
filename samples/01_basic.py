from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from foundry_local import FoundryLocalManager

# 使用するモデル名
model_alias = 'phi-4-mini'
# 軽量版を使用する場合はこちらをコメントアウト
# model_alias = 'qwen2.5-0.5b'

manager = FoundryLocalManager()

# モデルがダウンロードされているか確認
if not [x for x in manager.list_cached_models() if x.alias == model_alias]:
    raise Exception(f'モデルがダウンロードされていません {model_alias}')

llm = ChatOpenAI(
    model=manager.get_model_info(model_alias).id,
    base_url=manager.endpoint,
    api_key=manager.api_key
)

# ユーザー入力を待機
user_input = input("入力してください > ")

print(f'[ユーザー]: {user_input}')

print('回答を生成しています...')

# LLMから回答を取得
assistant_output = llm.invoke(user_input)

# 回答を出力
print(f"[アシスタント]: {assistant_output.content}")