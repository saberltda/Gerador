# src/config.py

class GenesisConfig:
    VERSION = "GENESIS V.57 (BEST OF BOTH WORLDS)"

    # Design System & URLs
    COLOR_PRIMARY = "#003366"   # Azul Saber
    COLOR_ACTION  = "#28a745"   # Verde Ação
    GRADIENT_CTA  = "linear-gradient(135deg, #003366 0%, #001a33 100%)"
    BLOG_URL = "https://blog.saber.imb.br"
    FUSO_PADRAO = "-03:00"

    # =====================================================
    # 1. MATRIZ DE PERSONAS (ORDENADA POR PRIORIDADE)
    # =====================================================
    PERSONAS = {
        # =================================================
        # 👑 O SEXTETO DE OURO (TOPO DA LISTA)
        # =================================================
        "CITIZEN_GENERAL": {
            "cluster_ref": ["PORTAL", "URBAN"], 
            "nome": "🏙️ CIDADÃO DE INDAIATUBA (Informação Geral)",
            "dor": "Desinformação sobre obras, trânsito e o futuro da cidade.",
            "desejo": "Notícias rápidas, utilidade pública e entender a valorização do bairro."
        },
        "INVESTOR_SHARK": {
            "cluster_ref": ["INVESTOR"],
            "nome": "🦈 INVESTIDOR SHARK (Foco em Yield)",
            "dor": "Dinheiro perdendo para inflação real e medo de vacância prolongada.",
            "desejo": "Yield comprovado, análise de dados (vacância/m²) e liquidez de saída."
        },
        "EXODUS_ELITE": {
            "cluster_ref": ["HIGH_END", "FAMILY"],
            "nome": "✈️ EXODUS ELITE SP (A Fuga da Capital)",
            "dor": "Violência da capital, trânsito caótico e filhos crescendo sem liberdade.",
            "desejo": "Segurança de condomínio fechado, escolas bilíngues e quintal com grama."
        },
        "FIRST_HOME_COUPLE": {
            "cluster_ref": ["URBAN", "FAMILY"],
            "nome": "🔑 1º IMÓVEL (Casal Jovem)",
            "dor": "Medo de financiamento de 30 anos e de ficar 'preso' a um imóvel ruim.",
            "desejo": "Entrada facilitada, localização central (fazer tudo a pé) e baixo condomínio."
        },
        "OLD_MONEY": {
            "cluster_ref": ["HIGH_END"],
            "nome": "💎 OLD MONEY (Busca Privacidade)",
            "dor": "Exposição excessiva, vizinhos barulhentos e falta de exclusividade.",
            "desejo": "Terrenos duplos ou de esquina, vista para mata preservada e silêncio absoluto."
        },
        "LOGISTICS_CEO": {
            "cluster_ref": ["LOGISTICS", "CORPORATE"],
            "nome": "🚚 GIGANTE DA LOGÍSTICA (CEO/Diretor)",
            "dor": "Custo logístico (Last Mile) e falta de mão de obra qualificada.",
            "desejo": "Frente para Rodovia Santos Dumont, pé direito de 12m e incentivos fiscais."
        },

        # =================================================
        # 🚀 EXPANSÃO SEO (NICHO & OPORTUNIDADE)
        # =================================================
        "AIRBNB_PRO": {
            "cluster_ref": ["INVESTOR", "URBAN"],
            "nome": "🧳 Anfitrião Airbnb (Short Stay)",
            "dor": "Concorrência alta em SP e baixa rentabilidade no aluguel tradicional.",
            "desejo": "Studios perto do Centro/Distrito Industrial, decoração instagramável e alta rotatividade."
        },
        "DOCTOR_CLINIC": {
            "cluster_ref": ["CORPORATE", "HIGH_END"],
            "nome": "🏥 Médico/Clínica (Setor Saúde)",
            "dor": "Consultórios antigos e sem estacionamento para pacientes.",
            "desejo": "Salas modernas próximas ao HAOC/Santa Ignês ou terrenos para clínicas."
        },
        "LAND_BANKER": {
            "cluster_ref": ["INVESTOR"],
            "nome": "🗺️ Land Banker (Especulador de Terras)",
            "dor": "Comprar no pico do preço e ficar com capital travado.",
            "desejo": "Loteamentos em pré-lançamento (Vetor de Crescimento) e valorização de longo prazo."
        },

        # =================================================
        # 🧠 INTELLIGENCE PACK (DETALHAMENTO DE PERSONA)
        # =================================================
        "INVESTOR_DATA": {
            "cluster_ref": ["INVESTOR"],
            "nome": "📊 Investidor 3.0 (Data-Driven)",
            "dor": "Falta de dados confiáveis para tomada de decisão.",
            "desejo": "Relatórios, gráficos de tendência e comparação técnica."
        },
        "THE_FLIPPER": {
            "cluster_ref": ["INVESTOR"],
            "nome": "🛠️ O Flipper (Reformar para Vender)",
            "dor": "Margem de lucro espremida em imóveis prontos.",
            "desejo": "Imóvel 'feio' (desatualizado) em bairro nobre com desconto agressivo."
        },
        "TECH_NOMAD": {
            "cluster_ref": ["URBAN", "HIGH_END"],
            "nome": "💻 Tech Nomad / Home Office Definitivo",
            "dor": "Internet instável e mistura de ambiente de trabalho com lazer.",
            "desejo": "Cômodo extra isolado (Office), fibra ótica e silêncio."
        },
        "SOLO_OWNER": {
            "cluster_ref": ["URBAN"],
            "nome": "👩 Mulher Independente (Solo Owner)",
            "dor": "Preocupação com segurança pessoal e manutenção complexa.",
            "desejo": "Portaria 24h rigorosa, apartamento prático e serviços no entorno."
        },
        "PET_PARENT": {
            "cluster_ref": ["FAMILY", "URBAN"],
            "nome": "🐾 Pet Parent Premium",
            "dor": "Condomínios hostis a animais e falta de espaço.",
            "desejo": "Garden privativo, quintal seguro e parques pet-friendly."
        },
        "SILVER_PREMIUM": {
            "cluster_ref": ["HIGH_END", "URBAN"],
            "nome": "🍷 Silver Premium (Melhor Idade)",
            "dor": "Casa grande demais (ninho vazio) e escadas perigosas.",
            "desejo": "Casa térrea compacta ou apartamento de luxo com acessibilidade."
        },
        "EXP_SEEKER": {
            "cluster_ref": ["HIGH_END"],
            "nome": "✨ Buscador de Experiência (Novo Luxo)",
            "dor": "Arquitetura 'caixote' padronizada.",
            "desejo": "Design autoral, biofilia e integração com a natureza."
        },
        "ECO_CONSCIOUS": {
            "cluster_ref": ["HIGH_END", "FAMILY"],
            "nome": "🌿 O Comprador Eco-Consciente",
            "dor": "Desperdício e conta de energia alta.",
            "desejo": "Fotovoltaica, cisterna e sustentabilidade real."
        }
    }

    # =====================================================
    # 2. REGRAS DE SEGURANÇA (MANTIDAS)
    # =====================================================
    RULES = {
        "INDUSTRIAL_RESTRICTION": [
            "Casa de Rua", "Casa em Condomínio", "Apartamento",
            "Apartamento 2 ou 3 dormitórios", "Casa térrea de rua",
            "Sobrado em bairro residencial aberto", "Cobertura", "Studio residencial"
        ],
        "OPEN_NEIGHBORHOOD_RESTRICTION": [
            "Condomínio Fechado", "Portaria 24h", "Portaria 24 horas",
            "Acesso controlado", "Controle de acesso", "Lazer Completo",
            "Área de lazer completa"
        ],
        "FORBIDDEN_WORDS": [
            "sonho", "sonhos", "oportunidade única", "excelente localização",
            "ótimo investimento", "preço imperdível", "lindo", "maravilhoso",
            "tranquilo", "localização privilegiada", "região privilegiada",
            "venha conferir", "agende sua visita", "paraíso", "espetacular",
            "imóvel dos sonhos", "toque de requinte",
            "locação", "aluguel", "alugar", "inquilino", "fiador", "locatário"
        ],
        "FORBIDDEN_FEATURES": ["varanda gourmet"]
    }

    STRICT_GUIDELINES = [
        "NUNCA invente nomes de clientes (ex: Ricardo, Ana, João).",
        "NUNCA invente profissões específicas para o personagem.",
        "NUNCA crie depoimentos falsos.",
        "ALERTA GEOGRÁFICO CRÍTICO: Bairros com nomes parecidos podem ser distantes.",
        "OBRIGATÓRIO: Verifique a distância real no Google Maps Mental antes de citar proximidade.",
        "PROIBIDO descrever um imóvel específico (unidade única). Venda o BAIRRO e a TIPOLOGIA."
    ]

    # =====================================================
    # 3. TÓPICOS, FORMATOS E CLUSTERS
    # =====================================================
    TOPICS_MAP = {
        "MERCADO_DADOS": "📈 Análise de Mercado & Dados (Yield/Vacância)",
        "INVESTIMENTO_ROI": "💰 ROI e Valorização Patrimonial (Investidor)",
        "FINANCAS_TOKEN": "💳 Financiamento Inteligente & Tokenização",
        "SUSTENTABILIDADE_ESG": "🌱 Sustentabilidade ESG & Economia Verde",
        "LOCALIZACAO_PREMIUM": "📍 Localização Estratégica & Mobilidade",
        "LUXO_COMPACTO": "💎 Luxo Compacto & Design Autoral",
        "CIDADES_INTELIGENTES": "🏙️ Cidades Inteligentes & Infraestrutura",
        "HOME_OFFICE_FLEX": "💻 Home Office & Plantas Flexíveis",
        "LOGISTICA_HUB": "🚚 Logística, Viracopos e Last Mile",
        "BEM_ESTAR_BIOFILIA": "🌿 Bem-Estar, Saúde e Design Biofílico",
        "SENIOR_LIVING": "🍷 Silver Economy (Acessibilidade 60+)",
        "SEGURANCA_TECH": "🛡️ Segurança Tecnológica & IA",
        "SHORT_STAY": "🧳 Short Stay & Rentabilidade Airbnb",
        "PETS_GARDEN": "🐾 Pet Friendly & Garden Privativo",
        "SMART_HOME": "📱 Automação Residencial (Smart Home)"
    }

    TOPICS_WEIGHTS = {
        "MERCADO_DADOS": 100, "INVESTIMENTO_ROI": 95, "FINANCAS_TOKEN": 90,
        "SUSTENTABILIDADE_ESG": 85, "LOCALIZACAO_PREMIUM": 85, "LUXO_COMPACTO": 80,
        "CIDADES_INTELIGENTES": 70, "HOME_OFFICE_FLEX": 65, "LOGISTICA_HUB": 60,
        "BEM_ESTAR_BIOFILIA": 50, "SENIOR_LIVING": 45, "SEGURANCA_TECH": 40,
        "SHORT_STAY": 35, "PETS_GARDEN": 30, "SMART_HOME": 20
    }

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

    EMOTIONAL_TRIGGERS_MAP = {
        "ESCASSEZ": "💎 ESCASSEZ (A Joia da Coroa)",
        "URGENCIA": "🚨 URGÊNCIA (Agora ou Nunca)",
        "AUTORIDADE": "👑 AUTORIDADE (Quem Sabe Faz)",
        "RECIPROCIDADE": "🤝 RECIPROCIDADE (Dar para Receber)",
        "PROVA_SOCIAL": "👥 PROVA SOCIAL (O Que Todos Dizem)",
        "PORQUE": "🧠 O PORQUÊ (A Razão Lógica)",
        "ANTECIPACAO": "👀 Antecipação (O Futuro Chegando)",
        "NOVIDADE": "✨ Novidade (Dopamina/O Novo)",
        "CURIOSIDADE": "❓ Curiosidade (O Gap de Informação)",
        "HISTORIA": "📖 História (Conexão/Storytelling)",
        "MEDO": "😨 Medo (De Perder/Ficar de Fora)"
    }
    EMOTIONAL_TRIGGERS = list(EMOTIONAL_TRIGGERS_MAP.keys())

    ASSETS_CATALOG = {
        "HIGH_END": ["MANSÃO EM CONDOMÍNIO", "CASA TÉRREA ALTO PADRÃO", "SOBRADO NEO CLÁSSICO", "Lote em Condomínio de Luxo"],
        "FAMILY": ["CASA EM CONDOMÍNIO", "SOBRADO COM ÁREA GOURMET", "CASA TÉRREA ACESSÍVEL", "Casa de Rua em Bairro Planejado"],
        "URBAN": ["APARTAMENTO 3 DORMITÓRIOS", "APARTAMENTO 2 DORMITÓRIOS", "COBERTURA DUPLEX", "Studio / Loft Moderno"],
        "INVESTOR": ["TERRENO EM CONDOMÍNIO", "TERRENO DE ESQUINA", "Imóvel para Reforma (Flip)", "Kitnet para Renda"],
        "LOGISTICS": ["GALPÃO INDUSTRIAL AAA", "TERRENO INDUSTRIAL", "Condomínio Logístico", "Área para CD"],
        "RURAL_LIFESTYLE": ["CHÁCARA EM ITAICI", "SÍTIO OU HARAS", "Chácara em Condomínio Fechado"],
        "CORPORATE": ["Sala Comercial Corporativa", "Laje Corporativa", "Prédio Monousuário"]
    }

    PORTAL_CATALOG = {
        "NOTICIAS": ["NOTÍCIAS DO DIA", "📰 Trânsito e Obras", "📰 Segurança Pública", "📰 Nova Lei Municipal", "📰 Evento Cultural"],
        "UTILIDADE": ["💡 Farmácias de Plantão", "🚌 Horário de Ônibus", "💼 Vagas de Emprego", "💧 Falta de Água"],
        "LAZER_CULTURA": ["🍽️ Onde Comer", "🌳 Parque Ecológico", "🎭 Agenda Cultural"],
        "CURIOSIDADES": ["🏛️ História dos Bairros", "📈 Valorização dos Imóveis"]
    }
