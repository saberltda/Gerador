# src/config.py

class GenesisConfig:
    VERSION = "GERADOR V.53.5 (FULL ROSTER UPDATE)"

    # Design System & URLs
    COLOR_PRIMARY = "#003366"   # Azul Saber
    COLOR_ACTION  = "#28a745"   # Verde Ação
    GRADIENT_CTA  = "linear-gradient(135deg, #003366 0%, #001a33 100%)"
    BLOG_URL = "https://blog.saber.imb.br"
    FUSO_PADRAO = "-03:00"

    # =====================================================
    # 1. REGRAS DE SEGURANÇA E BLOQUEIOS
    # =====================================================
    RULES = {
        # Ativos que NÃO podem aparecer em zonas industriais/logísticas
        "INDUSTRIAL_RESTRICTION": [
            "Casa de Rua", "Casa em Condomínio", "Apartamento",
            "Apartamento 2 ou 3 dormitórios", "Casa térrea de rua",
            "Sobrado em bairro residencial aberto", "Cobertura", "Studio residencial"
        ],
        # Recursos que NÃO podem aparecer em bairro aberto
        "OPEN_NEIGHBORHOOD_RESTRICTION": [
            "Condomínio Fechado", "Portaria 24h", "Portaria 24 horas",
            "Acesso controlado", "Controle de acesso", "Lazer Completo",
            "Área de lazer completa"
        ],
        # Clichês imobiliários banidos
        "FORBIDDEN_WORDS": [
            "sonho", "sonhos", "oportunidade única", "excelente localização",
            "ótimo investimento", "preço imperdível", "lindo", "maravilhoso",
            "tranquilo", "localização privilegiada", "região privilegiada",
            "venha conferir", "agende sua visita", "paraíso", "espetacular",
            "imóvel dos sonhos", "toque de requinte",
            "locação", "aluguel", "alugar", "inquilino", "fiador", "locatário"
        ],
        # Features sensíveis
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
    # 2. INTELIGÊNCIA DE SEO (Tópicos Gerais)
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
        "SENIOR_LIVING": "🍷 Melhor Idade (Acessibilidade 60+)",
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

    # =====================================================
    # 3. MATRIZ DE PERSONAS (COMPLETA)
    # =====================================================
    PERSONAS = {
        # --- ELITE / TOPO DA LISTA (PRIORITÁRIOS) ---
        "CITIZEN_GENERAL": {
            "cluster_ref": "PORTAL", 
            "nome": "🏙️ CIDADÃO DE INDAIATUBA (Informação Geral)",
            "dor": "Desinformação sobre o que acontece na cidade e oportunidades perdidas.",
            "desejo": "Saber sobre obras, trânsito, eventos, utilidade pública e valorização do seu bairro."
        },
        "INVESTOR_SHARK_ROI": {
            "cluster_ref": "INVESTOR",
            "nome": "🦈 INVESTIDOR TUBARÃO (Foco em Yield)",
            "dor": "Dinheiro parado no CDI perdendo para inflação real e medo de vacância.",
            "desejo": "Ativos com liquidez comprovada, dados matemáticos de valorização e Cap Rate acima da média."
        },
        "EXODUS_SP_ELITE_FAMILY": {
            "cluster_ref": "HIGH_END",
            "nome": "✈️ ÊXODO SÃO PAULO (Fuga da Capital)",
            "dor": "Insegurança extrema em SP, filhos presos em apartamento e poluição.",
            "desejo": "Condomínio fechado com segurança armada, escolas bilingues e qualidade de vida imediata."
        },
        "FIRST_HOME_DREAMER": {
            "cluster_ref": "URBAN",
            "nome": "🔑 1º IMÓVEL (Casal Jovem)",
            "dor": "Medo de comprometer a renda por 30 anos e comprar um imóvel que desvalorize.",
            "desejo": "Entrada facilitada, bairro com potencial de crescimento e baixo custo de condomínio."
        },
        "LUXURY_PRIVACY_SEEKER": {
            "cluster_ref": "HIGH_END",
            "nome": "💎 OLD MONEY (Busca Privacidade)",
            "dor": "Exposição excessiva, vizinhos barulhentos e falta de exclusividade.",
            "desejo": "Terrenos duplos ou de esquina, vista para mata preservada, arquitetura autoral e silêncio absoluto."
        },
        "COMMERCIAL_LOGISTICS_BOSS": {
            "cluster_ref": "LOGISTICS",
            "nome": "🚚 GIGANTE DA LOGÍSTICA (CEO/Diretor)",
            "dor": "Custo do 'Last Mile', falta de mão de obra local e trânsito para escoar carga.",
            "desejo": "Proximidade da SP-75/Viracopos, pé direito de 12m e incentivos fiscais."
        },
        "PET_PARENT_PREMIUM": {
            "cluster_ref": "FAMILY",
            "nome": "🐾 DONO DE ANIMAIS (Pet Lover)",
            "dor": "Dificuldade em encontrar condomínios com quintais e regras flexíveis para animais grandes.",
            "desejo": "Casa com amplo quintal gramado, próxima a 'Pet Places' e parques."
        },

        # --- CLÁSSICOS & RESTAURADOS (SEQUÊNCIA) ---
        "HYBRID_COMMUTER": {
            "cluster_ref": "URBAN",
            "nome": "🚗 O PENDULAR (Trabalha em SP/Campinas)",
            "dor": "Cansaço da estrada diária e tempo perdido no trânsito urbano até a rodovia.",
            "desejo": "Acesso imediato à Rodovia Santos Dumont (SP-75) e serviços rápidos na saída da cidade."
        },
        "REMOTE_WORKER_TECH": {
            "cluster_ref": "URBAN",
            "nome": "💻 NÔMADE DIGITAL / HOME OFFICE",
            "dor": "Apartamentos apertados sem isolamento acústico para reuniões e internet instável.",
            "desejo": "Cômodo extra para escritório (3º dormitório), vista livre e fibra ótica de alta velocidade."
        },
        "MEDICAL_PRO_HEALTH": {
            "cluster_ref": "HIGH_END",
            "nome": "🩺 MÉDICO / PROFISSIONAL DE SAÚDE",
            "dor": "Rotina exaustiva de plantões, necessidade de silêncio absoluto para descanso.",
            "desejo": "Proximidade do Hospital HAOC/Santa Ignês e suíte master com isolamento acústico."
        },
        "ACTIVE_RETIREE": {
            "cluster_ref": "FAMILY",
            "nome": "🍷 MELHOR IDADE ATIVA",
            "dor": "Casas com muitas escadas, manutenção difícil e solidão.",
            "desejo": "Casa térrea prática, próxima a farmácias, mercados e convivência social."
        },
        "INVESTOR_CONSERVATIVE": {
            "cluster_ref": "INVESTOR",
            "nome": "🛡️ INVESTIDOR CONSERVADOR (Patrimônio)",
            "dor": "Medo de arriscar em mercado financeiro e perder o principal.",
            "desejo": "Imóvel físico ('tijolo'), segurança jurídica total e reserva de valor para os filhos."
        },
        "INVESTOR_FLIP": {
            "cluster_ref": "INVESTOR",
            "nome": "🛠️ INVESTIDOR DE REFORMA (Flipper)",
            "dor": "Margem de lucro apertada em imóveis prontos.",
            "desejo": "Imóvel depreciado em boa localização para reformar e vender com margem."
        },
        "COUNTRYSIDE_LIFESTYLE": {
            "cluster_ref": "RURAL_LIFESTYLE",
            "nome": "🌿 ESTILO DE VIDA CAMPESTRE (Chácaras)",
            "dor": "Estresse da cidade grande e falta de contato com a natureza.",
            "desejo": "Chácara em condomínio (segurança) com espaço para horta e lazer."
        }
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

    # =====================================================
    # CATÁLOGOS
    # =====================================================
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
