import os

import pytest
from pathlib import Path
from fastapi import FastAPI, APIRouter
from fastapi.testclient import TestClient



@pytest.fixture(scope="function")
def client_app(monkeypatch):
    # Set the base content root path to the directory containing your FastAPI app module
    content_root_path = Path(__file__).parent.parent.resolve()
    # from main.routes import router
    # Create a FastAPI app instance
    app = FastAPI()
    # Modify the app's content root path
    monkeypatch.setattr(app, "root_path", str(content_root_path))
    from main.routes import router
    app.include_router(router)

    return app
