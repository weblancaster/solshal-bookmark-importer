"""
Solshal bookmark importer service
"""
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/import/chrome", methods=["POST"])
def chrome_importer():
    """Get data in the request and pass to formatter
    then return formatted data to Solshal
    
    Decorators:
        app
    
    Returns:
        [Dict] -- Formatted collection for Solshal
    """

    data = request.get_json()["data"]
    formattedData = format_data(data)

    return jsonify({
        "data": formattedData
    })

def format_data(data):
    return data

if __name__ == "__main__":
    HOST = "0.0.0.0"
    PORT = os.getenv("PORT", 5001)
    app.run(
        host=HOST,
        port=PORT
    )

