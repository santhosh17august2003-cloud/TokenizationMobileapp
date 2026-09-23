import os
import flet as ft
import flet.fastapi as flet_fastapi

if not hasattr(ft, "ElevatedButton") and hasattr(ft, "FilledButton"):
    ft.ElevatedButton = ft.FilledButton

from ui.main_page import build_main_page

# FastAPI app for deployment on Render, Railway, or Heroku
app = flet_fastapi.app(build_main_page)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    # Run locally as web app
    ft.run(
        build_main_page,
        view=ft.AppView.WEB_BROWSER,
        host="0.0.0.0",
        port=port,
    )
