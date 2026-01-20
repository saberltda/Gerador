# src/config.py

class GenesisConfig:
    VERSION = "GERADOR V.53.2 (PERSONAS 2026 EDITION)"

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
    # 3. MATRIZ DE PERSONAS (ARQUÉTIPOS AVANÇADOS 2026)
    # =====================================================
    PERSONAS = {
        # --- OS GIGANTES DO MERCADO (Joias da Coroa) ---
        "INVESTOR_DATA_DRIVEN": {
            "cluster_ref": "INVESTOR",
            "nome": "📊 INVESTIDOR 3.0 (Data-Driven)",
            "dor": "Medo de ativos ilíquidos e taxas de juros reais negativas.",
            "desejo": "Yield comprovado, dados de vacância e valorização acima do CDI."
        },
        "GEN_Z_FIRST_HOME": {
            "cluster_ref": "URBAN",
            "nome": "📱 GERAÇÃO Z (1º Imóvel Funcional)",
            "dor": "Orçamento apertado e aversão a processos burocráticos/lentos.",
            "desejo": "Estúdio/Compacto ultra-conectado, sem reformas e com serviços digitais."
        },
        "WEALTHY_BOOMER": {
            "cluster_ref": "HIGH_END",
            "nome": "🍷 SILVER PREMIUM (Downsizing de Luxo)",
            "dor": "Manutenção de casarões vazios e distância de serviços médicos.",
            "desejo": "Casa térrea ou apto de luxo menor, perto de tudo e com segurança total."
        },
        "EXODUS_FAMILY_PRO": {
            "cluster_ref": "FAMILY",
            "nome": "👨‍👩‍👧‍👦 FAMÍLIA EXODUS (Qualidade SP->Interior)",
            "dor": "Insegurança urbana e criação dos filhos em apartamentos fechados.",
            "desejo": "Condomínio clube, quintal privativo e escolas bilíngues num raio de 10 min."
        },
        "SOLO_FEMALE_BUYER": {
            "cluster_ref": "URBAN",
            "nome": "👩 MULHER INDEPENDENTE (Solo Owner)",
            "dor": "Medo de descapitalização e segurança física no imóvel.",
            "desejo": "Patrimônio seguro, portaria 24h e autonomia financeira imediata."
        },

        # --- NICHOS ESTRATÉGICOS (Cauda Longa) ---
        "LUXURY_EXPERIENTIAL": {
            "cluster_ref": "HIGH_END",
            "nome": "✨ Buscador de Experiência (Novo Luxo)",
            "dor": "Imóveis padronizados sem 'alma' ou exclusividade.",
            "desejo": "Arquitetura autoral, vista perene e design biofílico (natureza integrada)."
        },
        "REMOTE_TECH_NOMAD": {
            "cluster_ref": "FAMILY",
            "nome": "💻 Tech Nomad / Home Office Definitivo",
            "dor": "Internet instável e mistura de ambiente de trabalho com lazer.",
            "desejo": "Cômodo 'Zoom-Ready' isolado acusticamente e fibra ótica dedicada."
        },
        "PET_PARENT_PREMIUM": {
            "cluster_ref": "FAMILY",
            "nome": "🐾 Pet Parent Premium",
            "dor": "Regras de condomínio hostis e falta de área gramada.",
            "desejo": "Garden ou quintal privativo 'Pet-Friendly' e parques próximos."
        },
        "FLIP_PLAYER": {
            "cluster_ref": "INVESTOR",
            "nome": "🛠️ O Flipper (Reformar para Vender)",
            "dor": "Pagar preço de mercado em imóvel depreciado.",
            "desejo": "Oportunidade 'feia' em bairro nobre para reforma cosmética rápida."
        },
        "ECO_CONSCIOUS": {
            "cluster_ref": "HIGH_END",
            "nome": "🌿 O Comprador Eco-Consciente",
            "dor": "Desperdício energético e construções predatórias.",
            "desejo": "Painéis solares, reuso de água e certificação verde (ESG)."
        }
    }

    # =====================================================
    # 4. FORMATOS DE CONTEÚDO (MAPA)
    # =====================================================
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
    # Lista técnica para o motor usar nos sorteios
    CONTENT_FORMATS = list(CONTENT_FORMATS_MAP.keys())

    # =====================================================
    # 5. GATILHOS MENTAIS (GUSTAVO FERREIRA)
    # =====================================================
    EMOTIONAL_TRIGGERS_MAP = {
        # --- AS JOIAS DA COROA (Decisão de Compra) ---
        "ESCASSEZ": "💎 ESCASSEZ (A Joia da Coroa)",
        "URGENCIA": "🚨 URGÊNCIA (Fator Tempo)",
        "AUTORIDADE": "👑 AUTORIDADE (Nós Sabemos)",
        "PROVA_SOCIAL": "👥 PROVA SOCIAL (Efeito Manada)",
        "RECIPROCIDADE": "🤝 RECIPROCIDADE (Gerar Valor)",
        
        # --- GATILHOS ESTRATÉGICOS (Conexão/Retenção) ---
        "NOVIDADE": "✨ Novidade (Dopamina/Inédito)",
        "CURIOSIDADE": "❓ Curiosidade (O Segredo)",
        "INIMIGO_COMUM": "🛡️ Inimigo Comum (Nós vs Eles/Caos)",
        "ANTECIPACAO": "👀 Antecipação (Vem aí)",
        "HISTORIA": "📖 Storytelling (Jornada do Herói)",
        "COMPROMISSO": "💍 Compromisso e Coerência",
        "SIMPLICIDADE": "💡 Simplicidade (O Caminho Fácil)",
        "PORQUE": "🧠 O 'Porquê' (Justificativa Racional)"
    }
    
    EMOTIONAL_TRIGGERS = list(EMOTIONAL_TRIGGERS_MAP.keys())
