# braille_converter.py
# Contains the Malayalam and English Braille Map and the conversion logic.

BRAILLE_MAP = {
    # English Letters (Grade 1)
    'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑',
    'f': '⠋', 'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚',
    'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝', 'o': '⠕',
    'p': '⠏', 'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞',
    'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭', 'y': '⠽', 'z': '⠵',

    # Punctuation/Symbols
    ' ': ' ', '.': '⠲', ',': '⠂', '?': '⠦', '!': '⠖',
    '"': '⠶', "'": '⠄', '-': '⠤', '(': '⠐⠣', ')': '⠐⠜',

    # Malayalam Independent Vowels & Vowel Signs (Matras)
    'അ': '⠁', 'ആ': '⠜', 'ഇ': '⠊', 'ഈ': '⠔',
    'ഉ': '⠥', 'ഊ': '⠳', 'ഋ': '⠱', 
    'എ': '⠑', 'ഏ': '⠣', 'ഐ': '⠌', 
    'ഒ': '⠕', 'ഓ': '⠹', 'ഔ': '⠪',
    
    'ാ': '⠜', 'ി': '⠊', 'ീ': '⠔', 'ു': '⠥', 'ൂ': '⠳', 'ൃ': '⠱',
    'െ': '⠑', 'േ': '⠣', 'ൈ': '⠌', 'ൊ': '⠕', 'ോ': '⠹', 'ൌ': '⠪',

    # Malayalam Consonants
    'ക': '⠅', 'ഖ': '⠟', 'ഗ': '⠛', 'ഘ': '⠣', 'ങ': '⠻',
    'ച': '⠉', 'ഛ': '⠡', 'ജ': '⠚', 'ഝ': '⠪', 'ഞ': '⠴',
    'ട': '⠾', 'ഠ': '⠾', 'ഡ': '⠙', 'ഢ': '⠹', 'ണ': '⠝', 
    'ത': '⠞', 'ഥ': '⠹', 'ദ': '⠙', 'ധ': '⠹', 'ന': '⠝',
    'പ': '⠏', 'ഫ': '⠋', 'ബ': '⠃', 'ഭ': '⠃', 'മ': '⠍',
    'യ': '⠽', 'ര': '⠗', 'ല': '⠇', 'വ': '⠧',
    'ശ': '⠩', 'ഷ': '⠱', 'സ': '⠎', 'ഹ': '⠓',
    'ള': '⠸', 'ഴ': '⠮', 'റ': '⠷', # Using ⠷ for ऱ 

    # Other Malayalam Signs
    '്': '⠈', # Virama (suppresses inherent vowel)
    'ം': '⠰', # Anuswara (M)
    'ഃ': '⠆', # Visarga (H)
}

def text_to_braille(text, lang):
    """
    Converts the transcribed text to Braille using the defined map.
    """
    output = []
    
    if lang == "en":
        # Ensure all English characters are lowercase for map matching
        text = text.lower() 
        for ch in text:
            # Fallback to character itself if not found in map (e.g., numbers)
            output.append(BRAILLE_MAP.get(ch, ch))
    
    elif lang == "ml":
        for ch in text:
            # Look up Malayalam characters. If not found, ignore it
            braille_char = BRAILLE_MAP.get(ch, '') 
            if braille_char:
                output.append(braille_char)
            # If ch is not found, it is ignored (e.g. spaces, numbers, etc. that aren't mapped)
    
    return "".join(output)
