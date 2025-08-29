# ハンズオン環境掃除方法 Mac版

## ダウンロードしたLLMモデルを削除する
ターミナルで以下を実行します

```sh
foundry cache remove '*' --all --yes
```

## Azure AI Foundry Localをアンインストールする
ターミナルで以下を実行します

```sh
brew rm foundrylocal
brew untap microsoft/foundrylocal
brew cleanup --scrub
```
