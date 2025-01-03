from src.main import create_app
from src.config import config_instance

if __name__ == "__main__":
    app = create_app(config_instance())
    app.run(host="0.0.0.0", debug=True, port=5000)
