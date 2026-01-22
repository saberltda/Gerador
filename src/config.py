# src/config.py

class GenesisConfig:
    VERSION = "GERADOR V.56.0 (TONE & STRUCTURE SYNC)"

    COLOR_PRIMARY = "#003366"
    COLOR_ACTION  = "#28a745"
    GRADIENT_CTA  = "linear-gradient(135deg, #003366 0%, #001a33 100%)"
    BLOG_URL = "https://blog.saber.imb.br"
    FUSO_PADRAO = "-03:00"

    # ... (RULES e STRICT_GUIDELINES permanecem iguais) ...
    RULES = {
        "INDUSTRIAL_RESTRICTION": ["Casa de Rua", "Casa em Condomínio", "Apartamento", "Apartamento 2 ou 3 dormitórios", "Casa térrea de rua", "Sobrado em bairro residencial aberto", "Cobertura", "Studio residencial"],
        "OPEN_NEIGHBORHOOD_RESTRICTION": ["Condomínio Fechado", "Portaria 24h", "Portaria 24 horas", "Acesso controlado", "Controle de acesso", "Lazer Completo", "Área de lazer completa"],
        "FORBIDDEN_WORDS": ["sonho", "sonhos", "oportunidade única", "excelente localização", "ótimo investimento", "preço imperdível", "lindo", "maravilhoso", "tranquilo", "localização privilegiada", "região privilegiada", "venha conferir", "agende sua visita", "paraíso", "espetacular", "imóvel dos sonhos", "toque de requinte", "locação", "aluguel", "alugar", "inquilino", "fiador", "locatário"],
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

    # ... (TOPICS_MAP e WEIGHTS permanecem iguais da última atualização) ...
    TOPICS_MAP = {
        "MERCADO_DADOS": "📈 Dados de Mercado e Rentabilidade",
        "INVESTIMENTO_ROI": "💰 Lucro e Valorização de Patrimônio",
        "FINANCAS_TOKEN": "💳 Potencial de Financiamento e Crédito",
        "SUSTENTABILIDADE_ESG": "🌱 Sustentabilidade e Economia Verde",
        "LOCALIZACAO_PREMIUM": "📍 Localização e Facilidade de Acesso",
        "LUXO_COMPACTO": "💎 Luxo e Design Exclusivo",
        "CIDADES_INTELIGENTES": "🏙️ Infraestrutura Urbana e Modernidade",
        "HOME_OFFICE_FLEX": "💻 Espaço para Trabalho e Flexibilidade",
        "LOGISTICA_HUB": "🚚 Logística e Proximidade com Aeroporto",
        "BEM_ESTAR_BIOFILIA": "🌿 Saúde, Bem-Estar e Natureza",
        "SENIOR_LIVING": "🍷 Qualidade de Vida na Melhor Idade",
        "SEGURANCA_TECH": "🛡️ Segurança e Monitoramento Inteligente",
        "SHORT_STAY": "🧳 Aluguel por Temporada e Renda Extra",
        "PETS_GARDEN": "🐾 Espaço para Animais e Quintal",
        "SMART_HOME": "📱 Casa Inteligente e Tecnologia",
        "JURIDICO_SEGURANCA": "⚖️ Segurança Jurídica e Documentação",
        "ARQUITETURA_FACHADA": "🎨 Arquitetura e Estilo da Fachada",
        "COMUNIDADE_VIZINHANCA": "🤝 Vizinhança e Vida em Comunidade"
    }
    
    TOPICS_WEIGHTS = {"MERCADO_DADOS": 100} # Simplificado para exemplo

    # ... (PERSONAS permanecem iguais) ...
    PERSONAS = {
        "CITIZEN_GENERAL": {"cluster_ref": "PORTAL", "nome": "🏙️ CIDADÃO DE INDAIATUBA (Informação Geral)", "dor": "Desinformação sobre o que acontece na cidade e oportunidades perdidas.", "desejo": "Saber sobre obras, trânsito, eventos, utilidade pública e valorização do seu bairro."},
        "INVESTOR_SHARK_ROI": {"cluster_ref": "INVESTOR", "nome": "🦈 INVESTIDOR TUBARÃO (Foco em Yield)", "dor": "Dinheiro parado no CDI perdendo para inflação real e medo de vacância.", "desejo": "Ativos com liquidez comprovada, dados matemáticos de valorização e Cap Rate acima da média."},
        "EXODUS_SP_ELITE_FAMILY": {"cluster_ref": "HIGH_END", "nome": "✈️ ÊXODO SÃO PAULO (Fuga da Capital)", "dor": "Insegurança extrema em SP, filhos presos em apartamento e poluição.", "desejo": "Condomínio fechado com segurança armada, escolas bilingues e qualidade de vida imediata."},
        "FIRST_HOME_DREAMER": {"cluster_ref": "URBAN", "nome": "🔑 1º IMÓVEL (Casal Jovem)", "dor": "Medo de comprometer a renda por 30 anos e comprar um imóvel que desvalorize.", "desejo": "Entrada facilitada, bairro com potencial de crescimento e baixo custo de condomínio."},
        "LUXURY_PRIVACY_SEEKER": {"cluster_ref": "HIGH_END", "nome": "💎 OLD MONEY (Busca Privacidade)", "dor": "Exposição excessiva, vizinhos barulhentos e falta de exclusividade.", "desejo": "Terrenos duplos ou de esquina, vista para mata preservada, arquitetura autoral e silêncio absoluto."},
        "COMMERCIAL_LOGISTICS_BOSS": {"cluster_ref": "LOGISTICS", "nome": "🚚 GIGANTE DA LOGÍSTICA (CEO/Diretor)", "dor": "Custo do 'Last Mile', falta de mão de obra local e trânsito para escoar carga.", "desejo": "Proximidade da SP-75/Viracopos, pé direito de 12m e incentivos fiscais."},
        "PET_PARENT_PREMIUM": {"cluster_ref": "FAMILY", "nome": "🐾 DONO DE ANIMAIS (Pet Lover)", "dor": "Dificuldade em encontrar condomínios com quintais e regras flexíveis para animais grandes.", "desejo": "Casa com amplo quintal gramado, próxima a 'Pet Places' e parques."},
        "HYBRID_COMMUTER": {"cluster_ref": "URBAN", "nome": "🚗 O PENDULAR (Trabalha em SP/Campinas)", "dor": "Cansaço da estrada diária e tempo perdido no trânsito urbano até a rodovia.", "desejo": "Acesso imediato à Rodovia Santos Dumont (SP-75) e serviços rápidos na saída da cidade."},
        "REMOTE_WORKER_TECH": {"cluster_ref": "URBAN", "nome": "💻 NÔMADE DIGITAL / HOME OFFICE", "dor": "Apartamentos apertados sem isolamento acústico para reuniões e internet instável.", "desejo": "Cômodo extra para escritório (3º dormitório), vista livre e fibra ótica de alta velocidade."},
        "MEDICAL_PRO_HEALTH": {"cluster_ref": "HIGH_END", "nome": "🩺 MÉDICO / PROFISSIONAL DE SAÚDE", "dor": "Rotina exaustiva de plantões, necessidade de silêncio absoluto para descanso.", "desejo": "Proximidade do Hospital HAOC/Santa Ignês e suíte master com isolamento acústico."},
        "ACTIVE_RETIREE": {"cluster_ref": "FAMILY", "nome": "🍷 MELHOR IDADE ATIVA", "dor": "Casas com muitas escadas, manutenção difícil e solidão.", "desejo": "Casa térrea prática, próxima a farmácias, mercados e convivência social."},
        "INVESTOR_CONSERVATIVE": {"cluster_ref": "INVESTOR", "nome": "🛡️ INVESTIDOR CONSERVADOR (Patrimônio)", "dor": "Medo de arriscar em mercado financeiro e perder o principal.", "desejo": "Imóvel físico ('tijolo'), segurança jurídica total e reserva de valor para os filhos."},
        "INVESTOR_FLIP": {"cluster_ref": "INVESTOR", "nome": "🛠️ INVESTIDOR DE REFORMA (Flipper)", "dor": "Margem de lucro apertada em imóveis prontos.", "desejo": "Imóvel depreciado em boa localização para reformar e vender com margem."},
        "COUNTRYSIDE_LIFESTYLE": {"cluster_ref": "RURAL_LIFESTYLE", "nome": "🌿 ESTILO DE VIDA CAMPESTRE (Chácaras)", "dor": "Estresse da cidade grande e falta de contato com a natureza.", "desejo": "Chácara em condomínio (segurança) com espaço para horta e lazer."}
    }

    # =====================================================
    # 4. FORMATOS DE CONTEÚDO (RENOMEADOS E SINCRONIZADOS)
    # =====================================================
    CONTENT_FORMATS_MAP = {
        "GUIA_DEFINITIVO": "📘 Guia Definitivo (Manual Completo)",
        "LISTA_POLEMICA": "🔥 Lista Polêmica (Quebra de Mitos)",
        "COMPARATIVO_TECNICO": "⚖️ Comparativo Técnico (Batalha VS)",
        "INSIGHT_DE_CORRETOR": "💡 Insight de Bastidores (Segredos)",
        "PERGUNTAS_RESPOSTAS": "❓ Perguntas & Respostas (FAQ Direto)",
        "CENARIO_ANALITICO": "📊 Cenário Analítico (Foco em Dados)",
        "CHECKLIST_TECNICO": "✅ Checklist de Verificação",
        "PREVISAO_MERCADO": "🔮 Previsão de Futuro (Tendências)",
        "ROTINA_SUGERIDA": "📅 Rotina Sugerida (Storytelling)",
        "DATA_DRIVEN": "📈 Relatório Numérico (Estatístico)"
    }
    CONTENT_FORMATS = list(CONTENT_FORMATS_MAP.keys())

    # ... (GATILHOS e CATÁLOGOS permanecem iguais) ...
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

