# ハンズオン環境掃除方法 Windows版 (書きかけ)

## ダウンロードしたLLMモデルを削除する
Powershellで以下を実行します

```sh
foundry cache remove '*' --all --yes
```

## Azure AI Foundry Localをアンインストールする
Powershellで下記コマンドを実行します

```
winget remove Microsoft.FoundryLocal
```