# src/logic.py
import random
import unicodedata
from .config import GenesisConfig

class PlanoDiretor:
    """
    Responsável pela Lógica de Negócio, Compatibilidade Urbana e Risco Jurídico.
    Recuperado da versão 'Gerador 35'.
    """

    def _normalize(self, texto: str) -> str:
        if not isinstance(texto, str): return ""
        t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
        return t.lower()

    def calcular_risco_juridico(self, zona_norm: str, cluster_key: str) -> str:
        """Calcula o Score de Risco Jurídico (Recuperado da V35)"""
        score = 0
        if zona_norm == "industrial": score += 3
        if cluster_key in ("CORPORATE", "LOGISTICS"): score += 2
        if "mista" in zona_norm: score += 1
        
        if score >= 5: return "ALTO (Consulte Depto Jurídico)"
        if score >= 3: return "MÉDIO"
        return "BAIXO"

    def refinar_ativo(self, cluster_tecnico, bairro_obj, ativos_base_list):
        """
        Analisa a compatibilidade e Corrige alucinações de zoneamento.
        Retorna: ativo_final, obs_tecnica (com risco incluso)
        """
        if isinstance(ativos_base_list, str): ativos_base_list = [ativos_base_list]

        ativo_final = random.choice(ativos_base_list)
        ativo_norm = self._normalize(ativo_final)
        
        # Recupera zona normalizada
        zona = bairro_obj.get("zona_normalizada", "indefinido") if bairro_obj else "indefinido"
        
        obs_log = []
        risco = self.calcular_risco_juridico(zona, cluster_tecnico)

        # --- LÓGICA DE PROTEÇÃO DE ZONEAMENTO (V35) ---

        # 1. ZONA INDUSTRIAL (Bloqueio Residencial)
        if zona == "industrial":
            termos_proibidos = ["casa", "apto", "apartamento", "dormitórios", "sobrado", "residencial"]
            if any(t in ativo_norm for t in termos_proibidos) or cluster_tecnico in ["FAMILY", "URBAN", "HIGH_END"]:
                if cluster_tecnico == "INVESTOR":
                    ativo_final = "Terreno Industrial (Z1/Z2)"
                    obs_log.append("CORREÇÃO: Residencial proibido em Z.I. -> Ajustado para Terreno Ind.")
                else:
                    ativo_final = "Galpão Logístico / Industrial"
                    obs_log.append("CORREÇÃO: Zona Industrial exige Galpão.")

        # 2. CONDOMÍNIO FECHADO (Bloqueio Comercial/Aberto)
        elif zona == "residencial_fechado":
            termos_proibidos = ["galpão", "loja", "comercial", "rua", "bairro aberto"]
            if any(t in ativo_norm for t in termos_proibidos):
                ativo_final = "Casa em Condomínio Fechado"
                obs_log.append("CORREÇÃO: Zona Fechada não aceita comércio/rua.")

        # 3. BAIRRO ABERTO (Bloqueio de Condomínio)
        elif zona == "residencial_aberto":
            termos_condominio = ["condominio", "fechado", "portaria", "lazer completo"]
            if any(t in ativo_norm for t in termos_condominio):
                ativo_final = "Casa de Rua (Bairro Aberto)"
                obs_log.append("CORREÇÃO: Bairro Aberto não tem portaria/condomínio.")

        # 4. CHÁCARAS
        elif "chacara" in zona:
            if "apartamento" in ativo_norm or "predio" in ativo_norm:
                ativo_final = "Chácara de Lazer"
                obs_log.append("CORREÇÃO: Verticalização proibida em zona rural.")

        if not obs_log:
            obs_log.append(f"Compatível com {zona}")

        obs_final = f"{' | '.join(obs_log)} [Risco: {risco}]"
        return ativo_final, obs_final
