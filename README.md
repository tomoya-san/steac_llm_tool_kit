# STEAC LLM ツールキット

## 準備

この手順は、リポジトリをクローン済みで、Python 3.12 以降がインストールされていることを前提としています。

### 仮想環境の作成

依存関係の管理や他プロジェクトとの競合を避けるため、仮想環境の利用を推奨します。プロジェクトのルートディレクトリで仮想環境を作成します。

```bash
python -m venv .venv
```

### 仮想環境の有効化

本プロジェクト関連のコマンドを実行する前に、必ず仮想環境を有効化してください。これにより、正しい Python インタプリタとパッケージが使用されます。

```bash
source .venv/bin/activate
```

### 依存パッケージのインストール

必要な Python パッケージをインストールしてください。

```bash
python -m pip install -r requirements.txt
```

### 環境変数の設定

プロジェクトのルートディレクトリに `.env` ファイルを作成し、OpenRouter の API キーを追加してください。フォーマットは `.env.example` を参照してください。API キーは [OpenRouter](https://openrouter.ai/) で無料登録して取得できます。

```plaintext
OPENROUTER_API_KEY=your_api_key_here
```

## 各ツールの使い方

### スクリプトと質問の分割

生のスクリプトファイルを `split_script_and_questions/input_data/raw_scripts/` ディレクトリにアップロードしてください。各スクリプトファイルには複数の質問を含めることができます。ファイルは拡張子が `.txt` のプレーンテキストである必要があります。

スクリプトを質問と回答に分割するには、以下のコマンドを実行します。出力ファイル名は任意です。

```bash
python split_script_and_questions/main.py <output_csv_filename>
```

### Punctuation 修正

`fix_punctuation/input_data/` ディレクトリに、修正したいテキストを `raw_asr_text` カラムに含む csv ファイル `[your_input_filename].csv` を作成してください。

ASR テキストの句読点を LLM で修正するには、以下のコマンドを実行します。ファイル名はパスを含めず、ファイル名のみ指定してください。出力ファイル名は任意です。

```bash
python fix_punctuation/main.py <input_csv_filename> <output_csv_filename>
```

出力は `fix_punctuation/out/` ディレクトリに、`gpt_fixed_text` カラムが追加された csv ファイルとして保存されます。

### テキスト比較

`compare_text/input_data/` ディレクトリに、比較したいテキストを `original_text` と `fixed_text` カラムに含む csv ファイル `[your_input_filename].csv` を作成してください。

2 つのテキストを比較し、変更点の要約を生成するには、以下のコマンドを実行します。ファイル名はパスを含めず、ファイル名のみ指定してください。出力ファイル名は任意です。

```bash
python compare_text/main.py <input_csv_filename> <output_csv_filename>
```

出力は `compare_text/out/` ディレクトリに、変更点を要約した `changes` カラムが追加された csv ファイルとして保存されます。

### 選択肢の抽出

`extract_choices/input_data/raw_scripts/` ディレクトリに、選択肢を含むスクリプトファイルをアップロードしてください。各ファイルはプレーンテキストで、ファイルの拡張子が `.txt` である必要があります。

選択肢を抽出するには、以下のコマンドを実行します。出力ファイル名は任意です。

```bash
python extract_choices/main.py <output_csv_filename>
```
