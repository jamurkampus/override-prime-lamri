from flask import Flask, jsonify
import json, hashlib
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

app = Flask(__name__)

@app.route('/validate')
def validate():
    try:
        with open("public.pem", "rb") as key_file:
            public_key = serialization.load_pem_public_key(key_file.read())

        with open("verify.json", "r") as f:
            data = json.load(f)
        
        signature = bytes.fromhex(data["signed_checksum"])
        clone = data.copy()
        del clone["signed_checksum"]

        payload = json.dumps(clone, sort_keys=True).encode()
        public_key.verify(
            signature,
            hashlib.sha256(payload).digest(),
            padding.PKCS1v15(),
            hashes.SHA256()
        )

        return jsonify({
            "status": "VALID ✅",
            "identity": data["identity"],
            "node": data["node"],
            "function": data["function"],
            "checksum": data["checksum"],
            "timestamp": data["timestamp"]
        })
    except Exception as e:
        return jsonify({
            "status": "TIDAK VALID ❌",
            "error": str(e)
        }), 400
