# src/database.py
import json
import os
from .utils import slugify  # Importando a função do nosso utilitário

class GenesisData:
    def __init__(self, bairros_path: str = "assets/bairros.json"):
        """
        Carrega a lista de bairros e define os ativos imobiliários disponíveis.
        """
        self.bairros = self._carregar_bairros(bairros_path)

        # Definição dos tipos de imóveis por perfil (Hardcoded)
        self.ativos_por_cluster = {
            "HIGH_END": ["Casa em Condomínio de Luxo", "Sobrado Alto Padrão", "Mansão em Condomínio"],
            "FAMILY": ["Casa de Rua (Bairro Aberto)", "Casa em Condomínio Club", "Sobrado Residencial"],
            "URBAN": ["Apartamento Moderno", "Studio/Loft", "Cobertura Duplex"],
            "INVESTOR": ["Terreno em Condomínio", "Lote para Construção", "Imóvel para Reforma (Flip)"],
            "CORPORATE": ["Sala Comercial", "Laje Corporativa", "Prédio Monousuário"],
            "LOGISTICS": ["Galpão Logístico", "Terreno Industrial", "Condomínio Logístico"],
        }
        
        # Gera uma lista única de todos os ativos para o SelectBox da interface
        self.todos_ativos = []
        for lista in self.ativos_por_cluster.values():
            self.todos_ativos.extend(lista)
        self.todos_ativos = list(set(self.todos_ativos)) # Remove duplicatas
        self.todos_ativos.sort()

    def _carregar_bairros(self, path: str):
        # Verifica se o arquivo existe
        if not os.path.exists(path):
            # Tenta um fallback para o diretório atual caso rode fora da raiz
            if os.path.exists(f"../{path}"):
                path = f"../{path}"
            else:
                raise RuntimeError(
                    f"ERRO CRÍTICO: Arquivo '{path}' não encontrado. "
                    "Verifique se a pasta 'assets' está na raiz do projeto."
                )

        try:
            with open(path, "r", encoding="utf-8") as f:
                raw = json.load(f)
        except Exception as e:
            raise RuntimeError(f"Erro ao ler JSON de bairros: {e}")

        # Processa e enriquece os dados dos bairros
        bairros_enriquecidos = []
        
        # Função auxiliar interna para mapear zonas
        def _map_zona(zona_texto: str):
            z = zona_texto.lower()
            if "industrial" in z or "empresarial" in z: return "industrial"
            if "condomínio" in z and "fechado" in z: return "residencial_fechado"
            if "chácara" in z: return "chacaras_aberto" if "aberto" in z else "chacaras_fechado"
            if "mista" in z: return "mista"
            return "residencial_aberto"

        for b in raw:
            # Cria uma cópia para não alterar o original
            b2 = dict(b)
            # Cria o slug (ex: "Jardim Pau Preto" -> "jardim_pau_preto")
            b2["slug"] = slugify(b["nome"])
            # Normaliza a zona para a lógica do sistema
            b2["zona_normalizada"] = _map_zona(b.get("zona", ""))
            bairros_enriquecidos.append(b2)

        return bairros_enriquecidos


class GenesisRules:
    def __init__(self, path: str = "assets/REGRAS.txt"):
        """
        Carrega as regras imutáveis de compliance e formatação.
        """
        if not os.path.exists(path):
             # Fallback
            if os.path.exists(f"../{path}"):
                path = f"../{path}"
            else:
                raise RuntimeError(f"ERRO: Arquivo '{path}' de regras não encontrado.")
            
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.raw_text = f.read()
        except Exception as e:
            raise RuntimeError(f"Erro ao ler REGRAS.txt: {e}")

    def get_for_prompt(self, contexto_local: str) -> str:
        """
        Injeta o contexto local (Nome do Bairro) dentro do texto das regras
        onde houver o placeholder {b['nome']}.
        """
        txt = self.raw_text
        # Substituição simples de string
        txt = txt.replace("{b['nome']}", contexto_local)
        return txt