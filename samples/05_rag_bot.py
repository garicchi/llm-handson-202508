#
# 05_rag_advance.py
# RAGを利用して外部知識を取り入れた会話をするサンプル
# 知識はmarkdownで記載されたものを分割し、
# 類似度が高いものをプロンプトに入れる
#

from typing import List
from langchain_openai import ChatOpenAI
from foundry_local import FoundryLocalManager
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_core.messages import BaseMessage
from pathlib import Path

# 使用するモデル名
model_alias = 'phi-4-mini'
# 軽量版を使用する場合はこちらをコメントアウト
# model_alias = 'qwen2.5-0.5b'

# Trueの場合、LLMの出力をストリーミングで表示する
stream_output_mode = False

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

# RAGの知識をロード (markdown形式)
knowledge_path = Path(__file__).parent / 'knowledge.md'
knowledge: str = None
with open(knowledge_path, 'r', encoding='utf-8') as f:
    knowledge = f.read()

# 会話履歴を保存するリスト
chat_histories: List[BaseMessage] = []

# システムプロンプトのテンプレートを定義
system_prompt_template = ChatPromptTemplate.from_messages([
    ('system', '''
あなたは日本語で回答する料理のレシピアシスタントです
3ターンほどをいくつかの質問をしてから、レシピを提案してください。
レシピ情報の中の情報を含めて、提案してください

## レシピ情報の出力例
Q： 材料を表示
A: 材料: 
     * 牛薄切り肉: 200g
Q: 作り方を表示
A: 作り方:
     1. じゃがいもは1口大に切る

## レシピ情報
{rag_knowledge}
''')
])
# システムプロンプトを生成
system_prompt = system_prompt_template.invoke({
    'rag_knowledge': knowledge
})
# 会話履歴にシステムプロンプトを追加
chat_histories.extend(system_prompt.to_messages())

print('[アシスタント]: 料理のレシピについて何でも質問してください')

# LLMの出力をストリーミングでprintし、全文を返す関数
def print_stream(llm: ChatOpenAI, prompt: ChatPromptTemplate) -> str:
    output_text = ""
    for chunk in llm.stream(prompt):
        print(chunk.content, end='', flush=True)
        output_text += chunk.content
    print()
    return output_text

# 会話ループ
while True:
    # ユーザー入力を取得
    print()
    user_input = input('入力してください(qキーで終了) > ')

    # qキーを押したら終了
    if user_input.lower() == 'q':
        print('終了します')
        break

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
    assistant_output = ''
    if stream_output_mode:
        assistant_output = print_stream(llm, prompt)
    else:
        assistant_output = llm.invoke(prompt).content
        print(assistant_output)

    # 会話履歴に追加
    chat_histories.extend([
        # 最後のユーザー入力
        prompt.to_messages()[-1],
        # アシスタントの回答
        assistant_output
    ])