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
        # Step 1: Create a blank zigzag pattern
        rail = [['\n' for _ in range(len(text))] for _ in range(key)]
        direction_down = None
        row, col = 0, 0

        # Step 2: Mark the positions of the zigzag pattern
        for i in range(len(text)):
            if row == 0:
                direction_down = True
            if row == key - 1:
                direction_down = False

            # Mark current position
            rail[row][col] = '*'
            col += 1

            # Move to next row based on direction
            row += 1 if direction_down else -1

        # Step 3: Fill the pattern with ciphertext characters
        index = 0
        for i in range(key):
            for j in range(len(text)):
                if rail[i][j] == '*' and index < len(text):
                    rail[i][j] = text[index]
                    index += 1

        # Step 4: Read characters in zigzag order to reconstruct plaintext
        result = []
        row, col = 0, 0
        direction_down = None
        for i in range(len(text)):
            if row == 0:
                direction_down = True
            if row == key - 1:
                direction_down = False

            if rail[row][col] != '\n':
                result.append(rail[row][col])
                col += 1

            row += 1 if direction_down else -1

        return ''.join(result)

    else:
        # Encryption logic
        rail = ['' for _ in range(key)]
        row = 0
        direction_down = True

        for char in text:
            rail[row] += char
            if row == 0:
                direction_down = True
            elif row == key - 1:
                direction_down = False

            row += 1 if direction_down else -1

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