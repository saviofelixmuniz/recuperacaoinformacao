from unidecode import unidecode


def standardize_text(text):
    return unidecode(''.join(e for e in text if (e.isalnum() or e ==' ')).lower())


def join_list(article_sections):
    return ' '.join(str(e) for e in article_sections)
