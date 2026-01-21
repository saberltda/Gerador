# src/database.py
import json
import os
from .utils import slugify
from .config import GenesisConfig 

class GenesisData:
    def __init__(self, bairros_path: str = "assets/bairros.json"):
        """
        Carrega a lista de bairros e define os ativos imobiliários E do portal.
        """
        self.bairros = self._carregar_bairros(bairros_path)

        # 1. ATIVOS DA IMOBILIÁRIA (Define o dicionário principal)
        self.ativos_imobiliaria = GenesisConfig.ASSETS_CATALOG
        
        self.ativos_por_cluster = self.ativos_imobiliaria 

        self.todos_ativos_imoveis = []
        for lista in self.ativos_imobiliaria.values():
            self.todos_ativos_imoveis.extend(lista)
        self.todos_ativos_imoveis = list(set(self.todos_ativos_imoveis))
        self.todos_ativos_imoveis.sort()

        # 2. ATIVOS DO PORTAL
        self.ativos_portal = GenesisConfig.PORTAL_CATALOG
        self.todos_ativos_portal = []
        for lista in self.ativos_portal.values():
            self.todos_ativos_portal.extend(lista)
        self.todos_ativos_portal = list(set(self.todos_ativos_portal))
        
        # --- ORDENAÇÃO INTELIGENTE (FIXAR NOTÍCIAS NO TOPO) ---
        self.todos_ativos_portal.sort()
        
        # Força "NOTÍCIAS DO DIA" para o topo da lista (Índice 0)
        # O Streamlit adiciona "Aleatório" antes deste índice 0
        ITEM_DESTAQUE = "NOTÍCIAS DO DIA"
        if ITEM_DESTAQUE in self.todos_ativos_portal:
            self.todos_ativos_portal.remove(ITEM_DESTAQUE)
            self.todos_ativos_portal.insert(0, ITEM_DESTAQUE)

        # Para compatibilidade, 'todos_ativos' padrão continua sendo imóveis
        self.todos_ativos = self.todos_ativos_imoveis

    def _carregar_bairros(self, path: str):
        if not os.path.exists(path):
            if os.path.exists(f"../{path}"):
                path = f"../{path}"
            else:
                raise RuntimeError(
                    f"ERRO CRÍTICO: Arquivo '{path}' não encontrado. "
                    "Verifique se a pasta 'assets' está na raiz do projeto."
                )

        try:
            with open(path, "r", encoding="utf-8") as f:
                raw = json.load(f)
        except Exception as e:
            raise RuntimeError(f"Erro ao ler JSON de bairros: {e}")

        bairros_enriquecidos = []
        
        def _map_zona(zona_texto: str):
            z = zona_texto.lower()
            if "industrial" in z or "empresarial" in z: return "industrial"
            if "condomínio" in z and "fechado" in z: return "residencial_fechado"
            if "chácara" in z: return "chacaras_aberto" if "aberto" in z else "chacaras_fechado"
            if "mista" in z: return "mista"
            return "residencial_aberto"

        for b in raw:
            b2 = dict(b)
            b2["slug"] = slugify(b["nome"])
            b2["zona_normalizada"] = _map_zona(b.get("zona", ""))
            bairros_enriquecidos.append(b2)

        return bairros_enriquecidos


class GenesisRules:
    """
    Gerenciador de Regras de Compliance (Constituição do Blog).
    Lê o arquivo REGRAS.txt e injeta no prompt.
    """
    def __init__(self, path: str = "assets/REGRAS.txt"):
        if not os.path.exists(path):
            if os.path.exists(f"../{path}"):
                path = f"../{path}"
            else:
                raise RuntimeError(f"ERRO: Arquivo '{path}' de regras não encontrado.")
            
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.raw_text = f.read()
        except Exception as e:
            raise RuntimeError(f"Erro ao ler REGRAS.txt: {e}")

    def get_for_prompt(self, contexto_local: str) -> str:
        txt = self.raw_text
        txt = txt.replace("{b['nome']}", contexto_local)
        txt = txt.replace("{{BAIRRO}}", contexto_local)
        txt = txt.replace("{{LOCAL}}", contexto_local)
        return txt
