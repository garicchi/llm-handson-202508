#
# 05_rag_advance.py
# RAGを利用して外部知識を取り入れた会話をするサンプル
# 知識はmarkdownで記載されたものを分割し、
# 類似度が高いものをプロンプトに入れる
#

from langchain_openai import ChatOpenAI
from foundry_local import FoundryLocalManager
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import MarkdownHeaderTextSplitter

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

# 文章の類似度を計算する関数
#   text1を2文字ずつ区切って、text2の中に含まれる数を類似度とする
def calc_similarity(text1: str, text2: str) -> int:
    chunk_char_count = 2
    chunked_list = [''.join(text1[i:i+chunk_char_count]) for i in range(0, len(text1), chunk_char_count)]
    score = sum(1 for chunk in chunked_list if chunk in text2)
    return score

# RAGの知識 (markdown形式)
knowledge = '''
## バナナシステムとは
バナナシステムとは、USB接続されたバナナを使って他者と通話するシステムです

## りんごシステムとは
りんごシステムとは、USB接続されたりんごを使って他者と通話するシステムです
'''

# markdownのテキストを分割するTextSplitter
text_splitter = MarkdownHeaderTextSplitter([
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3")
])

# RAGの知識テキストを分割
splitted_texts = text_splitter.split_text(knowledge)

# ユーザー入力を取得
user_input = input('入力してください > ')

print(f'[ユーザー]: {user_input}')

print('回答を生成しています...')

# プロンプトを定義
prompt_template = ChatPromptTemplate.from_messages([
    ('system', '''
     あなたは日本語で回答するAIアシスタントです。名前はマイクです
     {rag_knowledge}
     '''),
    ('user', '{user_input_data}')
])

# 分割したテキストの中から、ユーザー入力に最も類似したものを選択
target_knowledge = max(
    splitted_texts, 
    key=lambda x: calc_similarity(user_input, x.page_content)
)

# プロンプトに知識とユーザー入力値を埋め込む
prompt = prompt_template.invoke({
    'rag_knowledge': target_knowledge.page_content,
    'user_input_data': user_input
})

# 回答を生成
assistant_output = llm.invoke(prompt)

print(f'[アシスタント]: {assistant_output.content}')