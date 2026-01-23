# src/logic.py
import random
import unicodedata
from collections import defaultdict
from .config import GenesisConfig

# =======================================================
# SINCRONIZADOR PORTAL
# =======================================================
class PortalSynchronizer:
    def __init__(self):
        self.matrix = GenesisConfig.PORTAL_MATRIX
        self.topics_display = GenesisConfig.PORTAL_TOPICS_DISPLAY
        self.formats_display = GenesisConfig.PORTAL_FORMATS_DISPLAY

    def get_editorias_display(self):
        return [(k, v['label']) for k, v in self.matrix.items()]

    def get_valid_topics(self, editoria_key):
        if editoria_key not in self.matrix: return []
        raw = self.matrix[editoria_key]['topics']
        return [(t, self.topics_display.get(t, t)) for t in raw]

    def get_valid_formats(self, editoria_key):
        if editoria_key not in self.matrix: return []
        raw = self.matrix[editoria_key]['formats']
        return [(f, self.formats_display.get(f, f)) for f in raw]

    def get_random_set(self):
        editoria_key = random.choice(list(self.matrix.keys()))
        editoria_label = self.matrix[editoria_key]['label']
        topic_key = random.choice(self.matrix[editoria_key]['topics'])
        format_key = random.choice(self.matrix[editoria_key]['formats'])
        return {
            "editoria": (editoria_key, editoria_label),
            "topico": (topic_key, self.topics_display.get(topic_key, topic_key)),
            "formato": (format_key, self.formats_display.get(format_key, format_key))
        }

# =======================================================
# NOVO: SINCRONIZADOR IMOBILIÁRIO
# =======================================================
class RealEstateSynchronizer:
    """
    Garante que Cluster (Categoria) -> Ativo -> Tópico -> Formato
    façam sentido para o mercado imobiliário.
    """
    def __init__(self):
        self.matrix = GenesisConfig.REAL_ESTATE_MATRIX
        self.assets_catalog = GenesisConfig.ASSETS_CATALOG
        self.topics_display = GenesisConfig.REAL_ESTATE_TOPICS_DISPLAY
        self.formats_display = GenesisConfig.REAL_ESTATE_FORMATS_DISPLAY

    def get_clusters_display(self):
        """Retorna lista de (KEY, LABEL) para os clusters/categorias"""
        return [(k, v['label']) for k, v in self.matrix.items()]

    def get_valid_assets(self, cluster_key):
        """Retorna lista de ativos (strings) válidos para este cluster"""
        return self.assets_catalog.get(cluster_key, [])

    def get_valid_topics(self, cluster_key):
        """Retorna tópicos válidos para o cluster"""
        if cluster_key not in self.matrix: return []
        raw = self.matrix[cluster_key]['topics']
        return [(t, self.topics_display.get(t, t)) for t in raw]

    def get_valid_formats(self, cluster_key):
        """Retorna formatos válidos para o cluster"""
        if cluster_key not in self.matrix: return []
        raw = self.matrix[cluster_key]['formats']
        return [(f, self.formats_display.get(f, f)) for f in raw]
    
    def get_random_set(self):
        """Gera um pacote imobiliário completo e lógico"""
        cluster_key = random.choice(list(self.matrix.keys()))
        cluster_label = self.matrix[cluster_key]['label']
        
        assets_list = self.assets_catalog.get(cluster_key, ["Imóvel Padrão"])
        asset_val = random.choice(assets_list)
        
        topic_key = random.choice(self.matrix[cluster_key]['topics'])
        format_key = random.choice(self.matrix[cluster_key]['formats'])
        
        return {
            "cluster": (cluster_key, cluster_label),
            "ativo": asset_val,
            "topico": (topic_key, self.topics_display.get(topic_key, topic_key)),
            "formato": (format_key, self.formats_display.get(format_key, format_key))
        }

# =======================================================
# LEGACY LOGIC
# =======================================================
class SEOHeatmap:
    def __init__(self):
        self.mapa = defaultdict(lambda: defaultdict(int))
    def registrar(self, bairro_slug, cluster_nome):
        self.mapa[bairro_slug][cluster_nome] += 1
    def saturacao(self, bairro_slug, cluster_nome):
        n = self.mapa[bairro_slug][cluster_nome]
        if n >= 5: return "ALTA"
        if n >= 3: return "MÉDIA"
        return "BAIXA"

class RiscoJuridico:
    def calcular(self, bairro, cluster_key):
        zona_norm = bairro.get("zona_normalizada", "")
        score = 0
        if zona_norm == "industrial": score += 3
        if cluster_key in ("CORPORATE", "LOGISTICS"): score += 2
        if "mista" in zona_norm: score += 1
        if score >= 5: return "ALTO"
        if score >= 3: return "MÉDIO"
        return "BAIXO"

class PlanoDiretor:
    def _normalize(self, texto: str) -> str:
        if not isinstance(texto, str): return ""
        t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
        return t.lower()

    def calcular_risco_juridico(self, zona_norm: str, cluster_key: str) -> str:
        score = 0
        if zona_norm == "industrial": score += 3
        if cluster_key in ("CORPORATE", "LOGISTICS"): score += 2
        if "mista" in zona_norm: score += 1
        if score >= 5: return "ALTO"
        if score >= 3: return "MÉDIO"
        return "BAIXO"

    def refinar_ativo(self, cluster_tecnico, bairro_obj, ativos_base_list):
        if isinstance(ativos_base_list, str): ativos_base_list = [ativos_base_list]
        ativo_final = random.choice(ativos_base_list)
        ativo_norm = self._normalize(ativo_final)
        zona = bairro_obj.get("zona_normalizada", "indefinido") if bairro_obj else "indefinido"
        obs_log = []
        risco = self.calcular_risco_juridico(zona, cluster_tecnico)

        if zona == "industrial":
            termos_proibidos = ["casa", "apto", "apartamento", "dormitórios", "sobrado", "residencial"]
            if any(t in ativo_norm for t in termos_proibidos) or cluster_tecnico in ["FAMILY", "URBAN", "HIGH_END"]:
                ativo_final = "GALPÃO INDUSTRIAL" if cluster_tecnico == "LOGISTICS" else "TERRENO INDUSTRIAL"
                obs_log.append("CORREÇÃO: Zona Industrial -> Ajustado.")

        elif zona == "residencial_fechado":
            if any(t in ativo_norm for t in ["galpão", "loja", "comercial", "rua"]):
                ativo_final = "CASA EM CONDOMÍNIO"
                obs_log.append("CORREÇÃO: Zona Fechada -> Forçado CASA CONDOMÍNIO.")

        elif zona == "residencial_aberto":
            if any(t in ativo_norm for t in ["condominio", "fechado", "portaria"]):
                ativo_final = "CASA DE RUA"
                obs_log.append("CORREÇÃO: Bairro Aberto -> Forçado CASA DE RUA.")

        if not obs_log: obs_log.append(f"Compatível com {zona}")
        return ativo_final, f"{' | '.join(obs_log)} [Risco: {risco}]"
