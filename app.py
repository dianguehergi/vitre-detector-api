from flask import Flask, request, jsonify, render_template_string
import os
import torch

app = Flask(__name__)

# -------------------------
# Chargement du modèle AU DÉMARRAGE
# -------------------------
MODEL_PATH = "best_model.pt"

model = None
model_status = "not_loaded"

try:
    model = torch.load(MODEL_PATH, map_location="cpu")
    model.eval()
    model_status = "loaded"
    print("✅ Modèle chargé avec succès")
except Exception as e:
    model_status = f"error: {e}"
    print("❌ Erreur chargement modèle :", e)

# -------------------------
# Page d'accueil (test)
# -------------------------
@app.route("/", methods=["GET"])
def home():
    return render_template_string(f"""
    <h2>API Vitre Detector</h2>
    <p><b>Model status:</b> {model_status}</p>

    <form action="/predict" method="post" enctype="multipart/form-data">
        <input type="file" name="image" accept="image/*" required>
        <br><br>
        <button type="submit">Envoyer l'image</button>
    </form>
    """)

# -------------------------
# Endpoint /predict (SANS ML)
# -------------------------
@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({
            "error": "Modèle non chargé",
            "model_status": model_status
        }), 500

    if "image" not in request.files:
        return jsonify({"error": "Aucune image envoyée"}), 400

    image_file = request.files["image"]

    return jsonify({
        "message": "Image reçue avec succès",
        "filename": image_file.filename,
        "model_status": model_status,
        "status": "model_ready"
    })

# -------------------------
# Lancement Flask (Azure)
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
