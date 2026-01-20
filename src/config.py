# src/config.py

class GenesisConfig:
    VERSION = "GERADOR V.53.0 (MODULAR)"

    # Design System & URLs
    COLOR_PRIMARY = "#003366"   # Azul Saber
    BLOG_URL = "https://blog.saber.imb.br"
    FUSO_PADRAO = "-03:00"

    # =====================================================
    # 1. INTELIGÊNCIA DE SEO (Weighted Randomness)
    # =====================================================
    # Mapeamento: Chave Técnica -> Nome Amigável
    TOPICS_MAP = {
        "INVESTIMENTO": "Valorização e Aluguel", 
        "CUSTO_VIDA": "Matemática Financeira e Custo de Vida", 
        "SEGURANCA": "Segurança Pública e Patrimonial", 
        "EDUCACAO": "Escolas e Formação dos Filhos",
        "LOGISTICA": "Trânsito, Estradas e Viracopos",
        "LAZER": "Gastronomia, Parques e Clubes",
        "SAUDE": "Hospitais, Médicos e Bem-estar",
        "FUTURO": "Plano Diretor e Obras Futuras", 
        "CONDOMINIO": "Vida em Comunidade vs Privacidade",
        "COMMUTE": "Vida Híbrida (SP-Indaiatuba)",
        "LUXO": "Mercado de Alto Padrão",
        "PETS": "Infraestrutura para Animais",
        "HOME_OFFICE": "Conectividade e Espaço de Trabalho",
        "ARQUITETURA": "Estilo das Casas e Tendências",
        "CLIMA": "Microclima e Áreas Verdes"
    }

    # Pesos: Quanto maior, mais chance de ser sorteado
    # Foco em Money Keywords (Investimento, Segurança, Custo)
    TOPICS_WEIGHTS = {
        "INVESTIMENTO": 100,
        "CUSTO_VIDA": 90,
        "SEGURANCA": 85,
        "FUTURO": 80,
        "EDUCACAO": 70,
        "LOGISTICA": 60,
        "SAUDE": 50,
        "LAZER": 40,
        "CONDOMINIO": 40,
        "COMMUTE": 35,
        "LUXO": 30,
        "HOME_OFFICE": 20,
        "PETS": 15,
        "ARQUITETURA": 10,
        "CLIMA": 5 
    }

    # =====================================================
    # 2. REGRAS DE SEGURANÇA (ALTO NÍVEL)
    # =====================================================
    STRICT_GUIDELINES = [
        "NUNCA invente nomes de clientes (ex: Ricardo, Ana, João).",
        "NUNCA invente profissões específicas para o personagem.",
        "NUNCA crie depoimentos falsos.",
        "OBRIGATÓRIO: Pesquise locais reais no Google Maps antes de citar."
    ]

    RULES = {
        "FORBIDDEN_WORDS": [
            "sonho", "sonhos", "oportunidade única", "excelente localização",
            "ótimo investimento", "preço imperdível", "lindo", "maravilhoso",
            "tranquilo", "localização privilegiada", "região privilegiada",
            "venha conferir", "agende sua visita", "paraíso", "espetacular",
            "imóvel dos sonhos", "toque de requinte"
        ]
    }

    # =====================================================
    # 3. MATRIZ DE PERSONAS (ARQUÉTIPOS)
    # =====================================================
    PERSONAS = {
        "EXODUS_SP_FAMILY": {
            "cluster_ref": "FAMILY",
            "nome": "Família em Êxodo Urbano",
            "dor": "Medo da violência e trânsito caótico da capital.",
            "desejo": "Quintal, segurança de condomínio e escolas fortes."
        },
        "INVESTOR_ROI": {
            "cluster_ref": "INVESTOR",
            "nome": "Investidor Analítico",
            "dor": "Medo da inflação e vacância do imóvel.",
            "desejo": "Rentabilidade real, valorização do m² e liquidez."
        },
        "REMOTE_WORKER": {
            "cluster_ref": "FAMILY",
            "nome": "Profissional Home Office",
            "dor": "Internet instável e falta de espaço dedicado para trabalho.",
            "desejo": "Cômodo extra (Office), silêncio e vista livre."
        },
        "HYBRID_COMMUTER": {
            "cluster_ref": "URBAN",
            "nome": "O Pendular (SP-Indaiatuba)",
            "dor": "Cansaço da estrada e tempo perdido no trânsito.",
            "desejo": "Acesso imediato à Rodovia e serviços rápidos."
        },
        "RETIREE_ACTIVE": {
            "cluster_ref": "FAMILY",
            "nome": "Melhor Idade Ativa",
            "dor": "Solidão, escadas e distância de serviços de saúde.",
            "desejo": "Casa térrea, proximidade do Parque e farmácias."
        },
        "FIRST_HOME": {
            "cluster_ref": "URBAN",
            "nome": "Jovens (1º Imóvel)",
            "dor": "Orçamento limitado e medo de financiamento longo.",
            "desejo": "Entrada viável, baixo condomínio e potencial de venda futura."
        },
        "LUXURY_SEEKER": {
            "cluster_ref": "HIGH_END",
            "nome": "Buscador de Exclusividade",
            "dor": "Falta de privacidade e padronização excessiva.",
            "desejo": "Arquitetura autoral, terrenos duplos e lazer privativo."
        },
        "PET_LOVER": {
            "cluster_ref": "FAMILY",
            "nome": "Tutor de Grandes Animais",
            "dor": "Regras restritivas de condomínio e falta de espaço verde.",
            "desejo": "Quintal privativo gramado e parques próximos."
        },
        "MEDICAL_PRO": {
            "cluster_ref": "HIGH_END",
            "nome": "Profissional de Saúde (Médicos)",
            "dor": "Rotina exaustiva e necessidade de descanso absoluto.",
            "desejo": "Proximidade do HAOC/Santa Ignês e silêncio total."
        },
        "LOGISTICS_MANAGER": {
            "cluster_ref": "LOGISTICS",
            "nome": "Gestor de Logística/Empresário",
            "dor": "Custo logístico (Last Mile) e falta de área de manobra.",
            "desejo": "Galpão funcional, pé direito alto e acesso à SP-75."
        }
    }

    # Mapa para a TELA (Bonito)
    CONTENT_FORMATS_MAP = {
        "GUIA_DEFINITIVO": "📘 Guia Definitivo Completo",
        "LISTA_POLEMICA": "🔥 Lista Polêmica (Mitos & Verdades)",
        "COMPARATIVO_TECNICO": "⚖️ Comparativo Técnico (Prós e Contras)",
        "CENARIO_ANALITICO": "📊 Cenário Analítico (Investidor)",
        "CHECKLIST_TECNICO": "✅ Checklist de Verificação",
        "PREVISAO_MERCADO": "🔮 Previsão de Mercado Futuro",
        "ROTINA_SUGERIDA": "📅 Rotina Sugerida (Dia a Dia)",
        "PERGUNTAS_RESPOSTAS": "❓ Perguntas & Respostas (FAQ)",
        "INSIGHT_DE_CORRETOR": "💡 Insight de Corretor (Bastidores)",
        "DATA_DRIVEN": "📈 Análise Baseada em Dados"
    }

    # Lista para o MOTOR (Técnico)
    # Extrai automaticamente só as CHAVES do dicionário acima
    CONTENT_FORMATS = list(CONTENT_FORMATS_MAP.keys())

    EMOTIONAL_TRIGGERS = [
        "MEDO_PERDA", "GANANCIA_LOGICA", "ALIVIO_IMEDIATO",
        "STATUS_ORGULHO", "SEGURANCA_TOTAL"
    ]
