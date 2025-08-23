#
# 06_manage_memory.py
# LLMと会話をするときに、会話履歴を表示する
# 数字キーを押すと、その記憶を消去できるサンプル
#

from typing import List
from langchain_openai import ChatOpenAI
from foundry_local import FoundryLocalManager
from langchain_core.prompts import ChatPromptTemplate
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

# システムプロンプトのテンプレートを定義
system_prompt_template = ChatPromptTemplate.from_messages([
    ('system', 'あなたは日本語で回答するAIアシスタントです。マイクという名前で会話してください')
])
# システムプロンプトを生成
system_prompt = system_prompt_template.invoke({})
# 会話履歴にシステムプロンプトを追加
chat_histories.extend(system_prompt.to_messages())

# 会話履歴を表示する関数
def print_histories():
    print('\n\n### 会話履歴 ###')
    for i, history in enumerate(chat_histories):
        print(f'[{i}] {history.type} {history.content}')
    print('################\n\n')

# 会話ループ
while True:
    # 履歴を表示
    print_histories()

    # ユーザー入力を取得
    user_input = input('入力してください(qキーで終了、数字で記憶消去) > ')

    # qキーを押したら終了
    if user_input.lower() == 'q':
        print('終了します')
        break

    # 数字なら、その記憶を消去
    if user_input.isdigit():
        selected_number = int(user_input)
        history = chat_histories[selected_number]
        print(f'[{selected_number}]の記憶を消します')
        chat_histories.remove(history)
        continue

    print(f'[ユーザー]: {user_input}')

    print('回答を生成しています...')

    # 会話履歴を含めたプロンプトテンプレートを定義
    prompt_template = ChatPromptTemplate.from_messages(
        # 会話履歴
        chat_histories
        # ユーザー入力
        + [('user', '{user_input_data}')]
    )

    # プロンプトを生成
    prompt = prompt_template.invoke({
        'user_input_data': user_input
    })

    # 回答を生成
    assistant_output = llm.invoke(prompt)

    print(f'[アシスタント]: {assistant_output.content}')

    # 会話履歴に追加
    chat_histories.extend([
        # 最後のユーザー入力
        prompt.to_messages()[-1],
        # アシスタントの回答
        assistant_output
    ])

