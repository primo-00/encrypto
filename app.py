from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS

# Cipher Functions (same as before)
def caesar_cipher(text, shift, decrypt=False):
    if decrypt:
        shift = -shift
    result = ""
    for char in text:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char
    return result

def vigenere_cipher(text, key, decrypt=False):
    key = key.lower()
    result = ""
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - 97
            if decrypt:
                shift = -shift
            shift_base = 65 if char.isupper() else 97
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
            key_index += 1
        else:
            result += char
    return result

def affine_cipher(text, a, b, decrypt=False):
    result = ""
    if decrypt:
        mod_inverse = pow(a, -1, 26)
        for char in text:
            if char.isalpha():
                shift_base = 65 if char.isupper() else 97
                result += chr(((ord(char) - shift_base - b) * mod_inverse) % 26 + shift_base)
            else:
                result += char
    else:
        for char in text:
            if char.isalpha():
                shift_base = 65 if char.isupper() else 97
                result += chr((a * (ord(char) - shift_base) + b) % 26 + shift_base)
            else:
                result += char
    return result

def reverse_cipher(text):
    return text[::-1]

def rail_fence_cipher(text, key, decrypt=False):
    if decrypt:
        result = ['' for _ in range(key)]
        direction = 1
        row = 0
        for char in text:
            result[row] += char
            if row == 0:
                direction = 1
            elif row == key - 1:
                direction = -1
            row += direction
        # Decryption is just reverse encoding, so we must handle it
        return ''.join(result)
    # For encryption 
    rail = ['' for _ in range(key)]
    direction = 1
    row = 0
    for char in text:
        rail[row] += char
        if row == 0:
            direction = 1
        elif row == key - 1:
            direction = -1
        row += direction
    return ''.join(rail)

@app.route('/cipher', methods=['POST'])
def cipher():
    try:
        data = request.json
        method = data.get("method")
        text = data.get("text")
        decrypt = data.get("decrypt", False)

        # Default or dynamically assigned keys
        if method == "caesar":
            key = 3  # Default shift for Caesar Cipher
            result = caesar_cipher(text, key, decrypt)
        elif method == "vigenere":
            key = "KEY"  # Default key for Vigenère Cipher
            result = vigenere_cipher(text, key, decrypt)
        elif method == "affine":
            a, b = 5, 8  # Default constants for Affine Cipher
            result = affine_cipher(text, a, b, decrypt)
        elif method == "reverse":
            result = reverse_cipher(text)
        elif method == "railfence":
            key = 3  # Default rails for Rail Fence Cipher
            result = rail_fence_cipher(text, key, decrypt)
        else:
            result = "Method not supported!"
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)