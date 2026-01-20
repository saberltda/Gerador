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
        # Monta a URL do feed JSON do Blogger
        # Pega a URL base lá do arquivo de configuração
        base_url = GenesisConfig.BLOG_URL
        self.feed_url = f"{base_url}/feeds/posts/default?alt=json&max-results=500"
        
        self.bairros_publicados = set()
        self.todos_titulos = []

    def mapear(self):
        """
        Conecta na internet, baixa a lista de posts e processa os títulos.
        """
        self.bairros_publicados = set()
        self.todos_titulos = []
        
        try:
            # Configuração SSL para ignorar erros de certificado (comum em scripts locais)
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            # Faz a requisição HTTP (GET)
            with urllib.request.urlopen(self.feed_url, context=ctx, timeout=10) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode())
                    
                    # Navega no JSON do Blogger para achar os títulos
                    if "feed" in data and "entry" in data["feed"]:
                        for entry in data["feed"]["entry"]:
                            # Extrai o título do post
                            titulo = entry["title"]["$t"]
                            
                            # Guarda o título original para exibir no histórico
                            self.todos_titulos.append(titulo)
                            
                            # Guarda a versão 'slug' para comparação matemática
                            # Ex: "Morar no Jardim Pau Preto" -> "morar_no_jardim_pau_preto"
                            self.bairros_publicados.add(slugify(titulo))
                            
        except Exception as e:
            # Se der erro (sem internet, blog fora do ar), vida que segue.
            # O sistema vai assumir que nada foi publicado e continuar funcionando.
            print(f"Aviso: Não foi possível escanear o blog. Erro: {e}")

    def ja_publicado(self, nome_bairro: str) -> bool:
        """
        Verifica se um nome de bairro já aparece em algum título anterior.
        """
        slug_bairro = slugify(nome_bairro)
        
        # Varre a lista de posts baixados
        for post_slug in self.bairros_publicados:
            # Se o nome do bairro estiver contido no slug do post...
            if slug_bairro in post_slug:
                return True
        return False

    def get_ultimos_titulos(self, limite=10):
        """Retorna a lista simples dos últimos posts para exibir na tela."""
        return self.todos_titulos[:limite]