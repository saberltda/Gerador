# src/engine.py
import random
import csv
import datetime
import os
from .config import GenesisConfig
from .logic import PlanoDiretor
from .scanner import BlogScanner

class GenesisEngine:
    def __init__(self, data_instance):
        self.data = data_instance
        self.config = GenesisConfig()
        self.plano = PlanoDiretor()
        self.scanner = BlogScanner()
        self.log_file = "historico_geracao.csv"

    def _salvar_log(self, dados: dict, data_pub_usuario: datetime.date):
        file_exists = os.path.isfile(self.log_file)
        bairro_nome = dados['bairro']['nome'] if dados['bairro'] else "N/A (Cidade)"
        formato_tecnico = dados['formato']
        formato_bonito = self.config.CONTENT_FORMATS_MAP.get(formato_tecnico, formato_tecnico)
        gatilho_tecnico = dados['gatilho']
        gatilho_bonito = self.config.EMOTIONAL_TRIGGERS_MAP.get(gatilho_tecnico, gatilho_tecnico)
        tipo_pauta = dados.get('tipo_pauta', 'INDEFINIDO')
        
        data_pub_str = data_pub_usuario.strftime("%Y-%m-%d")
        fuso_br = datetime.timezone(datetime.timedelta(hours=-3))
        data_criacao_str = datetime.datetime.now(fuso_br).strftime("%Y-%m-%d %H:%M:%S")

        # Adicionada coluna TIPO_PAUTA para facilitar filtro futuro
        linha = [
            data_pub_str, data_criacao_str, tipo_pauta, dados['persona']['nome'],
            bairro_nome, dados['topico'], dados['ativo_definido'],
            formato_bonito, gatilho_bonito
        ]
        try:
            with open(self.log_file, mode='a', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f, delimiter=';')
                if not file_exists:
                    writer.writerow(["DATA_PUB", "CRIADO_EM", "TIPO_PAUTA", "PERSONA", "BAIRRO", "TOPICO", "ATIVO", "FORMATO", "GATILHO"])
                writer.writerow(linha)
        except Exception as e:
            print(f"Erro log: {e}")

    def run(self, user_selection: dict):
        """
        user_selection espera:
        {
            "tipo_pauta": "PORTAL" ou "IMOBILIARIA" (CÓDIGO FIXO),
            "persona_key": "ALEATÓRIO" ou chave str,
            ...
        }
        """
        # 1. Atualiza Scanner
        self.scanner.mapear()
        historico_recente = self.scanner.get_ultimos_titulos(20)

        # Captura o CÓDIGO DO TIPO DA PAUTA (Vem limpo do app.py)
        tipo_pauta_code = user_selection.get("tipo_pauta", "IMOBILIARIA")
        eh_portal = (tipo_pauta_code == "PORTAL")

        # 2. Persona
        if user_selection['persona_key'] != "ALEATÓRIO":
            persona_key = user_selection['persona_key']
        else:
            persona_key = random.choice(list(self.config.PERSONAS.keys()))
        persona_data = self.config.PERSONAS[persona_key]
        cluster_ref = persona_data.get("cluster_ref", "FAMILY")

        # 3. Bairro (Lógica unificada)
        bairro_selecionado = None
        modo = "CIDADE"
        obs_tecnica = "Foco Macro (Cidade)"

        if user_selection['bairro_nome'] != "ALEATÓRIO":
            if user_selection['bairro_nome'] == "FORCE_CITY_MODE":
                modo = "CIDADE"
                obs_tecnica = "Usuário forçou modo Cidade"
            else:
                for b in self.data.bairros:
                    if b['nome'] == user_selection['bairro_nome']:
                        bairro_selecionado = b
                        break
                if bairro_selecionado:
                    modo = "BAIRRO"
                    obs_tecnica = "Bairro Definido pelo Usuário"
        else:
            # Sorteio inteligente de bairro
            candidatos_validos = []
            for b in self.data.bairros:
                z = b.get("zona_normalizada")
                clusters_zonas = {
                    "HIGH_END": ["residencial_fechado", "chacaras_fechado"],
                    "FAMILY": ["residencial_fechado", "residencial_aberto", "chacaras_fechado"],
                    "URBAN": ["residencial_aberto", "mista"],
                    "INVESTOR": ["industrial", "residencial_fechado", "mista", "residencial_aberto"],
                    "LOGISTICS": ["industrial"],
                    "CORPORATE": ["mista", "industrial", "residencial_aberto"]
                }
                # Se for portal, aceita zonas mais amplas (qualquer lugar que tenha gente)
                target_zones = clusters_zonas.get(cluster_ref, []) if not eh_portal else ["residencial_aberto", "residencial_fechado", "mista", "industrial", "chacaras_aberto"]
                
                if z in target_zones:
                    candidatos_validos.append(b)

            if candidatos_validos:
                if random.random() < 0.65:
                    ineditos = [b for b in candidatos_validos if not self.scanner.ja_publicado(b["nome"])]
                    if ineditos:
                        bairro_selecionado = random.choice(ineditos)
                        obs_tecnica = "Bairro Inédito Compatível (IA)"
                    else:
                        bairro_selecionado = random.choice(candidatos_validos)
                        obs_tecnica = "Bairro Compatível (IA - Já publicado)"
                    modo = "BAIRRO"
            
            if modo == "BAIRRO" and bairro_selecionado is None:
                modo = "CIDADE"
                obs_tecnica = "Fallback: Nenhum bairro compatível encontrado."

        # 4. Tópico
        if user_selection['topico'] != "ALEATÓRIO":
            topico_nome = user_selection['topico'] 
        else:
            keys = list(self.config.TOPICS_MAP.keys())
            pesos = [self.config.TOPICS_WEIGHTS[k] for k in keys]
            chave_sorteada = random.choices(keys, weights=pesos, k=1)[0]
            topico_nome = self.config.TOPICS_MAP[chave_sorteada]

        # 5. Ativo (Aqui a lógica muda se for Portal)
        if user_selection['ativo'] != "ALEATÓRIO":
            ativo_final = user_selection['ativo']
            obs_ref = "Definido pelo Usuário"
            # Só refina se for IMOBILIÁRIA. Se for PORTAL, aceita o tema direto.
            if not eh_portal and bairro_selecionado:
                 ativo_final, obs_ajuste = self.plano.refinar_ativo(cluster_ref, bairro_selecionado, [ativo_final])
                 obs_ref += f" | {obs_ajuste}"
        else:
            if eh_portal:
                # Sorteia um tema do Portal
                todos_portal = []
                for l in self.data.ativos_portal.values(): todos_portal.extend(l)
                ativo_final = random.choice(todos_portal)
                obs_ref = "Tema Portal Aleatório"
            else:
                ativo_base_list = self.data.ativos_por_cluster.get(cluster_ref, ["Imóvel Padrão"])
                if modo == "BAIRRO" and bairro_selecionado:
                    ativo_final, obs_ajuste = self.plano.refinar_ativo(cluster_ref, bairro_selecionado, ativo_base_list)
                    obs_ref = obs_ajuste
                else:
                    ativo_final = random.choice(ativo_base_list)
                    obs_ref = "Ativo Aleatório"
        
        obs_tecnica += f" | {obs_ref}"

        # 6. Formato e Gatilho
        formato = user_selection['formato'] if user_selection['formato'] != "ALEATÓRIO" else random.choice(self.config.CONTENT_FORMATS)
        gatilho = user_selection['gatilho'] if user_selection['gatilho'] != "ALEATÓRIO" else random.choice(self.config.EMOTIONAL_TRIGGERS)

        pacote = {
            "modo": modo,
            "bairro": bairro_selecionado,
            "cluster_tecnico": cluster_ref,
            "ativo_definido": ativo_final,
            "topico": topico_nome,
            "persona": persona_data,
            "formato": formato,
            "gatilho": gatilho,
            "obs_tecnica": obs_tecnica,
            "historico_titulos": historico_recente,
            "tipo_pauta": tipo_pauta_code # "PORTAL" ou "IMOBILIARIA"
        }

        data_pub = user_selection.get('data_pub_obj', datetime.date.today())
        self._salvar_log(pacote, data_pub)
        
        return pacote
