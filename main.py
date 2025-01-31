from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

class PINGenerator:
    # Define character mappings for different languages
    LANGUAGE_MAPPINGS = {
        "odia": {
            "ଅ": "A0", "ଆ": "A1", "ଇ": "I2", "ଈ": "I3", "ଉ": "U4",
            "ଊ": "U5", "ଋ": "R6", "ଏ": "E7", "ଐ": "E8", "ଓ": "O9",
            "କ": "K1", "ଖ": "K2", "ଗ": "G3", "ଘ": "G4", "ଙ": "N5",
            "ଚ": "C6", "ଛ": "C7", "ଜ": "J8", "ଝ": "J9", "ଞ": "N0",
            "ଟ": "T1", "ଠ": "T2", "ଡ": "D3", "ଢ": "D4", "ଣ": "N5",
            "ତ": "T6", "ଥ": "T7", "ଦ": "D8", "ଧ": "D9", "ନ": "N0",
            "ପ": "P1", "ଫ": "P2", "ବ": "B3", "ଭ": "B4", "ମ": "M5",
            "ଯ": "Y6", "ର": "R7", "ଲ": "L8", "ଶ": "S9", "ଷ": "S0", "ସ": "S1",
            "ହ": "H2", "ଳ": "L3", "କ୍ଷ": "KX4", "ଜ୍ଞ": "JN5",
        },
        "telugu": {
            "అ": "A0", "ఆ": "A1", "ఇ": "I2", "ఈ": "I3", "ఉ": "U4",
            "క": "K1", "ఖ": "K2", "గ": "G3", "ఘ": "G4", "ఙ": "N5",
            "చ": "C6", "ఛ": "C7", "జ": "J8", "ఝ": "J9", "ఞ": "N0",
        },
        "tamil": {
            "அ": "A0", "ஆ": "A1", "இ": "I2", "ஈ": "I3", "உ": "U4",
            "க": "K1", "ங": "N5", "ச": "C6", "ஞ": "N0",
        },
        "malayalam": {
            "അ": "A0", "ആ": "A1", "ഇ": "I2", "ഈ": "I3", "ഉ": "U4",
            "ക": "K1", "ഖ": "K2", "ഗ": "G3", "ഘ": "G4", "ങ": "N5",
            "ച": "C6", "ഛ": "C7", "ജ": "J8", "ഝ": "J9", "ഞ": "N0",
        }
    }

    # Special character mapping
    SPECIAL_CHAR_MAPPING = {
        "0": "@", "1": "#", "2": "%", "3": "&", "4": "*", "5": "$",
        "6": "@", "7": "#", "8": "%", "9": "&"
    }

    # Language script mapping for transliteration
    SCRIPT_MAPPING = {
        "odia": sanscript.ORIYA,
        "telugu": sanscript.TELUGU,
        "tamil": sanscript.TAMIL,
        "malayalam": sanscript.MALAYALAM
    }

    def __init__(self, language="odia"):
        if language not in self.LANGUAGE_MAPPINGS:
            raise ValueError(f"Unsupported language: {language}")
        self.language = language
        self.mapping = self.LANGUAGE_MAPPINGS[language]
        self.script = self.SCRIPT_MAPPING[language]

    def transliterate_text(self, english_text):
        """Convert English transliterated text to the selected Indian script"""
        return transliterate(english_text.lower(), sanscript.ITRANS, self.script)

    def map_to_values(self, script_text):
        """Map Indian script characters to predefined values"""
        mapped_values = []
        for char in script_text:
            if char in self.mapping:
                mapped_values.append(self.mapping[char])
        return mapped_values

    def repeat_to_length(self, values, length, default_char="0"):
        """Ensure minimum length by repeating values if necessary with a specified default"""
        if not values:
            return [default_char] * length  # Default if no values found
        while len(values) < length:
            values += values  # Repeat from start
        return values[:length]

    def generate_pins(self, mapped_values):
        """Generate 4-digit, 6-digit, and alphanumeric PINs deterministically"""
        combined = "".join(mapped_values)
        digits = [c for c in combined if c.isdigit()]
        letters = [c for c in combined if c.isalpha()]

        pin4 = "".join(self.repeat_to_length(digits, 4, '9'))
        pin6 = "".join(self.repeat_to_length(digits, 6, '9'))
        first_digit = pin4[0] if pin4 else '9'
        special_char = self.SPECIAL_CHAR_MAPPING.get(first_digit, "@")

        # Generate alphabet part with min 4 and max 6 letters
        if not letters:
            alphabet_part = 'z' * 4
        else:
            original_length = len(letters)
            repeats_needed = (4 + original_length - 1) // original_length  # Ceiling division
            extended = letters * repeats_needed
            extended = extended[:6]  # Truncate to max 6
            alphabet_part = ''.join(extended)
            # Ensure minimum 4 characters (add 'z' if still insufficient)
            if len(alphabet_part) < 4:
                alphabet_part += 'z' * (4 - len(alphabet_part))
            alphabet_part = alphabet_part[:6]  # Final truncation

        alphanumeric = alphabet_part + special_char + pin4

        return pin4, pin6, alphanumeric

    def generate(self, english_text):
        """Main function to generate PINs from input text"""
        script_text = self.transliterate_text(english_text)
        mapped_values = self.map_to_values(script_text)
        pin4, pin6, alphanumeric_pin = self.generate_pins(mapped_values)

        return {
            "input": english_text,
            "script_text": script_text,
            "4-digit PIN": pin4,
            "6-digit PIN": pin6,
            "alphanumeric PIN": alphanumeric_pin
        }


# Example Usage
if __name__ == "__main__":
    # User chooses language
    language = input("Choose language: ")  # Change to "telugu", "tamil", or "malayalam" for other languages
    pin_generator = PINGenerator(language)

    # User input
    user_input = input("Enter text: ")

    # Generate PINs
    result = pin_generator.generate(user_input)

    # Display Results
    print(f"Input: {result['input']} → Script: {result['script_text']}")
    print(f"4-digit PIN: {result['4-digit PIN']}")
    print(f"6-digit PIN: {result['6-digit PIN']}")
    print(f"Alphanumeric PIN: {result['alphanumeric PIN']}")