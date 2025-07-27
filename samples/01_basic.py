import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from foundry_local import FoundryLocalManager

model_alias = "phi-4-mini"

print('llmを初期化しています...')

manager = FoundryLocalManager(model_alias)

llm = ChatOpenAI(
    model=manager.get_model_info(model_alias).id,
    base_url=manager.endpoint,
    api_key=manager.api_key,
    temperature=0.6,
    streaming=False
)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "あなたの名前はマイクです。日本語で回答を行います。"
    ),
    ("human", "{input}")
])

chain = prompt | llm

input = input("入力してください > ")

print(f'[ユーザー]: {input}')
print('回答を生成しています...')

output_message = chain.invoke({
    "input": input
})


print(f"[アシスタント]: {output_message.content}")