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
```
- `INPUT_DIRECTORY`：動画ファイルが格納されているディレクトリのパス
- `OUTPUT_DIRECTORY`：サムネイル画像を保存するディレクトリのパス

4. 実行方法
Poetry環境内でスクリプトを実行：
```shell
poetry run python main.py
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
抽出時間を変更する場合は、main.pyの以下の部分を編集してください：
```python
times_to_extract = [20.0, 150.0, 180.0, 300.0]  # 抽出したい時間（秒）のリスト
```

## 注意事項
- poetry + pyenvの環境で構築しているため、pip環境とはご自身でカスタマイズしてください。
- 出力ディレクトリは自動的に作成されます。
- 指定した時間が動画の長さを超える場合は、そのフレームはスキップされます。

## ライセンス
MITライセンスの下で提供されています。詳細はLICENSEファイルを参照してください。
