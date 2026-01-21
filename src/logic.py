# src/logic.py
import random
import unicodedata

class PlanoDiretor:
    """
    Responsável pela Lógica de Negócio e Compatibilidade Urbana.
    Garante que o ativo sorteado faz sentido físico no bairro escolhido.
    """

    def _normalize(self, texto: str) -> str:
        """
        Remove acentos e coloca em minúsculas para comparação segura.
        Ex: "CONDOMÍNIO" -> "condominio"
        """
        if not isinstance(texto, str):
            return ""
        t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
        return t.lower()

    def refinar_ativo(self, cluster_tecnico, bairro_obj, ativos_base_list):
        """
        Analisa a compatibilidade entre o Bairro e o Tipo de Imóvel.
        Se houver incompatibilidade física (ex: Condomínio em Bairro Aberto),
        o sistema corrige automaticamente.
        """
        
        # Se ativos_base for uma string única (seleção manual), transforma em lista
        if isinstance(ativos_base_list, str):
            ativos_base_list = [ativos_base_list]

        # Sorteia um ativo inicial da lista de candidatos
        ativo_final = random.choice(ativos_base_list)
        ativo_norm = self._normalize(ativo_final)
        
        # Recupera a zona normalizada pelo database.py (ex: 'residencial_aberto')
        # Se não tiver zona definida, assume 'indefinido'
        zona = bairro_obj.get("zona_normalizada", "indefinido") if bairro_obj else "indefinido"
        
        obs = f"Compatível com {zona}"

        # =========================================================
        # REGRAS DE OURO (CORREÇÃO AUTOMÁTICA)
        # =========================================================

        # REGRA 1: Bairro Aberto não pode ter "Condomínio Fechado"
        # Agora compara com texto normalizado (minúsculo e sem acento)
        if zona == "residencial_aberto" and "condominio" in ativo_norm and "fechado" in ativo_norm:
            ativo_final = "Casa de Rua / Sobrado Padrão"
            obs = "Ajuste Automático: Bairro aberto não comporta condomínio fechado."

        # REGRA 2: Condomínio Fechado exige imóvel interno
        elif zona == "residencial_fechado" and "rua" in ativo_norm:
            ativo_final = "Casa em Condomínio Fechado"
            obs = "Ajuste Automático: Zona fechada exige tipologia de condomínio."

        # REGRA 3: Zona Industrial força galpão (se o cluster for investidor)
        elif zona == "industrial" and cluster_tecnico == "INVESTOR":
            ativo_final = "Terreno Industrial / Galpão Logístico"
            obs = "Ajuste Automático: Zona Industrial detectada."

        # REGRA 4: Chácaras (Ajuste de terminologia)
        elif zona == "chacaras_aberto" and "apartamento" in ativo_norm:
            ativo_final = "Chácara de Lazer"
            obs = "Ajuste Automático: Zona rural/chácaras não tem verticalização."

        return ativo_final, obs
