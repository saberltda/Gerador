# src/engine.py
import random
import csv
import datetime
import os
from .config import GenesisConfig
from .logic import PlanoDiretor
from .scanner import BlogScanner

class GenesisEngine:
    """
    O 'Maestro'.
    Coordena subsistemas e gera LOGS de operação.
    """

    def __init__(self, data_instance):
        self.data = data_instance
        self.config = GenesisConfig()
        self.plano = PlanoDiretor()
        self.scanner = BlogScanner()
        # Define onde salvar o log
        self.log_file = "historico_geracao.csv"

    def _salvar_log(self, dados: dict):
        """Escreve uma linha no arquivo CSV para controle do usuário."""
        file_exists = os.path.isfile(self.log_file)
        
        # Prepara os dados para o CSV
        bairro_nome = dados['bairro']['nome'] if dados['bairro'] else "N/A (Cidade)"
        linha = [
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            dados['persona']['nome'],
            bairro_nome,
            dados['topico'],
            dados['ativo_definido'],
            dados['formato'],
            dados['gatilho']
        ]

        try:
            with open(self.log_file, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                # Se arquivo é novo, cria cabeçalho
                if not file_exists:
                    writer.writerow(["DATA", "PERSONA", "BAIRRO", "TOPICO", "ATIVO", "FORMATO", "GATILHO"])
                writer.writerow(linha)
        except Exception as e:
            print(f"Erro ao salvar log: {e}")

    def run(self, user_selection: dict):
        # 1. Atualiza o Scanner
        self.scanner.mapear()
        historico_recente = self.scanner.get_ultimos_titulos(20)

        # =====================================================
        # 1. DEFINIÇÃO DA PERSONA
        # =====================================================
        if user_selection['persona_key'] != "ALEATÓRIO":
            persona_key = user_selection['persona_key']
        else:
            persona_key = random.choice(list(self.config.PERSONAS.keys()))
            
        persona_data = self.config.PERSONAS[persona_key]
        cluster_ref = persona_data.get("cluster_ref", "FAMILY")

        # =====================================================
        # 2. DEFINIÇÃO DO BAIRRO (COM NULL SAFETY)
        # =====================================================
        bairro_selecionado = None
        modo = "CIDADE"
        obs_tecnica = "Foco Macro (Cidade)"

        if user_selection['bairro_nome'] != "ALEATÓRIO":
            for b in self.data.bairros:
                if b['nome'] == user_selection['bairro_nome']:
                    bairro_selecionado = b
                    break
            if bairro_selecionado:
                modo = "BAIRRO"
                obs_tecnica = "Bairro Definido pelo Usuário"
        else:
            candidatos_validos = []
            for b in self.data.bairros:
                z = b.get("zona_normalizada")
                match = False
                if cluster_ref == "HIGH_END" and z in ["residencial_fechado", "chacaras_fechado"]: match = True
                elif cluster_ref == "FAMILY" and z in ["residencial_fechado", "residencial_aberto", "chacaras_fechado"]: match = True
                elif cluster_ref == "URBAN" and z in ["residencial_aberto", "mista"]: match = True
                elif cluster_ref == "INVESTOR" and z in ["industrial", "residencial_fechado", "mista", "residencial_aberto"]: match = True
                elif cluster_ref == "LOGISTICS" and z in ["industrial"]: match = True
                elif cluster_ref == "CORPORATE" and z in ["mista", "industrial", "residencial_aberto"]: match = True
                if match:
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
            
            # --- CORREÇÃO DE SEGURANÇA (NULL SAFETY) ---
            # Se a IA tentou escolher mas falhou, garante que volta para modo CIDADE
            if modo == "BAIRRO" and bairro_selecionado is None:
                modo = "CIDADE"
                obs_tecnica = "Fallback: Nenhum bairro compatível encontrado."

        # =====================================================
        # 3. TÓPICO, ATIVO E REFINAMENTO
        # =====================================================
        if user_selection['topico'] != "ALEATÓRIO":
            topico_nome = user_selection['topico'] 
        else:
            keys = list(self.config.TOPICS_MAP.keys())
            pesos = [self.config.TOPICS_WEIGHTS[k] for k in keys]
            chave_sorteada = random.choices(keys, weights=pesos, k=1)[0]
            topico_nome = self.config.TOPICS_MAP[chave_sorteada]

        if user_selection['ativo'] != "ALEATÓRIO":
            ativo_final = user_selection['ativo']
            obs_ref = "Ativo Definido pelo Usuário"
            if bairro_selecionado:
                 ativo_final, obs_ajuste = self.plano.refinar_ativo(cluster_ref, bairro_selecionado, [ativo_final])
                 obs_ref += f" | {obs_ajuste}"
        else:
            ativo_base_list = self.data.ativos_por_cluster.get(cluster_ref, ["Imóvel Padrão"])
            if modo == "BAIRRO" and bairro_selecionado:
                ativo_final, obs_ajuste = self.plano.refinar_ativo(cluster_ref, bairro_selecionado, ativo_base_list)
                obs_ref = obs_ajuste
            else:
                ativo_final = random.choice(ativo_base_list)
                obs_ref = "Ativo Aleatório"

        obs_tecnica += f" | {obs_ref}"

        if user_selection['formato'] != "ALEATÓRIO":
            formato = user_selection['formato']
        else:
            formato = random.choice(self.config.CONTENT_FORMATS)

        if user_selection['gatilho'] != "ALEATÓRIO":
            gatilho = user_selection['gatilho']
        else:
            gatilho = random.choice(self.config.EMOTIONAL_TRIGGERS)

        # Monta o pacote final
        pacote_final = {
            "modo": modo,
            "bairro": bairro_selecionado,
            "cluster_tecnico": cluster_ref,
            "ativo_definido": ativo_final,
            "topico": topico_nome,
            "persona": persona_data,
            "formato": formato,
            "gatilho": gatilho,
            "obs_tecnica": obs_tecnica,
            "historico_titulos": historico_recente
        }

        # --- GERA O LOG AUTOMÁTICO ---
        self._salvar_log(pacote_final)

        return pacote_final
