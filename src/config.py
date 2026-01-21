# src/config.py

class GenesisConfig:
    VERSION = "GERADOR V.8.2 (ANTI-ALUCINAÇÃO)"

    # Design System & URLs
    COLOR_PRIMARY = "#003366"   # Azul Saber
    BLOG_URL = "https://blog.saber.imb.br"
    FUSO_PADRAO = "-03:00"

    # =====================================================
    # 1. INTELIGÊNCIA DE SEO (Tópicos Gerais)
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
    # 2. REGRAS DE SEGURANÇA (ATUALIZADO)
    # =====================================================
    STRICT_GUIDELINES = [
        "NUNCA invente nomes de clientes (ex: Ricardo, Ana, João).",
        "NUNCA invente profissões específicas para o personagem.",
        "NUNCA crie depoimentos falsos.",
        
        # --- CORREÇÃO DE ALUCINAÇÃO GEOGRÁFICA ---
        "ALERTA GEOGRÁFICO CRÍTICO: Bairros com nomes parecidos podem ser distantes.",
        "EXEMPLO DE ERRO A EVITAR: 'Jardim do Sol' e 'Jardim Morada do Sol' ficam em extremos opostos da cidade. NUNCA diga que são vizinhos.",
        "OBRIGATÓRIO: Verifique a distância real no Google Maps Mental antes de citar proximidade.",
        
        # --- REGRAS ANTI-ANÚNCIO ---
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
            "imóvel dos sonhos", "toque de requinte",
            # --- PROIBIÇÕES DE LOCAÇÃO (SOMENTE VENDAS) ---
            "locação", "aluguel", "alugar", "inquilino", "fiador", "locatário"
        ]
    }

    # =====================================================
    # 3. MATRIZ DE PERSONAS
    # =====================================================
    PERSONAS = {
        # ---------------------------------------------------------------------
        # 🏆 TIER 0: PERSONA UNIVERSAL (DEFAULT)
        # ---------------------------------------------------------------------
        "CITIZEN_GENERAL": {
            "cluster_ref": "PORTAL", 
            "nome": "🏙️ CIDADÃO DE INDAIATUBA (Informação Geral)",
            "dor": "Desinformação sobre o que acontece na cidade e oportunidades perdidas.",
            "desejo": "Saber sobre obras, trânsito, eventos, utilidade pública e valorização do seu bairro."
        },

        # ---------------------------------------------------------------------
        # 🚨 TIER 1: SEO CRÍTICO & ALTO VOLUME (TOPO DA CADEIA ALIMENTAR)
        # ---------------------------------------------------------------------
        "INVESTOR_SHARK_ROI": {
            "cluster_ref": "INVESTOR",
            "nome": "🦈 INVESTIDOR SHARK (Foco em Yield)",
            "dor": "Dinheiro parado no CDI perdendo para inflação real e medo de vacância.",
            "desejo": "Ativos com liquidez comprovada, dados matemáticos de valorização e Cap Rate acima de 0.6%."
        },
        "EXODUS_SP_ELITE_FAMILY": {
            "cluster_ref": "HIGH_END",
            "nome": "✈️ EXODUS ELITE SP (A Fuga da Capital)",
            "dor": "Insegurança extrema em SP (blindados), filhos presos em apartamento e poluição.",
            "desejo": "Condomínio fechado com segurança armada, escolas internacionais (bilingues) e qualidade de vida imediata."
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

        # ---------------------------------------------------------------------
        # 🧬 TIER 2: NICHOS DE ESTILO DE VIDA (LONG TAIL)
        # ---------------------------------------------------------------------
        "digital_nomad_tech": {
            "cluster_ref": "URBAN",
            "nome": "💻 Nômade Digital / Tech Lead",
            "dor": "Internet instável em bairros afastados e falta de delivery/serviços 24h.",
            "desejo": "Fibra ótica dedicada, cômodo isolado (Zoom-ready) e iFood/Rappi funcionando perfeitamente."
        },
        "pet_parent_heavy_user": {
            "cluster_ref": "FAMILY",
            "nome": "🐾 Pet Parent (Muitos Cães)",
            "dor": "Condomínios com regras restritivas e apartamentos sem área externa.",
            "desejo": "Garden ou casa com quintal gramado seguro (muro alto) e parques pet-friendly próximos."
        },
        "eco_conscious_buyer": {
            "cluster_ref": "HIGH_END",
            "nome": "🌿 O Comprador Eco-Consciente (ESG)",
            "dor": "Desperdício energético (conta de luz alta) e construções que destroem a natureza.",
            "desejo": "Energia fotovoltaica já instalada, cisterna, ventilação cruzada e entorno verde."
        },
        "minimalist_urban": {
            "cluster_ref": "URBAN",
            "nome": "🚶 O Minimalista Urbano (Sem Carro)",
            "dor": "Dependência de carro para comprar pão ou ir à academia.",
            "desejo": "Faça tudo a pé (Walkability score alto), perto do Parque Ecológico e serviços essenciais."
        },
        "weekend_hobby_farmer": {
            "cluster_ref": "RURAL_LIFESTYLE",
            "nome": "👨‍🌾 Fazendeiro de Fim de Semana",
            "dor": "Estresse corporativo e falta de conexão com a terra durante a semana.",
            "desejo": "Chácara em Itaici com pomar, internet boa (para emergências) e fácil acesso (sem estrada de terra ruim)."
        },

        # ---------------------------------------------------------------------
        # 🔄 TIER 3: MOMENTOS DE VIDA (SITUACIONAL)
        # ---------------------------------------------------------------------
        "newly_divorced_restart": {
            "cluster_ref": "URBAN",
            "nome": "💔 Recomeço (Recém Separado)",
            "dor": "Necessidade urgente de mudar, orçamento ajustado pós-partilha e solidão.",
            "desejo": "Apartamento pronto (sem reforma), prático, em área movimentada e socialmente ativa."
        },
        "empty_nesters_downsizing": {
            "cluster_ref": "HIGH_END",
            "nome": "🍷 Ninho Vazio (Downsizing)",
            "dor": "Manutenção de casarão vazio e escadas que começam a cansar.",
            "desejo": "Casa térrea de alto padrão ou apartamento de luxo, menor, mas sofisticado e seguro."
        },
        "university_parents_investor": {
            "cluster_ref": "INVESTOR",
            "nome": "🎓 Pais de Universitário (Unimax)",
            "dor": "Pagar aluguel caro por 5 anos de curso de Medicina/Direito.",
            "desejo": "Comprar imóvel para o filho morar e depois virar renda passiva (investimento híbrido)."
        },
        "growing_family_upgrade": {
            "cluster_ref": "FAMILY",
            "nome": "🤰 Família em Expansão (Bebê a caminho)",
            "dor": "Apartamento ficou pequeno, falta de quarto para o bebê e bagunça visível.",
            "desejo": "Upgrade para 3 dormitórios, varanda gourmet e brinquedoteca no condomínio."
        },
        "accessibility_priority": {
            "cluster_ref": "FAMILY",
            "nome": "♿ Acessibilidade Total (PNE/Idoso)",
            "dor": "Degraus, portas estreitas e banheiros inadaptados.",
            "desejo": "Casa 100% plana, portas largas, banheiros adaptáveis e rampas de acesso."
        },

        # ---------------------------------------------------------------------
        # 💼 TIER 4: PROFISSIONAIS ESPECÍFICOS
        # ---------------------------------------------------------------------
        "doctor_on_call": {
            "cluster_ref": "HIGH_END",
            "nome": "⚕️ Médico Plantonista (HAOC/Santa Ignês)",
            "dor": "Tempo de deslocamento em emergências e barulho durante descanso diurno.",
            "desejo": "Proximidade extrema dos hospitais (max 5 min), silêncio absoluto (janelas anti-ruído) e blackout."
        },
        "commercial_business_owner": {
            "cluster_ref": "CORPORATE",
            "nome": "👔 Dono de Pequena Empresa/Comércio",
            "dor": "Aluguel comercial instável e falta de visibilidade para o negócio.",
            "desejo": "Imóvel comercial próprio em avenida de fluxo ou sala comercial em prédio de prestígio."
        },
        "airbnb_host_pro": {
            "cluster_ref": "INVESTOR",
            "nome": "🧳 Anfitrião Profissional (Short Stay)",
            "dor": "Condomínios que proíbem Airbnb e vacância em baixa temporada.",
            "desejo": "Studios perto do Distrito Industrial ou Centro, prédios permissivos e decoração 'instagramável'."
        },
        "land_banker_speculator": {
            "cluster_ref": "INVESTOR",
            "nome": "🗺️ Land Banker (Especulador de Terra)",
            "dor": "Comprar no topo do preço e liquidez travada.",
            "desejo": "Loteamentos em pré-lançamento, áreas de expansão urbana futura e valorização de longo prazo."
        },
        "flipper_renovator": {
            "cluster_ref": "INVESTOR",
            "nome": "🛠️ O Flipper (Reformar para Vender)",
            "dor": "Encontrar a 'oportunidade' certa e estourar orçamento de obra.",
            "desejo": "Imóvel 'feio' (desatualizado) em localização nobre com desconto agressivo para reforma cosmética."
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
    # 5. GATILHOS MENTAIS
    # =====================================================
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
    # 6. CATÁLOGO DE IMÓVEIS (MODO IMOBILIÁRIA)
    # =====================================================
    # REMOVIDO TODO TERMO DE "LOCAÇÃO" PARA EVITAR ALUCINAÇÃO
    ASSETS_CATALOG = {
        "HIGH_END": [
            "MANSÃO EM CONDOMÍNIO (4+ Suítes)",
            "CASA TÉRREA ALTO PADRÃO (3 Suítes)",
            "SOBRADO NEO CLÁSSICO (Piscina Privativa)",
            "CASA DE ESQUINA (Terreno Ampliado)",
            "Lote em Condomínio de Luxo (>500m²)",
            "Casa com Vista para Mata (Privacidade Total)"
        ],
        "FAMILY": [
            "CASA EM CONDOMÍNIO (3 Dormitórios / 1 Suíte)",
            "CASA EM CONDOMÍNIO (2 Dormitórios / Entrada Facilitada)",
            "SOBRADO COM ÁREA GOURMET (3 Dormitórios)",
            "CASA TÉRREA (Acessibilidade Total)",
            "Casa de Rua em Bairro Planejado (3 Dorms)",
            "Villagio / Casas Geminadas (2 Dormitórios)"
        ],
        "URBAN": [
            "APARTAMENTO 3 DORMITÓRIOS (Família)",
            "APARTAMENTO 2 DORMITÓRIOS (Varanda Gourmet)",
            "COBERTURA DUPLEX (Vista Panorâmica)",
            "APARTAMENTO GARDEN (Quintal Suspenso)",
            "Studio / Loft Moderno (Investimento)",
            "Apartamento Compacto (1 Dormitório Central)"
        ],
        "INVESTOR": [
            "TERRENO EM CONDOMÍNIO (Lote Padrão 300m²)",
            "TERRENO DE ESQUINA (Potencial Construtivo)",
            "Imóvel para Reforma (Flip/Retrofit)",
            "Kitnet / Studio para Renda Passiva (Investimento)", # Corrigido de Locação
            "Terreno Comercial em Avenida (Visibilidade)",
            "Área para Incorporação Vertical (>1.000m²)"
        ],
        "LOGISTICS": [
            "GALPÃO INDUSTRIAL AAA (Pé Direito 12m)",
            "TERRENO INDUSTRIAL (Z1/Z2)",
            "Condomínio Logístico (Módulo Flexível)",
            "Galpão Comercial (Frente Rodovia)",
            "Área para Centro de Distribuição (Last Mile)",
            "Barracão Comercial Padrão (Pequeno Porte)"
        ],
        "RURAL_LIFESTYLE": [
            "CHÁCARA EM ITAICI (Lazer Completo)",
            "SÍTIO OU HARAS (Helvetia - Alto Padrão)",
            "Chácara em Condomínio Fechado (Segurança)",
            "Terreno de Chácara (1.000m² a 5.000m²)",
            "Casa de Campo com Pomar Formado"
        ],
        "CORPORATE": [
            "Sala Comercial em Prédio Corporativo",
            "Laje Corporativa Open Space",
            "Casa Comercial em Avenida",
            "Prédio Monousuário"
        ]
    }

    # =====================================================
    # 7. CATÁLOGO DO PORTAL (NOVO - MODO PORTAL)
    # =====================================================
    PORTAL_CATALOG = {
        "NOTICIAS": [
            "📰 Notícia de Trânsito / Obras Viárias",
            "📰 Notícia sobre Segurança Pública",
            "📰 Nova Lei Municipal (Aprovada ou em Pauta)",
            "📰 Evento Cultural / Agenda da Cidade",
            "📰 Inauguração de Novo Comércio/Serviço",
            "📰 Clima e Tempo (Alerta Defesa Civil)"
        ],
        "UTILIDADE": [
            "💡 Utilidade Pública (Água/Luz/Impostos)",
            "💉 Campanha de Saúde / Vacinação",
            "🏫 Matrículas Escolares e Educação",
            "🐕 Causa Animal / Adoção de Pets",
            "♻️ Coleta de Lixo e Reciclagem"
        ],
        "CURIOSIDADES": [
            "🏛️ História de Indaiatuba (Bairros Antigos)",
            "🌳 Parques e Áreas de Lazer (Guia)",
            "🍽️ Dicas de Gastronomia Local",
            "🚌 Mobilidade Urbana e Transporte Público"
        ]
    }
