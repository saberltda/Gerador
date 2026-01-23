# src/logic.py
from .config import GenesisConfig

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
