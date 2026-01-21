# src/config.py

class GenesisConfig:
    VERSION = "GERADOR V.55.2 (GATILHOS EXPANDIDOS)"

    # Design System & URLs
    COLOR_PRIMARY = "#003366"   # Azul Saber
    BLOG_URL = "https://blog.saber.imb.br"
    FUSO_PADRAO = "-03:00"

    # =====================================================
    # 1. INTELIGÊNCIA DE SEO (Weighted Randomness)
    # =====================================================
    TOPICS_MAP = {
        # --- MONEY KEYWORDS (Fundo de Funil) ---
        "MERCADO_DADOS": "📈 Análise de Mercado & Dados (Yield/Vacância)",
        "INVESTIMENTO_ROI": "💰 ROI e Valorização Patrimonial (Investidor)",
        "FINANCAS_TOKEN": "💳 Financiamento Inteligente & Tokenização",
        "SUSTENTABILIDADE_ESG": "🌱 Sustentabilidade ESG & Economia Verde",
        "LOCALIZACAO_PREMIUM": "📍 Localização Estratégica & Mobilidade",
        "LUXO_COMPACTO": "💎 Luxo Compacto & Design Autoral",
        
        # --- AUTHORITY & LIFESTYLE (Meio de Funil) ---
        "CIDADES_INTELIGENTES": "🏙️ Cidades Inteligentes & Infraestrutura",
        "HOME_OFFICE_FLEX": "💻 Home Office & Plantas Flexíveis",
        "LOGISTICA_HUB": "🚚 Logística, Viracopos e Last Mile",
        "BEM_ESTAR_BIOFILIA": "🌿 Bem-Estar, Saúde e Design Biofílico",
        "SENIOR_LIVING": "🍷 Silver Economy (Acessibilidade 60+)",
        "SEGURANCA_TECH": "🛡️ Segurança Tecnológica & IA",
        
        # --- VOLUME & NICHO (Topo de Funil) ---
        "SHORT_STAY": "🧳 Short Stay & Rentabilidade Airbnb",
        "PETS_GARDEN": "🐾 Pet Friendly & Garden Privativo",
        "SMART_HOME": "📱 Automação Residencial (Smart Home)"
    }

    TOPICS_WEIGHTS = {
        "MERCADO_DADOS": 100,
        "INVESTIMENTO_ROI": 95,
        "FINANCAS_TOKEN": 90,
        "SUSTENTABILIDADE_ESG": 85,
        "LOCALIZACAO_PREMIUM": 85,
        "LUXO_COMPACTO": 80,
        "CIDADES_INTELIGENTES": 70,
        "HOME_OFFICE_FLEX": 65,
        "LOGISTICA_HUB": 60,
        "BEM_ESTAR_BIOFILIA": 50,
        "SENIOR_LIVING": 45,
        "SEGURANCA_TECH": 40,
        "SHORT_STAY": 35,
        "PETS_GARDEN": 30,
        "SMART_HOME": 20
    }

    # =====================================================
    # 2. REGRAS DE SEGURANÇA (ALTO NÍVEL)
    # =====================================================
    STRICT_GUIDELINES = [
        "NUNCA invente nomes de clientes (ex: Ricardo, Ana, João).",
        "NUNCA invente profissões específicas para o personagem.",
        "NUNCA crie depoimentos falsos.",
        "OBRIGATÓRIO: Pesquise locais reais no Google Maps antes de citar.",
        
        # --- NOVAS REGRAS ANTI-ANÚNCIO (FIX V.55.1) ---
        "PROIBIDO descrever um imóvel específico (unidade única).",
        "NÃO use: 'Esta casa possui', 'Venha visitar este imóvel', 'Acabou de entrar'.",
        "USE: 'Casas nesta região costumam ter', 'O padrão construtivo aqui oferece', 'Ao buscar imóveis neste bairro'.",
        "OBJETIVO: Vender o BAIRRO e a TIPOLOGIA (CATEGORIA), não uma unidade específica."
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
        # --- OS GIGANTES DO MERCADO ---
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

        # --- NICHOS ESTRATÉGICOS ---
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
    # 4. FORMATOS DE CONTEÚDO
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
    CONTENT_FORMATS = list(CONTENT_FORMATS_MAP.keys())

    # =====================================================
    # 5. GATILHOS MENTAIS (COMPLETO - GUSTAVO FERREIRA)
    # =====================================================
    EMOTIONAL_TRIGGERS_MAP = {
        # --- AS JOIAS DA COROA (Core Triggers) ---
        "ESCASSEZ": "💎 ESCASSEZ (A Joia da Coroa)",
        "URGENCIA": "🚨 URGÊNCIA (Agora ou Nunca)",
        "AUTORIDADE": "👑 AUTORIDADE (Quem Sabe Faz)",
        "RECIPROCIDADE": "🤝 RECIPROCIDADE (Dar para Receber)",
        "PROVA_SOCIAL": "👥 PROVA SOCIAL (O Que Todos Dizem)",
        "PORQUE": "🧠 O PORQUÊ (A Razão Lógica)",
        
        # --- GATILHOS EMOCIONAIS E ESTRATÉGICOS ---
        "ANTECIPACAO": "👀 Antecipação (O Futuro Chegando)",
        "NOVIDADE": "✨ Novidade (Dopamina/O Novo)",
        "CURIOSIDADE": "❓ Curiosidade (O Gap de Informação)",
        "HISTORIA": "📖 História (Conexão/Storytelling)",
        "INIMIGO_COMUM": "🛡️ Inimigo Comum (Nós vs O Caos)",
        "COMPROMISSO": "💍 Compromisso e Coerência",
        "DESAPEGO": "🤷 Descaso/Desapego (Não Preciso Vender)",
        "ESPECIFICIDADE": "🎯 Especificidade (Números Exatos)",
        "GARANTIA": "🛡️ Garantia (Reversão de Risco)",
        "CONTRASTE": "⚖️ Contraste (Referência de Valor)",
        "SIMPLICIDADE": "📉 Simplicidade (O Caminho Fácil)",
        "EXCLUSIVIDADE": "🌟 Exclusividade (VIP/Acesso Restrito)",
        "SEMELHANCA": "👯 Semelhança/Rapport (Somos Iguais)",
        "PERTENCIMENTO": "🤲 Pertencimento (Comunidade/Tribo)",
        "SURPRESA": "🎁 Surpresa (Quebra de Padrão)",
        "POLARIZACAO": "⚡ Polarização (Assumir um Lado)",
        "HUMANIZACAO": "😊 Humanização (Pessoas Reais)",
        "MEDO": "😨 Medo (De Perder/Ficar de Fora)"
    }
    EMOTIONAL_TRIGGERS = list(EMOTIONAL_TRIGGERS_MAP.keys())

    # =====================================================
    # 6. CATÁLOGO DE IMÓVEIS (SEO INDAIATUBA)
    # =====================================================
    # Chave = Cluster Técnico (Para a Engine filtrar)
    # Lista = Opções Visíveis
    ASSETS_CATALOG = {
        "HIGH_END": [
            "MANSÃO EM CONDOMÍNIO FECHADO (Luxo)",
            "CASA TÉRREA DE ALTO PADRÃO (Piscina)",
            "SOBRADO NEO CLÁSSICO (Condomínio)",
            "TERRENO DE ESQUINA (Condomínio)",
            "Lote em Condomínio de Luxo (>500m²)",
            "Casa com Vista para Mata Preservada"
        ],
        "FAMILY": [
            "CASA EM CONDOMÍNIO (3 Dormitórios)",
            "SOBRADO COM ÁREA GOURMET",
            "CASA TÉRREA (Acessibilidade Total)",
            "Casa de Rua em Bairro Planejado",
            "Sobrado Misto (Residencial/Comercial)",
            "Villagio / Casas Geminadas (Condomínio)"
        ],
        "URBAN": [
            "APARTAMENTO VARANDA GOURMET (Centro)",
            "COBERTURA DUPLEX (Vista Panorâmica)",
            "APARTAMENTO GARDEN (Quintal Suspenso)",
            "Studio / Loft Moderno (Investimento)",
            "Apartamento Compacto (1 Dormitório)",
            "Apartamento Padrão (2 Dormitórios)"
        ],
        "INVESTOR": [
            "TERRENO EM CONDOMÍNIO (Oportunidade)",
            "LOTE PARA CONSTRUÇÃO (Flip)",
            "Imóvel para Reforma (Retrofit)",
            "Kitnet / Studio para Locação",
            "Terreno Comercial em Avenida",
            "Área para Incorporação Vertical"
        ],
        "LOGISTICS": [
            "GALPÃO INDUSTRIAL AAA (Logística)",
            "TERRENO INDUSTRIAL (Z1/Z2)",
            "Condomínio Logístico (Módulo)",
            "Galpão Comercial (Frente Rodovia)",
            "Área para Centro de Distribuição",
            "Barracão Comercial Padrão"
        ],
        "RURAL_LIFESTYLE": [
            "CHÁCARA EM ITAICI (Lazer)",
            "SÍTIO OU HARAS (Helvetia)",
            "Chácara em Condomínio Fechado",
            "Terreno de Chácara (>1.000m²)",
            "Casa de Campo com Pomar"
        ]
    }
