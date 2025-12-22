from flask import Flask, request, jsonify
import torch
from PIL import Image
import io
import base64
import os

# --------------------
# Initialisation Flask
# --------------------
app = Flask(__name__)

# --------------------
# Chargement du modèle
# --------------------
MODEL_PATH = "best_model.pt"

try:
    model = torch.load(MODEL_PATH, map_location="cpu")
    model.eval()
    print("✅ Modèle chargé avec succès")
except Exception as e:
    print("❌ Erreur lors du chargement du modèle :", e)
    model = None

# --------------------
# Route racine (test)
# --------------------
@app.route("/", methods=["GET"])
def home():
    return "API vitre-detector OK"

# --------------------
# Route prédiction (API)
# --------------------
@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Modèle non chargé"}), 500

    try:
        data = request.json

        if data is None or "image" not in data:
            return jsonify({"error": "Image manquante"}), 400

        # Décodage image base64
        image_bytes = base64.b64decode(data["image"])
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # ⚠️ Pour l’instant, on ne fait PAS l’inférence
        # (on valide d’abord que l’API fonctionne)
        return jsonify({
            "status": "success",
            "message": "Image reçue, API fonctionnelle"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --------------------
# Lancement serveur
# --------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
