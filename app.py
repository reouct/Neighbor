import os
from flask import Flask, request, jsonify, Response
import json

from search import validate_request, compute_results


def create_app() -> Flask:
    app = Flask(__name__)

    @app.post("/search")
    def search_endpoint():
        try:
            payload = request.get_json(force=True, silent=False)
        except Exception:
            return jsonify({"error": "Invalid or missing JSON body"}), 400
        try:
            vehicles = validate_request(payload)
            results = compute_results(vehicles)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        payload = results
        body = json.dumps(payload, ensure_ascii=False, sort_keys=False)
        return Response(body, mimetype="application/json")

    @app.errorhandler(404)
    def not_found(_: Exception):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(500)
    def server_error(e: Exception):
        return jsonify({"error": "Server error", "detail": str(e)}), 500

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
