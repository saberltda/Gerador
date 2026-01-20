# src/database.py
import json
import os
from .utils import slugify
from .config import GenesisConfig # <--- Importando a nova config

class GenesisData:
    def __init__(self, bairros_path: str = "assets/bairros.json"):
        """
        Carrega a lista de bairros e define os ativos imobiliários disponíveis.
        """
        self.bairros = self._carregar_bairros(bairros_path)

        # AGORA LÊ DIRETAMENTE DO CONFIG.PY
        # Isso centraliza a lista de imóveis num lugar só.
        self.ativos_por_cluster = GenesisConfig.ASSETS_CATALOG
        
        # Gera uma lista única de todos os ativos para o SelectBox da interface
        self.todos_ativos = []
        for lista in self.ativos_por_cluster.values():
            self.todos_ativos.extend(lista)
        self.todos_ativos = list(set(self.todos_ativos)) # Remove duplicatas
        self.todos_ativos.sort()

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

        # Processa e enriquece os dados dos bairros
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
        return txt
