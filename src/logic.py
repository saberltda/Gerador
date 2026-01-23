# src/logic.py
import random
from .config import GenesisConfig

class PlanoDiretor:
    """
    Lógica de Compatibilidade Física (O 'Engenheiro').
    Garante que não se venda "Casa em Condomínio" num bairro industrial.
    """
    def refinar_ativo(self, cluster, bairro, ativos_base):
        zona = bairro.get("zona_normalizada", "indefinido")
        
        # Se ativos_base for string (seleção manual), transforme em lista para processar
        if isinstance(ativos_base, str):
            ativos_base = [ativos_base]
            
        ativo_final = random.choice(ativos_base)
        obs = f"Compatível com {zona}"

        # Lógica de correção de coerência física
        if zona == "residencial_aberto" and "Condomínio" in ativo_final and "Fechado" in ativo_final:
            ativo_final = "Casa de Rua / Sobrado"
            obs = "Ajuste Automático: Bairro aberto não tem condomínio."
        elif zona == "residencial_fechado" and "Rua" in ativo_final:
            ativo_final = "Casa em Condomínio Fechado"
            obs = "Ajuste Automático: Condomínio exige casa interna."
        elif zona == "industrial" and cluster == "INVESTOR":
            ativo_final = "Terreno Industrial / Galpão"
            obs = "Ajuste Automático: Investidor em zona industrial."

        return ativo_final, obs

class SEOHeatmap:
    """
    (Placeholder) Analisa tendências de busca para sugerir tópicos quentes.
    Mantido para compatibilidade com engine.py.
    """
    pass

class RiscoJuridico:
    """
    (Placeholder) Verifica riscos legais básicos do ativo.
    Mantido para compatibilidade com engine.py.
    """
    pass

class PortalSynchronizer:
    """
    Gerencia as listas e opções exclusivas do MODO PORTAL.
    """
    def get_editorias_display(self):
        # Retorna lista de tuplas (chave, nome_bonito)
        raw = GenesisConfig.PORTAL_CATALOG
        display_list = []
        for k, v_list in raw.items():
            if k == "DESTAQUE_DIARIO": display_list.append((k, "🚨 Destaque / Resumo do Dia"))
            elif k == "CIDADE_ALERTA": display_list.append((k, "🚔 Cidade Alerta (Polícia/Trânsito)"))
            elif k == "PODER_POLITICA": display_list.append((k, "⚖️ Poder & Política"))
            elif k == "VIVER_INDAIATUBA": display_list.append((k, "🎭 Viver Indaiatuba (Lazer/Cultura)"))
            elif k == "SEU_DINHEIRO": display_list.append((k, "💰 Seu Dinheiro (Economia)"))
            elif k == "EDUCACAO_FUTURO": display_list.append((k, "🎓 Educação & Futuro"))
            elif k == "COMUNIDADE": display_list.append((k, "🤝 Comunidade & Pets"))
            else: display_list.append((k, k.replace("_", " ").title()))
        return display_list
    
    def get_valid_topics(self, editoria_key):
        return list(GenesisConfig.PORTAL_TOPICS_MAP.items())

    def get_valid_formats(self, editoria_key):
        return list(GenesisConfig.PORTAL_FORMATS_MAP.items())
    
    def get_random_set(self):
        """Retorna um pacote aleatório válido para o Portal"""
        editoria_key = random.choice(list(GenesisConfig.PORTAL_CATALOG.keys()))
        editoria_label = GenesisConfig.PORTAL_CATALOG[editoria_key][0] # Pega o primeiro item como exemplo
        
        topico = random.choice(list(GenesisConfig.PORTAL_TOPICS_MAP.items()))
        formato = random.choice(list(GenesisConfig.PORTAL_FORMATS_MAP.items()))
        
        return {
            'editoria': (editoria_key, editoria_label),
            'topico': topico,
            'formato': formato
        }

class RealEstateSynchronizer:
    """
    Gerencia as listas e opções exclusivas do MODO IMOBILIÁRIA.
    """
    def get_clusters_display(self):
        return [
            ("FAMILY", "👨‍👩‍👧‍👦 Família (Casas/Condomínios)"),
            ("HIGH_END", "💎 Alto Padrão (Luxo)"),
            ("URBAN", "🏙️ Urbano (Aptos/Centro)"),
            ("INVESTOR", "📈 Investidor (Terrenos/Flips)"),
            ("LOGISTICS", "🚚 Logística/Industrial"),
            ("RURAL_LIFESTYLE", "🌿 Rural/Chácaras"),
            ("CORPORATE", "🏢 Corporativo/Salas")
        ]

    def get_valid_assets(self, cluster_key):
        return GenesisConfig.ASSETS_CATALOG.get(cluster_key, ["Imóvel Padrão"])

    def get_valid_topics(self, cluster_key):
        return list(GenesisConfig.TOPICS_MAP.items())

    def get_valid_formats(self, cluster_key):
        return list(GenesisConfig.REAL_ESTATE_FORMATS_MAP.items())

    def get_random_set(self):
        """Retorna um pacote aleatório válido para Imobiliária"""
        cluster_key = random.choice(list(GenesisConfig.ASSETS_CATALOG.keys()))
        assets = GenesisConfig.ASSETS_CATALOG[cluster_key]
        ativo = random.choice(assets)
        
        topico = random.choice(list(GenesisConfig.TOPICS_MAP.items()))
        formato = random.choice(list(GenesisConfig.REAL_ESTATE_FORMATS_MAP.items()))
        
        return {
            'cluster': (cluster_key, cluster_key),
            'ativo': ativo,
            'topico': topico,
            'formato': formato
        }
