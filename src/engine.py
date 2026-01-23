# src/engine.py
import random
import copy
from .database import GenesisData
from .logic import PlanoDiretor, SEOHeatmap, RiscoJuridico, PortalSynchronizer, RealEstateSynchronizer
from .scanner import BlogScanner
from .config import GenesisConfig

class GenesisEngine:
    def __init__(self, data_instance):
        self.data = data_instance 
        self.plano = PlanoDiretor()
        self.heatmap = SEOHeatmap()
        self.risco_juridico = RiscoJuridico()
        self.scanner = BlogScanner()
        self.portal_sync = PortalSynchronizer()
        self.imob_sync = RealEstateSynchronizer() # Novo Cérebro Imobiliário

    def _selecionar_persona_compativel(self, cluster_key):
        candidatos = []
        for chave, persona in GenesisConfig.PERSONAS.items():
            refs = persona['cluster_ref']
            if not isinstance(refs, list): refs = [refs]
            if cluster_key in refs: candidatos.append(persona)
        
        if candidatos: return random.choice(candidatos)
        # Fallback inteligente
        return GenesisConfig.PERSONAS.get("EXODUS_SP_ELITE_FAMILY", list(GenesisConfig.PERSONAS.values())[0])

    def _filtrar_bairros_por_cluster(self, cluster_key):
        todos_bairros = self.data.bairros
        candidatos = []
        for b in todos_bairros:
            z = b.get("zona_normalizada", "indefinido")
            match = False
            # Lógica de compatibilidade Cluster <-> Zona
            if cluster_key == "HIGH_END" and z in ["residencial_fechado", "chacaras_fechado"]: match = True
            elif cluster_key == "FAMILY" and z in ["residencial_fechado", "residencial_aberto"]: match = True
            elif cluster_key == "URBAN" and z in ["residencial_aberto", "mista"]: match = True
            elif cluster_key == "INVESTOR" and z in ["industrial", "residencial_fechado", "mista", "residencial_aberto"]: match = True
            elif cluster_key == "LOGISTICS" and z in ["industrial", "mista"]: match = True
            elif cluster_key == "CORPORATE" and z in ["mista", "industrial", "residencial_aberto"]: match = True
            elif cluster_key == "RURAL_LIFESTYLE" and "chacara" in z: match = True
            if match: candidatos.append(b)
        return candidatos if candidatos else todos_bairros

    def run(self, user_selection: dict):
        self.scanner.mapear()
        historico_recente = self.scanner.get_ultimos_titulos(9999)

        tipo_pauta_code = user_selection.get("tipo_pauta", "IMOBILIARIA")
        eh_portal = (tipo_pauta_code == "PORTAL")

        # Variáveis de saída padrão
        modo = "CIDADE"
        obs_tecnica = ""
        ativo_final = "INDEFINIDO"
        topico = "INDEFINIDO"
        formato = "INDEFINIDO"
        gatilho = "ALEATÓRIO"
        persona_data = None
        cluster_ref = None
        bairro_selecionado = None

        # =========================================================
        # MODO PORTAL (Lógica Sincronizada)
        # =========================================================
        if eh_portal:
            persona_data = GenesisConfig.PERSONAS["CITIZEN_GENERAL"]
            cluster_ref = "PORTAL"
            
            # --- Seleção Sincronizada ---
            # 'ativo' vem como a Chave da Editoria
            sel_editoria = user_selection.get('ativo', 'ALEATÓRIO') 
            sel_topico = user_selection.get('topico', 'ALEATÓRIO')
            sel_formato = user_selection.get('formato', 'ALEATÓRIO')

            valid_keys = [k for k,v in self.portal_sync.get_editorias_display()]

            if sel_editoria != "ALEATÓRIO" and sel_editoria in valid_keys:
                editoria_key = sel_editoria
                editoria_label = GenesisConfig.PORTAL_MATRIX[editoria_key]['label']
                
                # Sincroniza Tópico
                valid_t = [t[0] for t in self.portal_sync.get_valid_topics(editoria_key)]
                topico_key = sel_topico if sel_topico in valid_t else random.choice(valid_t)

                # Sincroniza Formato
                valid_f = [f[0] for f in self.portal_sync.get_valid_formats(editoria_key)]
                formato_key = sel_formato if sel_formato in valid_f else random.choice(valid_f)

                ativo_final = editoria_label
                topico = GenesisConfig.PORTAL_TOPICS_DISPLAY.get(topico_key, topico_key)
                formato = formato_key
                obs_ref = "Manual (Sync)"
            else:
                pack = self.portal_sync.get_random_set()
                ativo_final = pack['editoria'][1]
                topico = pack['topico'][1]
                formato = pack['formato'][0]
                obs_ref = "Auto (Sync)"
            
            gatilho = "NEUTRAL_JOURNALISM"
            obs_tecnica = f"{obs_ref}"
            
            # Bairro geralmente é Cidade, mas aceita input
            if user_selection.get('bairro_nome') == "FORCE_CITY_MODE": modo = "CIDADE"
            else: modo = "CIDADE" # Portal default

        # =========================================================
        # MODO IMOBILIÁRIA (Lógica Sincronizada V2)
        # =========================================================
        else:
            # Recupera Inputs da UI
            # Agora 'ativo' na UI do Imob é a CATEGORIA/CLUSTER (Parent)
            # E temos um campo novo 'sub_ativo' para o imóvel específico (Child)
            sel_cluster = user_selection.get('ativo', 'ALEATÓRIO') # Parent
            sel_asset = user_selection.get('sub_ativo', 'ALEATÓRIO') # Child 1
            sel_topico = user_selection.get('topico', 'ALEATÓRIO') # Child 2
            sel_formato = user_selection.get('formato', 'ALEATÓRIO') # Child 3
            
            valid_clusters = [k for k,v in self.imob_sync.get_clusters_display()]
            
            # 1. Definição do Cluster (Categoria)
            if sel_cluster != "ALEATÓRIO" and sel_cluster in valid_clusters:
                cluster_ref = sel_cluster
                # Seleciona Persona baseada no cluster escolhido
                persona_data = self._selecionar_persona_compativel(cluster_ref)
                
                # Sincroniza Ativo (Imóvel Específico)
                valid_assets = self.imob_sync.get_valid_assets(cluster_ref)
                ativo_final = sel_asset if sel_asset in valid_assets else random.choice(valid_assets)
                
                # Sincroniza Tópico
                valid_t = [t[0] for t in self.imob_sync.get_valid_topics(cluster_ref)]
                topico_key = sel_topico if sel_topico in valid_t else random.choice(valid_t)
                topico = GenesisConfig.REAL_ESTATE_TOPICS_DISPLAY.get(topico_key, topico_key)
                
                # Sincroniza Formato
                valid_f = [f[0] for f in self.imob_sync.get_valid_formats(cluster_ref)]
                formato_key = sel_formato if sel_formato in valid_f else random.choice(valid_f)
                formato = GenesisConfig.REAL_ESTATE_FORMATS_DISPLAY.get(formato_key, formato_key)
                
                obs_ref = f"Manual ({cluster_ref})"
            
            else:
                # Tudo Aleatório Sincronizado
                pack = self.imob_sync.get_random_set()
                cluster_ref = pack['cluster'][0]
                ativo_final = pack['ativo']
                topico = pack['topico'][1]
                formato = pack['formato'][1]
                persona_data = self._selecionar_persona_compativel(cluster_ref)
                obs_ref = f"Auto ({cluster_ref})"

            # 2. Definição do Bairro (Compatível com o Cluster)
            if user_selection['bairro_nome'] != "ALEATÓRIO":
                if user_selection['bairro_nome'] == "FORCE_CITY_MODE": 
                    modo = "CIDADE"
                else:
                    for b in self.data.bairros:
                        if b['nome'] == user_selection['bairro_nome']: bairro_selecionado = b; break
                    if bairro_selecionado: modo = "BAIRRO"
            else:
                candidatos = self._filtrar_bairros_por_cluster(cluster_ref)
                ineditos = [b for b in candidatos if not self.scanner.ja_publicado(b["nome"])]
                if ineditos and random.random() < 0.75:
                    bairro_selecionado = random.choice(ineditos); obs_tecnica += " | Bairro Inédito"
                elif candidatos:
                    bairro_selecionado = random.choice(candidatos); obs_tecnica += " | Bairro Recorrente"
                if bairro_selecionado: modo = "BAIRRO"

            # Refinamento Final do Ativo com o Bairro (Check Físico)
            if modo == "BAIRRO" and bairro_selecionado:
                ativo_final, obs_ajuste = self.plano.refinar_ativo(cluster_ref, bairro_selecionado, [ativo_final])
                obs_ref += f" -> {obs_ajuste}"

            # Gatilho
            if user_selection.get('gatilho', 'ALEATÓRIO') != "ALEATÓRIO":
                gatilho = user_selection['gatilho']
            else:
                gatilho = random.choice(list(GenesisConfig.EMOTIONAL_TRIGGERS_MAP.values()))

            obs_tecnica = obs_ref

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
