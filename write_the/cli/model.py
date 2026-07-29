import typer
import requests
import json
from pathlib import Path


def get_config_path():
    APP_NAME = "write-the"
    app_dir = typer.get_app_dir(APP_NAME)
    config_path: Path = Path(app_dir) / "config.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    if not config_path.exists():
        with open(config_path, "w") as f:
            json.dump({}, f)
    return config_path

def get_default_model():
    config_path = get_config_path()
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        return config["default_model"]
    except Exception:
        return "gpt-3.5-turbo-instruct"

def set_default_model(model: str):
    config_path = get_config_path()
    config = {}
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except Exception:
        pass
    config["default_model"] = model
    with open(config_path, "w") as f:
        json.dump(config, f)

def fetch_openrouter_models(
        url: str = "https://openrouter.ai/api/v1/models",
        api_key: str | None = None,
        timeout: float = 30.0,
    ):
    """Fetch model metadata from OpenRouter and return a dict keyed by model ID."""
    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    response = requests.get(url, headers=headers, timeout=59)
    response.raise_for_status()

    payload = response.json()
    try:
        data = payload["data"]
    except KeyError as e:
        raise ValueError(f"Unexpected API response: missing 'data' key. Keys: {list(payload.keys())}") from e

    return {m["id"]: m for m in data if "id" in m}
