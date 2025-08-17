from langchain_openai import ChatOpenAI
from foundry_local import FoundryLocalManager
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage

# 使用するモデル名
model_alias = 'phi-4-mini'
# 軽量版を使用する場合はこちらをコメントアウト
# model_alias = 'qwen2.5-0.5b'

manager = FoundryLocalManager()

# モデルがダウンロードされているか確認
if not [x for x in manager.list_cached_models() if x.alias == model_alias]:
    raise Exception(f'モデルがダウンロードされていません {model_alias}')

# LLMの初期化
llm = ChatOpenAI(
    model=manager.get_model_info(model_alias).id,
    base_url=manager.endpoint,
    api_key=manager.api_key
)

# ユーザー入力を取得
user_input = input('入力してください > ')

print(f'[ユーザー]: {user_input}')

print('回答を生成しています...')

# プロンプトテンプレートを定義
prompt_template = ChatPromptTemplate.from_messages([
    # システムプロンプト
    ('system', 'あなたは日本語で回答するAIアシスタントです。名前はマイクです'),
    # ユーザープロンプト
    ('user', '{user_input_data}')
])

# プロンプトにユーザー入力値を埋め込んでプロンプトを生成
prompt = prompt_template.invoke({
    # {user_input_data}の部分を置き換える
    'user_input_data': user_input
})

# 回答を生成
assistant_output = llm.invoke(prompt)

print(f'[アシスタント]: {assistant_output.content}')