from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from foundry_local import FoundryLocalManager

# 使用するモデル名
model_alias = 'phi-4'
# 軽量版を使用する場合はこちらをコメントアウト
# model_alias = 'qwen2.5-0.5b'

manager = FoundryLocalManager()

# モデルがダウンロードされているか確認
if not [x for x in manager.list_cached_models() if x.alias == model_alias]:
    raise Exception(f'モデルがダウンロードされていません {model_alias}')

llm = ChatOpenAI(
    model=manager.get_model_info(model_alias).id,
    base_url=manager.endpoint,
    api_key=manager.api_key,
    temperature=0.6,
    streaming=False
)

input = input("入力してください > ")

print(f'[ユーザー]: {input}')
print('回答を生成しています...')

output_message = llm.invoke(input)

print(f"[アシスタント]: {output_message.content}")