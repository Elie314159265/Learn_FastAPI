# FastAPI 学習リポジトリ
本リポジトリはFastAPIの学習記録と演習コードを管理するためのリポジトリです。

# ディレクトリ構成例
```bash
.
├── (日付)/     #学習記録
├── app/    # FastAPI アプリケーション
│   ├── main.py
│   └── ...
├── requirements.txt    # 依存パッケージ一覧
├── README.md
└── .gitignore

```
# .gitignore設定例
```gitignore
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
env/
venv/
.env

# Logs
*.log

```

# 必要パッケージのインストール
```bash
$ pip install -r requirements.txt
```

# Git操作例
```bash
$ git branch
$ git checkout main
$ git pull origin main --rebase
$ git add .
$ git commit -m "学習記録を追加"
$ git push origin main
```
