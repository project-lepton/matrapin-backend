1. Language Mapping Loading

Loads language-specific mapping rules from JSON files located in the "mappings" directory.
If the mapping file for a given language is not found, it gracefully handles the situation by returning None.

2. Script Mapping

Defines a dictionary (SCRIPT_MAPPING) to map languages to their corresponding Sanskrit scripts (e.g., "odia" to sanscript.ORIYA).
This helps in transliterating English text to the target language's script.

3. Special Character Mapping

Defines a dictionary (SPECIAL_CHAR_MAPPING) to map digits (0-9) to special characters. This is used to add a special character to the alphanumeric PIN.

4. PINGenerator Class

Initialization (__init__)
- Stores the specified language.
- Loads the language-specific mapping using load_language_mapping.
- Determines the appropriate script for the language using SCRIPT_MAPPING.
- Raises a ValueError if the language mapping is not found.
- Mapping to Values (map_to_values)
- Translates each character in the input script_text to its corresponding value using the loaded self.mapping.
- Repeating Values (repeat_to_length)
- Repeats the given values list until it reaches the desired length.
- If values is empty, it creates a list of default values (e.g., "0") with the specified length.
- Generating PINs (generate_pins)
- Joins all mapped_values into a single string.
- Extracts digits and letters from the combined string.
- Generates a 4-digit PIN by repeating digits and padding with '9' if necessary.
- Generates a 6-digit PIN similarly.
- Determines a special character based on the first digit of the 4-digit PIN.
- Creates an alphanumeric PIN by combining letters, the special character, and the 4-digit PIN.
- Generating Output (generate)
- Transliterates the given english_text to the target language's script.
- Maps the transliterated text to values using map_to_values.
- Generates PINs using generate_pins.
- Returns a dictionary containing the input, transliterated text, and the generated 4-digit, 6-digit, and alphanumeric PINs.