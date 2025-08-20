# 2025/08 COPLI-NEXT 自分のパソコンで生成AIが動く！オリジナルチャットシステムの作り方を学んでみよう & ミニハンズオン

## 事前準備
各OS毎に事前準備が必要になりますので、なるべく準備をお願いしています

- [Windows](./docs/preparation_windows.md)
- [MacOS](./docs/preparation_mac.md)

不明点がありましたらconnpassの `イベントへのお問い合わせ` よりお問い合わせください

## サンプルコード起動手順

### Visual Studio Codeを起動する
#### Windowsの場合
スタートメニューもしくはWinキーを押し、 `code` と入力してVisualStudioCodeを起動します

#### Macの場合
LaunchPadもしくはCommand + スペースを押し、 `code` と入力してVisualStudioCodeを起動します

### [最初の1回のみ] リポジトリをcloneする
VisualStudioCodeのメニューバーから、 `View` > `Command Palette...` をクリックし、 `Git: Clone` と入力します

URLを入れる入力ボックスが表示されるので、以下のURLを入力します

`https://github.com/garicchi/llm-handson-202508`

`Clone from URL` というボタンが表示されるので、クリックします

フォルダの選択ダイアログが出るので、サンプルコードを保存したいフォルダを選択します

`Would you like to open cloned repository? ` と聞かれたら、 `Open` を押してください

### [最初の1回のみ] venvを作ってライブラリをインストールする
VisualStudioCodeのメニューバーから、 `Terminal` > `New Terminal` をクリックしてターミナルを開きます

#### Windowsの場合
以下を入力してENTERを押します
```
python ./cli/setup.py
```

#### Macの場合
以下を入力してENTERを押します

```
python3 ./cli/setup.py
```

※ この手順では、Macの場合、 `python3` なので注意してください

### [VSCodeを起動するたび] venvを起動する

#### Windowsの場合
以下を入力してENTERを押します
```
Set-ExecutionPolicy RemoteSigned -Scope Process
```
```
./venv/Scripts/activate
```

ターミナルの左端に `(venv)` と表示されればOKです

#### Macの場合
以下を入力してENTERを押します
```
source ./venv/bin/activate
```

ターミナルの左端に `(venv)` と表示されればOKです

### 01_basic.pyを起動する

以下を入力してENTERを押します
```
python ./samples/01_basic.py
```

エラーなく起動すればOKです
