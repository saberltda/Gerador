# src/logic.py
import random

class PlanoDiretor:
    """
    Responsável pela Lógica de Negócio e Compatibilidade Urbana.
    Garante que o ativo sorteado faz sentido físico no bairro escolhido.
    """

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
        
        # Recupera a zona normalizada pelo database.py (ex: 'residencial_aberto')
        # Se não tiver zona definida, assume 'indefinido'
        zona = bairro_obj.get("zona_normalizada", "indefinido") if bairro_obj else "indefinido"
        
        obs = f"Compatível com {zona}"

        # =========================================================
        # REGRAS DE OURO (CORREÇÃO AUTOMÁTICA)
        # =========================================================

        # REGRA 1: Bairro Aberto não pode ter "Condomínio Fechado"
        if zona == "residencial_aberto" and "Condomínio" in ativo_final and "Fechado" in ativo_final:
            ativo_final = "Casa de Rua / Sobrado Padrão"
            obs = "Ajuste Automático: Bairro aberto não comporta condomínio fechado."

        # REGRA 2: Condomínio Fechado exige imóvel interno
        elif zona == "residencial_fechado" and "Rua" in ativo_final:
            ativo_final = "Casa em Condomínio Fechado"
            obs = "Ajuste Automático: Zona fechada exige tipologia de condomínio."

        # REGRA 3: Zona Industrial força galpão (se o cluster for investidor)
        elif zona == "industrial" and cluster_tecnico == "INVESTOR":
            ativo_final = "Terreno Industrial / Galpão Logístico"
            obs = "Ajuste Automático: Zona Industrial detectada."

        # REGRA 4: Chácaras (Ajuste de terminologia)
        elif zona == "chacaras_aberto" and "Apartamento" in ativo_final:
            ativo_final = "Chácara de Lazer"
            obs = "Ajuste Automático: Zona rural/chácaras não tem verticalização."

        return ativo_final, obs