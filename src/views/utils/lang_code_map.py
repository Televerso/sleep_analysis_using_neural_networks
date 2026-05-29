

languages = ["English", "Russian"]
lang_codes = ["en_US", "ru_RU"]

def language_to_code(language):
    if language in languages:
        idx = languages.index(language)
        return lang_codes[idx]
    else:
        raise ValueError(f"Language '{language}' not recognized")

def language_to_id(language):
    if language in languages:
        idx = languages.index(language)
        return idx
    else:
        raise ValueError(f"Language '{language}' not recognized")

def code_to_language(code):
    if code in lang_codes:
        idx = lang_codes.index(code)
        return lang_codes[idx]
    else:
        raise ValueError(f"Code '{code}' not recognized")

def code_to_id(code):
    if code in lang_codes:
        idx = lang_codes.index(code)
        return idx
    else:
        raise ValueError(f"Code '{code}' not recognized")

def id_to_language(id):
    return languages[id]

def id_to_code(id):
    return lang_codes[id]

