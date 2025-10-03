import os 
from flask import Flask

def create_app() -> Flask:
    app = Flask(__name__)

    @app.post("/search")
    def search_end_point():
        return "Hello World"
    
    return app

app = create_app()

if __name__ == "__main__":  # pragma: no cover
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)