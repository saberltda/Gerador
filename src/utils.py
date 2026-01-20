import unicodedata
import re

def slugify(texto: str) -> str:
    """
    Transforma texto em slug URL-friendly.
    Ex: 'Jardim Amstalden' -> 'jardim_amstalden'
    """
    if not isinstance(texto, str):
        return ""
    
    # Normaliza acentos (Remove til, agudo, etc)
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    texto = texto.lower()
    
    # Substitui espaços e barras por underline
    texto = texto.replace("/", "_").replace("\\", "_").replace(" ", "_")
    
    # Remove caracteres especiais restantes
    texto = re.sub(r'[^a-z0-9_]', '', texto)
    return texto