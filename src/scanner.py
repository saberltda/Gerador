# src/scanner.py
import json
import urllib.request
import ssl
from .config import GenesisConfig
from .utils import slugify

class BlogScanner:
    """
    O 'Espião'.
    Acessa o feed público do Blogger para mapear o que já foi postado.
    Evita repetição de pautas recentes.
    """
    
    def __init__(self):
        base_url = GenesisConfig.BLOG_URL
        self.feed_url = f"{base_url}/feeds/posts/default?alt=json&max-results=9999"
        self.bairros_publicados = set()
        self.todos_titulos = []

    def mapear(self):
        self.bairros_publicados = set()
        self.todos_titulos = []
        
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            with urllib.request.urlopen(self.feed_url, context=ctx, timeout=10) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode())
                    
                    if "feed" in data and "entry" in data["feed"]:
                        for entry in data["feed"]["entry"]:
                            titulo = entry["title"]["$t"]
                            self.todos_titulos.append(titulo)
                            # Guarda slug com separadores para evitar match parcial
                            # Ex: "_jardim_pau_preto_"
                            self.bairros_publicados.add(f"_{slugify(titulo)}_")
                            
        except Exception as e:
            print(f"Aviso: Não foi possível escanear o blog. Erro: {e}")

    def ja_publicado(self, nome_bairro: str) -> bool:
        """
        Verifica com precisão se o bairro já foi citado.
        Usa técnica de 'Boundary Matching' (Bordas).
        """
        # Cria o slug do bairro também com separadores
        slug_bairro = f"_{slugify(nome_bairro)}_"
        
        for post_slug in self.bairros_publicados:
            # Agora "Vista" (_vista_) NÃO dá match em "Bela Vista" (_bela_vista_)
            # Mas "Pau Preto" (_pau_preto_) dá match em "Jardim Pau Preto" (_jardim_pau_preto_)
            if slug_bairro in post_slug:
                return True
        return False

    def get_ultimos_titulos(self, limite=10):
        return self.todos_titulos[:limite]

