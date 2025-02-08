import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

app = Flask(__name__)

CORS(app, resources={
    r"/generate": {
        "origins": [
            "https://matrapin.netlify.app",  # For production
            "http://localhost:8888"  # For local development
        ]
    }
})

# Load language mappings from JSON files
def load_language_mapping(language):
    mapping_file = f"mappings/{language}.json"
    if not os.path.exists(mapping_file):
        return None  # Handle missing file gracefully
    with open(mapping_file, "r", encoding="utf-8") as f:
        return json.load(f)

# For new language mappings, add a new entry here
# Define script mapping for transliteration
SCRIPT_MAPPING = {
    "odia": sanscript.ORIYA,
    "bengali": sanscript.BENGALI,
    "devanagari": sanscript.DEVANAGARI,
    "telugu": sanscript.TELUGU,
    "tamil": sanscript.TAMIL,
    "malayalam": sanscript.MALAYALAM
}

# Special character mapping
SPECIAL_CHAR_MAPPING = {
    "0": "@", "1": "#", "2": "%", "3": "&", "4": "*", "5": "$",
    "6": "@", "7": "#", "8": "%", "9": "&"
}

class PINGenerator:
    def __init__(self, language="odia"):
        self.language = language
        self.mapping = load_language_mapping(language)
        self.script = SCRIPT_MAPPING.get(language, sanscript.ITRANS)
        
        if self.mapping is None:
            raise ValueError(f"Language mapping for '{language}' not found!")

    def map_to_values(self, script_text):
        return [self.mapping.get(char, "") for char in script_text]

    def repeat_to_length(self, values, length, default="0"):
        if not values:
            return [default] * length
        while len(values) < length:
            values += values  
        return values[:length]

    def generate_pins(self, mapped_values):
        combined = "".join(mapped_values)
        digits = [c for c in combined if c.isdigit()]
        letters = [c for c in combined if c.isalpha()]

        pin4 = "".join(self.repeat_to_length(digits, 4, "9"))
        pin6 = "".join(self.repeat_to_length(digits, 6, "9"))

        # Special character logic
        first_digit = pin4[0] if pin4 else '9'
        special_char = SPECIAL_CHAR_MAPPING.get(first_digit, "@")

        # Ensure minimum 4 and max 6 letters for alphanumeric PIN
        if not letters:
            alphabet_part = "zzzz" # Default if no letters found
        else:
            extended_letters = letters * ((4 + len(letters) - 1) // len(letters))  # Repeat to at least 4
            alphabet_part = "".join(extended_letters[:6])

        # Final alphanumeric PIN
        alphanumeric = alphabet_part + special_char + pin4

        return pin4, pin6, alphanumeric

    def generate(self, english_text):
        script_text = transliterate(english_text.lower(), sanscript.ITRANS, self.script)
        mapped_values = self.map_to_values(script_text)
        pin4, pin6, alpha_pin = self.generate_pins(mapped_values)

        return {
            "input": english_text,
            "transliterated_text": script_text,
            "4-digit PIN": pin4,
            "6-digit PIN": pin6,
            "alphanumeric PIN": alpha_pin
        }

@app.route('/generate', methods=['POST'])
def generate_pin():
    data = request.json
    text = data.get('text', '')
    language = data.get('language', 'odia')

    try:
        generator = PINGenerator(language)
        response = generator.generate(text)
        return jsonify(response)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
