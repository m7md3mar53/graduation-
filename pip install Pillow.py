from flask import Flask, request, send_file
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import io
import os

app = Flask(__name__)

def encrypt_image(image_bytes, key):
    # Use AES-GCM mode for encryption
    iv = os.urandom(12)  # Initialization vector
    cipher = Cipher(algorithms.AES(key.encode("utf-8")), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(image_bytes) + encryptor.finalize()
    return iv + encryptor.tag + ciphertext  # Return IV, tag, and ciphertext

def decrypt_image(encrypted_bytes, key):
    iv = encrypted_bytes[:12]
    tag = encrypted_bytes[12:28]
    ciphertext = encrypted_bytes[28:]
    cipher = Cipher(algorithms.AES(key.encode("utf-8")), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_bytes = decryptor.update(ciphertext) + decryptor.finalize()
    return decrypted_bytes

@app.route("/encrypt", methods=["POST"])
def encrypt():
    file = request.files["file"]
    key = request.form["key"]

    image_bytes = file.read()
    encrypted_image = encrypt_image(image_bytes, key)

    return send_file(
        io.BytesIO(encrypted_image),
        as_attachment=True,
        download_name="encrypted_image.bin",
        mimetype="application/octet-stream",
    )

@app.route("/decrypt", methods=["POST"])
def decrypt():
    file = request.files["file"]
    key = request.form["key"]

    encrypted_bytes = file.read()
    decrypted_image = decrypt_image(encrypted_bytes, key)

    return send_file(
        io.BytesIO(decrypted_image),
        as_attachment=False,
        download_name="decrypted_image.png",
        mimetype="image/png",
    )

if __name__ == "__main__":
    app.run(debug=True)
