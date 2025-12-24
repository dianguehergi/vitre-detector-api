from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(__name__)

# -------------------------
# Page d'accueil (test)
# -------------------------
@app.route("/", methods=["GET"])
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test API Vitre Detector</title>
    </head>
    <body>
        <h2>Test API /predict</h2>

        <form action="/predict" method="post" enctype="multipart/form-data">
            <input type="file" name="image" accept="image/*" required>
            <br><br>
            <button type="submit">Envoyer l'image</button>
        </form>

        <p>Après l'envoi, la réponse JSON s'affichera.</p>
    </body>
    </html>
    """)

# -------------------------
# Endpoint /predict
# -------------------------
@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "Aucune image envoyée"}), 400

    image_file = request.files["image"]

    if image_file.filename == "":
        return jsonify({"error": "Nom de fichier vide"}), 400

    return jsonify({
        "message": "Image reçue avec succès",
        "filename": image_file.filename,
        "status": "ready_for_model"
    })

# -------------------------
# Lancement Flask (Azure)
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
