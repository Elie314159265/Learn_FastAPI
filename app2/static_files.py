from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

def setup_static_files(app: FastAPI):
    # templatesディレクトリを静的ファイルとしてマウント
    templates_path = Path(__file__).parent / "templates"
    if templates_path.exists():
        app.mount("/templates", StaticFiles(directory=templates_path), name="templates")
    
    # ルートパスでlogin.htmlを表示
    @app.get("/")
    async def read_login():
        return FileResponse(templates_path / "login.html")