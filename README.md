# セットアップガイド
## 必要条件
- Python 3.11以上
- Poetry（Pythonパッケージマネージャー）

## インストール手順
### 1. リポジトリのクローン
```shell
git clone https://github.com/ruis2615/AutoThumbnailGenerator.git
cd AutoThumbnailGenerator
```

### 2. Poetry環境のセットアップ
```shell
poetry install
```
これにより、以下の依存関係がインストールされます（pyproject.toml参照）
- opencv-python
- python-dotenv

### 3. 環境変数の設定
`.env.sample`を同じディレクトリにコピーし、ファイル名を`.env`に変更後、以下の内容を設定してください。
```env
INPUT_DIRECTORY=/path/to/your/videos
OUTPUT_DIRECTORY=/path/to/save/thumbnails
EXTRACT_TIMES=20,2:30,3m,5m
```
- `INPUT_DIRECTORY`：動画ファイルが格納されているディレクトリのパス
- `OUTPUT_DIRECTORY`：サムネイル画像を保存するディレクトリのパス
- `EXTRACT_TIMES`：動画から抽出する時間を指定(フォーマットについては「カスタマイズ」をご覧ください)

### 4. 実行方法
Poetry環境内でスクリプトを実行：
```shell
poetry run python main.py
```

引数にJSONファイルを指定することで、複数のファイルごとに別々のフレームを指定して一括処理することができます。
```shell
poetry run python main.py data-sample.json
```

## 対応している動画フォーマット
```python
video_extensions = ('.mp4', '.avi', '.mov', '.mkv')
```

## 出力される画像について
- フォーマット：`JPG`
- ファイル名形式：`{動画名}_{タイムスタンプ}_time{秒数}s.jpg`
- デフォルトの抽出時間：20秒, 150秒, 180秒, 300秒

## カスタマイズ
### 1つのファイルのみの場合
抽出時間を変更する場合は、`env`の以下の部分を編集してください：
```env
EXTRACT_TIMES=20,2:30,3m,5m
```

### 複数のファイルごとに別々のフレームを指定したい場合
`data-sample.json`をコピーし、サンプルのJSON形式に従って書いてください。
その際、拡張子まで含めてください。

### 指定できるフォーマット
- `10` or `30` (秒数のみでの指定可能)
- `2:30` or `1:10:10` (`時:分:秒`のフォーマットで指定可能)
- `3s` or `3m` or `3h` (`s=秒`, `m=分`, `h=時`での指定も可能。ただし、`1h5m`といった組み合わせは不可)

## 注意事項
- poetry + pyenvの環境で構築しているため、その他の環境の場合は適宜コマンドを修正してください。
- 出力ディレクトリは自動的に作成されます。
- 指定した時間が動画の長さを超える場合は、そのフレームはスキップされます。

## ライセンス
MITライセンスの下で提供されています。詳細はLICENSEファイルを参照してください。
