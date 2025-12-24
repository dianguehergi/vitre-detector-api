from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# -------------------------
# Route de santé (déjà OK)
# -------------------------
@app.route("/", methods=["GET"])
def health():
    return jsonify({
        "message": "L'API du détecteur Vitre est en cours d'exécution",
        "status": "ok"
    })


# -------------------------
# NOUVEL ENDPOINT /predict
# -------------------------
@app.route("/predict", methods=["POST"])
def predict():
    # Vérifier qu'un fichier est bien envoyé
    if "image" not in request.files:
        return jsonify({
            "error": "Aucune image envoyée. Utilisez le champ 'image'."
        }), 400

    image_file = request.files["image"]

    # Vérifier que le fichier a un nom
    if image_file.filename == "":
        return jsonify({
            "error": "Nom de fichier vide."
        }), 400

    # (Pour l’instant) on ne traite pas l’image
    # On confirme juste la réception
    return jsonify({
        "message": "Image reçue avec succès",
        "filename": image_file.filename,
        "status": "ready_for_model"
    })


# -------------------------
# Lancement Flask (AZURE)
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
