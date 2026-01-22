# src/logic.py
import random
import unicodedata
from collections import defaultdict
from .config import GenesisConfig

class PortalSynchronizer:
    """
    Garante que Editoria, Tópico e Formato sempre façam sentido juntos no Modo Portal.
    Evita combinações ilógicas (ex: "Giro Policial" com formato "Review de Restaurante").
    """
    def __init__(self):
        self.matrix = GenesisConfig.PORTAL_MATRIX
        self.topics_display = GenesisConfig.PORTAL_TOPICS_DISPLAY
        self.formats_display = GenesisConfig.PORTAL_FORMATS_DISPLAY

    def get_editorias_display(self):
        """Retorna lista de tuplas (KEY, LABEL) para selectbox da UI"""
        # Retorna: [("GIRO_POLICIAL", "🚔 Plantão..."), ...]
        return [(k, v['label']) for k, v in self.matrix.items()]

    def get_valid_topics(self, editoria_key):
        """Retorna tópicos permitidos para uma editoria específica"""
        if editoria_key not in self.matrix:
            return []
        
        raw_topics = self.matrix[editoria_key]['topics']
        # Retorna lista de (KEY, LABEL) buscando o nome bonito no display map
        return [(t, self.topics_display.get(t, t)) for t in raw_topics]

    def get_valid_formats(self, editoria_key):
        """Retorna formatos permitidos para uma editoria específica"""
        if editoria_key not in self.matrix:
            return []
        
        raw_formats = self.matrix[editoria_key]['formats']
        # Retorna lista de (KEY, LABEL) buscando o nome bonito no display map
        return [(f, self.formats_display.get(f, f)) for f in raw_formats]

    def get_random_set(self):
        """
        Gera um conjunto completo e Sincronizado aleatoriamente.
        Usado quando o usuário escolhe 'ALEATÓRIO' no modo Portal.
        """
        # 1. Escolhe Editoria Aleatória
        editoria_key = random.choice(list(self.matrix.keys()))
        editoria_label = self.matrix[editoria_key]['label']
        
        # 2. Escolhe Tópico Válido para essa Editoria
        topic_key = random.choice(self.matrix[editoria_key]['topics'])
        topic_label = self.topics_display.get(topic_key, topic_key)
        
        # 3. Escolhe Formato Válido para essa Editoria
        format_key = random.choice(self.matrix[editoria_key]['formats'])
        format_label = self.formats_display.get(format_key, format_key)
        
        return {
            "editoria": (editoria_key, editoria_label),
            "topico": (topic_key, topic_label),
            "formato": (format_key, format_label)
        }

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
        if score >= 5: return "ALTO (Consulte Depto Jurídico)"
        if score >= 3: return "MÉDIO"
        return "BAIXO"

class PlanoDiretor:
    """
    Responsável pela Lógica de Negócio e Compatibilidade Urbana (Modo Imobiliária).
    Versão V.58 (Smart Uppercase Sync).
    """

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
        """
        Analisa a compatibilidade e corrige alucinações físicas.
        """
        if isinstance(ativos_base_list, str): ativos_base_list = [ativos_base_list]

        ativo_final = random.choice(ativos_base_list)
        ativo_norm = self._normalize(ativo_final)
        
        zona = bairro_obj.get("zona_normalizada", "indefinido") if bairro_obj else "indefinido"
        obs_log = []
        risco = self.calcular_risco_juridico(zona, cluster_tecnico)

        # --- LÓGICA DE PROTEÇÃO (Sincronizada com Catalog) ---

        # 1. ZONA INDUSTRIAL (Bloqueio Residencial)
        if zona == "industrial":
            termos_proibidos = ["casa", "apto", "apartamento", "dormitórios", "sobrado", "residencial", "mansão", "lote"]
            if any(t in ativo_norm for t in termos_proibidos) or cluster_tecnico in ["FAMILY", "URBAN", "HIGH_END"]:
                if cluster_tecnico == "INVESTOR":
                    # Usa termo do catálogo INVESTOR
                    ativo_final = "TERRENO INDUSTRIAL"
                    obs_log.append("CORREÇÃO: Residencial proibido em Z.I. -> Ajustado para TERRENO IND.")
                else:
                    # Usa termo do catálogo LOGISTICS
                    ativo_final = "GALPÃO INDUSTRIAL AAA"
                    obs_log.append("CORREÇÃO: Zona Industrial exige GALPÃO.")

        # 2. CONDOMÍNIO FECHADO (Bloqueio Comercial/Aberto)
        elif zona == "residencial_fechado":
            termos_proibidos = ["galpão", "loja", "comercial", "rua", "bairro aberto"]
            if any(t in ativo_norm for t in termos_proibidos):
                # Usa termo do catálogo FAMILY
                ativo_final = "CASA EM CONDOMÍNIO"
                obs_log.append("CORREÇÃO: Zona Fechada -> Forçado CASA CONDOMÍNIO.")

        # 3. BAIRRO ABERTO (Bloqueio de Condomínio)
        elif zona == "residencial_aberto":
            termos_condominio = ["condominio", "fechado", "portaria", "lazer completo"]
            if any(t in ativo_norm for t in termos_condominio):
                # Usa termo do catálogo FAMILY
                ativo_final = "CASA DE RUA EM BAIRRO PLANEJADO"
                obs_log.append("CORREÇÃO: Bairro Aberto -> Forçado CASA DE RUA.")

        # 4. CHÁCARAS
        elif "chacara" in zona:
            if "apartamento" in ativo_norm or "predio" in ativo_norm:
                # Usa termo do catálogo RURAL
                ativo_final = "CHÁCARA EM CONDOMÍNIO FECHADO" if "fechado" in zona else "CHÁCARA EM ITAICI"
                obs_log.append("CORREÇÃO: Verticalização proibida em zona rural.")

        if not obs_log:
            obs_log.append(f"Compatível com {zona}")

        obs_final = f"{' | '.join(obs_log)} [Risco: {risco}]"
        return ativo_final, obs_final
