# src/engine.py
import random
import copy
from .database import GenesisData
from .logic import PlanoDiretor, SEOHeatmap, RiscoJuridico, PortalSynchronizer
from .scanner import BlogScanner
from .config import GenesisConfig

class GenesisEngine:
    def __init__(self, data_instance):
        self.data = data_instance 
        self.plano = PlanoDiretor()
        self.heatmap = SEOHeatmap()
        self.risco_juridico = RiscoJuridico()
        self.scanner = BlogScanner()
        self.portal_sync = PortalSynchronizer() # Novo Cérebro de Sincronização

    def _selecionar_persona_compativel(self, cluster_key):
        candidatos = []
        for chave, persona in GenesisConfig.PERSONAS.items():
            refs = persona['cluster_ref']
            if not isinstance(refs, list): refs = [refs]
            if cluster_key in refs: candidatos.append(persona)
        
        if candidatos: return random.choice(candidatos)
        return GenesisConfig.PERSONAS.get("PET_PARENT_PREMIUM", GenesisConfig.PERSONAS["CITIZEN_GENERAL"])

    def _filtrar_bairros_por_cluster(self, cluster_key):
        todos_bairros = self.data.bairros
        candidatos = []
        for b in todos_bairros:
            z = b.get("zona_normalizada", "indefinido")
            match = False
            if cluster_key == "HIGH_END" and z in ["residencial_fechado", "chacaras_fechado"]: match = True
            elif cluster_key == "FAMILY" and z in ["residencial_fechado", "residencial_aberto", "chacaras_fechado"]: match = True
            elif cluster_key == "URBAN" and z in ["residencial_aberto", "mista"]: match = True
            elif cluster_key == "INVESTOR" and z in ["industrial", "residencial_fechado", "mista", "residencial_aberto"]: match = True
            elif cluster_key == "LOGISTICS" and z in ["industrial", "mista"]: match = True
            elif cluster_key == "CORPORATE" and z in ["mista", "industrial", "residencial_aberto"]: match = True
            elif cluster_key == "RURAL_LIFESTYLE" and "chacara" in z: match = True
            if match: candidatos.append(b)
        return candidatos if candidatos else todos_bairros

    def _escolher_topico_ponderado(self, tipo_pauta):
        """
        Seleciona o tópico baseado no universo correto (Imob ou Portal) usando pesos.
        Mantido para fallback ou uso específico.
        """
        opcoes = []
        pesos = []
        
        if tipo_pauta == "PORTAL":
            mapa = GenesisConfig.PORTAL_TOPICS_DISPLAY
            pesos_ref = GenesisConfig.PORTAL_TOPICS_WEIGHTS
        else:
            mapa = GenesisConfig.TOPICS_MAP
            pesos_ref = GenesisConfig.TOPICS_WEIGHTS

        for key, nome_display in mapa.items():
            opcoes.append(nome_display)
            pesos.append(pesos_ref.get(key, 50))
            
        return random.choices(opcoes, weights=pesos, k=1)[0]

    def run(self, user_selection: dict):
        self.scanner.mapear()
        historico_recente = self.scanner.get_ultimos_titulos(9999)

        tipo_pauta_code = user_selection.get("tipo_pauta", "IMOBILIARIA")
        eh_portal = (tipo_pauta_code == "PORTAL")

        # --- PASSO 1: CLUSTER & PERSONA ---
        persona_data = None
        cluster_ref = "FAMILY" 

        if user_selection['persona_key'] != "ALEATÓRIO":
            key = user_selection['persona_key']
            persona_data = GenesisConfig.PERSONAS[key]
            cluster_ref = persona_data['cluster_ref']
        else:
            if eh_portal:
                persona_data = GenesisConfig.PERSONAS["CITIZEN_GENERAL"]
                cluster_ref = "PORTAL"
            else:
                clusters_disponiveis = list(self.data.ativos_por_cluster.keys())
                pesos_cluster = [2.0 if c in ["HIGH_END", "INVESTOR", "LOGISTICS"] else 1.0 for c in clusters_disponiveis]
                cluster_ref = random.choices(clusters_disponiveis, weights=pesos_cluster, k=1)[0]
                persona_data = self._selecionar_persona_compativel(cluster_ref)

        # --- PASSO 2: BAIRRO ---
        bairro_selecionado = None
        modo = "CIDADE"
        obs_tecnica = f"Cluster: {cluster_ref}"

        if user_selection['bairro_nome'] != "ALEATÓRIO":
            if user_selection['bairro_nome'] == "FORCE_CITY_MODE": modo = "CIDADE"
            else:
                for b in self.data.bairros:
                    if b['nome'] == user_selection['bairro_nome']: bairro_selecionado = b; break
                if bairro_selecionado: modo = "BAIRRO"; obs_tecnica += " | Bairro Manual"
        else:
            # Lógica de seleção aleatória de bairro (se não for City Mode forçado pelo app.py)
            if not eh_portal: # Portal geralmente foca na cidade, mas pode ter bairro
                candidatos = self._filtrar_bairros_por_cluster(cluster_ref)
                ineditos = [b for b in candidatos if not self.scanner.ja_publicado(b["nome"])]
                if ineditos and random.random() < 0.75:
                    bairro_selecionado = random.choice(ineditos); obs_tecnica += " | Bairro Inédito"
                elif candidatos:
                    bairro_selecionado = random.choice(candidatos); obs_tecnica += " | Bairro Recorrente"
                if bairro_selecionado: modo = "BAIRRO"

        # --- PASSO 3 & 4 (DIVISÃO DE MUNDOS: PORTAL vs IMOBILIÁRIA) ---
        
        ativo_final = "INDEFINIDO"
        topico = "INDEFINIDO"
        formato = "INDEFINIDO"
        gatilho = "NEUTRAL_JOURNALISM"

        if eh_portal:
            # === MODO PORTAL SINCRONIZADO ===
            
            # Recupera seleções (que podem ser ALEATÓRIO ou chaves específicas)
            sel_ativo = user_selection.get('ativo', 'ALEATÓRIO') # Aqui 'ativo' é a Editoria
            sel_topico = user_selection.get('topico', 'ALEATÓRIO')
            sel_formato = user_selection.get('formato', 'ALEATÓRIO')

            # Verifica se é uma chave válida de editoria
            valid_editorias_keys = [k for k,v in self.portal_sync.get_editorias_display()]

            if sel_ativo != "ALEATÓRIO" and sel_ativo in valid_editorias_keys:
                # 1. Editoria Manual -> Sincronizar o resto
                editoria_key = sel_ativo
                editoria_label = GenesisConfig.PORTAL_MATRIX[editoria_key]['label']
                
                # Sincroniza Tópico
                valid_topics = [t[0] for t in self.portal_sync.get_valid_topics(editoria_key)]
                if sel_topico in valid_topics:
                    topico_key = sel_topico
                else:
                    topico_key = random.choice(valid_topics)

                # Sincroniza Formato
                valid_formats = [f[0] for f in self.portal_sync.get_valid_formats(editoria_key)]
                if sel_formato in valid_formats:
                    formato_key = sel_formato
                else:
                    formato_key = random.choice(valid_formats)

                ativo_final = editoria_label
                topico = GenesisConfig.PORTAL_TOPICS_DISPLAY.get(topico_key, topico_key)
                formato = formato_key
                obs_ref = "Sincronização Manual (Portal)"

            else:
                # 2. Tudo Aleatório -> Pacote Sincronizado Completo
                pack = self.portal_sync.get_random_set()
                ativo_final = pack['editoria'][1] # Label
                topico = pack['topico'][1]       # Label
                formato = pack['formato'][0]     # Key
                obs_ref = "Sorteio Sincronizado (Portal)"
            
            # Gatilho para Portal
            gatilho = "NEUTRAL_JOURNALISM" # Padrão
            
            obs_tecnica += f" | {obs_ref}"

        else:
            # === MODO IMOBILIÁRIA (ORIGINAL) ===

            # Ativo (Imóvel)
            if user_selection['ativo'] != "ALEATÓRIO":
                ativo_final = user_selection['ativo']
                obs_ref = "Ativo Manual"
                if modo == "BAIRRO" and bairro_selecionado:
                    ativo_final, obs_ajuste = self.plano.refinar_ativo(cluster_ref, bairro_selecionado, [ativo_final])
                    obs_ref += f" ({obs_ajuste})"
            else:
                lista_ativos = self.data.ativos_por_cluster.get(cluster_ref, ["IMÓVEL PADRÃO"])
                ativo_base = random.choice(lista_ativos)
                if modo == "BAIRRO" and bairro_selecionado:
                    ativo_final, obs_ajuste = self.plano.refinar_ativo(cluster_ref, bairro_selecionado, [ativo_base])
                    obs_ref = obs_ajuste
                else: 
                    ativo_final = ativo_base; obs_ref = "Sorteio Simples"
            obs_tecnica += f" | {obs_ref}"

            # Tópico
            if user_selection['topico'] != "ALEATÓRIO": 
                topico = user_selection['topico']
            else: 
                topico = self._escolher_topico_ponderado(tipo_pauta_code)

            # Formato
            if user_selection['formato'] != "ALEATÓRIO": 
                formato = user_selection['formato']
            else: 
                formato = random.choice(GenesisConfig.REAL_ESTATE_FORMATS_MAP.keys() if hasattr(GenesisConfig, 'REAL_ESTATE_FORMATS_MAP') else GenesisConfig.CONTENT_FORMATS)
                # Fallback para chaves se dicionário, ou lista direta

            # Gatilho
            if user_selection['gatilho'] != "ALEATÓRIO": 
                gatilho = user_selection['gatilho']
            else: 
                gatilho = random.choice(list(GenesisConfig.EMOTIONAL_TRIGGERS_MAP.values()))

        return {
            "modo": modo, 
            "bairro": bairro_selecionado, 
            "cluster_tecnico": cluster_ref,
            "ativo_definido": ativo_final, 
            "topico": topico, 
            "persona": persona_data,
            "formato": formato, 
            "gatilho": gatilho, 
            "obs_tecnica": obs_tecnica,
            "historico_titulos": historico_recente, 
            "tipo_pauta": tipo_pauta_code
        }
