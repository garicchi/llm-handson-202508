#
# 03_conversation.py
# 会話履歴を保持し、LLMと複数ターンで会話するサンプル
# 会話履歴をプロンプトに入れることで記憶を保持できる
#

from typing import List
from langchain_openai import ChatOpenAI
from foundry_local import FoundryLocalManager
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import BaseMessage

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

# 会話履歴を保存するリスト
chat_histories: List[BaseMessage] = []

# プロンプトテンプレートを定義
prompt_template = ChatPromptTemplate.from_messages([
    # システムプロンプト
    ('system', 'あなたは日本語で回答するAIアシスタントです。マイクという名前で会話してください'),
    # 会話履歴が入る場所
    MessagesPlaceholder("history"),
    # ユーザー入力が入る場所
    ('user', '{user_input_data}')
])

# 会話ループ
while True:
    print()
    # ユーザー入力を取得
    user_input = input('入力してください(qキーで終了) > ')

    # qキーを押したら終了
    if user_input.lower() == 'q':
        print('終了します')
        break

    print(f'[ユーザー]: {user_input}')

    print('回答を生成しています...')

    # プロンプトを生成
    prompt = prompt_template.invoke({
        # 会話履歴を埋め込む
        'history': chat_histories,
        # ユーザー入力を埋め込む
        'user_input_data': user_input
    })

    # print(f'\n--プロンプト--\n{prompt.to_string()}\n------\n')

    # 回答を生成
    assistant_output = llm.invoke(prompt)

    print(f'[アシスタント]: {assistant_output.content}')

    # 会話履歴に追加
    chat_histories.extend([
        # 最後のユーザー入力
        [x for x in prompt.to_messages() if x.type == 'human'][-1],
        # アシスタントの回答
        assistant_output
    ])

