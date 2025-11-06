import pandas as pd
import numpy as np
import os
import time
import random
import re

from faker import Faker
from datetime import timedelta, date
from typing import Dict, List

# Configurações iniciais
start_time = time.time()
fake = Faker('pt_BR')
random.seed(42)
np.random.seed(42)
SEEDS_PATH = './seeds/'
os.makedirs(SEEDS_PATH, exist_ok=True)

def gerar_dados_maquinas(tamanho_lote: int) -> pd.DataFrame:
    """Gera dados fictícios de máquinas e retorna um DataFrame."""

    lista_maquinas = []
    maquinas_existentes = set()
    nomes_maquinas = [
        'Escavadeira Hidráulica', 'Caminhão Fora de Estrada', 'Trator de Esteiras', 'Pá Carregadeira', 
        'Motoniveladora', 'Perfuratriz Rotativa', 'Britador de Mandíbulas', 'Britador Cônico'
    ]
    nomes_fabricantes = [
        'Caterpillar', 'Komatsu', 'Liebherr', 'John Deere', 'Volvo'
    ]
    for i in range(0, tamanho_lote):
        while True:
            novos_codigos = f"MAQ-{random.randint(100, 999)}"
            if novos_codigos not in maquinas_existentes:
                maquinas_existentes.add(novos_codigos)
                break

        maquina = {
            "id": i,
            "codigo": novos_codigos,
            "nome": random.choice(nomes_maquinas),
            'fabricante': random.choice(nomes_fabricantes),
            'ano_fabricacao': fake.date_between(start_date='-8y', end_date='today'),
            'data_aquisicao': fake.date_between(start_date='-5y', end_date='today'),
            'valor_aquisicao': round(random.randint(50000, 500000), 2)
        }
        lista_maquinas.append(maquina)

    return pd.DataFrame(lista_maquinas)


def gerar_dados_operadores(tamanho_lote: int) -> pd.DataFrame:
    """Gera dados fictícios de operadores e retorna um DataFrame."""

    lista_operadores = []
    operadores_existentes = set()
    nome_setores = [
        'Extração', 'Transporte', 'Britagem', 'Beneficiamento', 'Carregamento', 'Perfuração'
    ]
    for i in range(0, tamanho_lote):
        while True:
            novos_codigos = f"OPR-{random.randint(100, 999)}"
            if novos_codigos not in operadores_existentes:
                operadores_existentes.add(novos_codigos)
                break

        operador = {
            'id': i,
            'matricula': novos_codigos,
            'nome': fake.name_male(),
            'setor': random.choice(nome_setores),
            'nivel_experiencia': random.choice(['Júnior', 'Pleno', 'Sênior'])
        }
        lista_operadores.append(operador)

    return pd.DataFrame(lista_operadores)


def gerar_dados_manutencoes(
        id_maquina: list, 
        tamanho_lote: int, 
        mapa_aquisicao: dict | None = None
    ) -> pd.DataFrame:
    """Gera dados de manutenções com os ID's de máquinas existentes e retorna um DataFrame."""

    manutencoes = []
    autoid = 1
    limite_min_global = date.today() - timedelta(days=8 * 365)

    for _ in range(tamanho_lote):
        inicio_minimo = mapa_aquisicao.get("codigo", limite_min_global) if mapa_aquisicao else limite_min_global
        if inicio_minimo > date.today():
            inicio_minimo = date.today()

        data_inicio = fake.date_between(start_date=inicio_minimo, end_date="today")
        data_fim = min(data_inicio + timedelta(days=random.randint(1, 60)), date.today())

        gravidade = random.choice(['Crítica', 'Alta', 'Média', 'Baixa'])
        if gravidade == 'Crítica':
            custo = round(random.randint(30000, 120000), 2)
        elif gravidade == 'Alta':
            custo = round(random.randint(15000, 50000), 2)
        elif gravidade == 'Média':
            custo = round(random.randint(3000, 30000), 2)
        else:
            custo = round(random.randint(5000, 5000), 2)

        manutencao = {
            "id": autoid,
            "cod_maquina": random.choice(id_maquina),
            "tipo": random.choice(["Corretiva", "Preventiva"]),
            "data_inicio": data_inicio,
            "data_fim": data_fim,
            "tempo_parada_horas": round(( (data_fim - data_inicio).days * 24), 2),
            "gravidade": gravidade,
            "custo": custo
        }
        manutencoes.append(manutencao)
        autoid += 1

    return pd.DataFrame(manutencoes)


def gerar_dados_inicentes(
        id_maquina: list, 
        id_operador: list, 
        tamanho_lote: int, 
        mapa_aquisicao: dict | None = None
    ) -> pd.DataFrame:
    """Gera dados de incidentes com id de máquina e operador existentes e retorna um DataFrame."""

    incidentes = []
    auto_id = 1
    limite_min_global = date.today() - timedelta(days=8 * 365)
    tipo_incidente = [
        "Falha Mecânica", "Falha Elétrica", "Falha Hidráulica", "Vazamento de Óleo", "Quebra de Correia", "Quebra de Mangueira",
        "Pneu Furado", "Falha na Transmissão", "Falha no Sensor", "Erro Operacional"
    ]

    for _ in range(tamanho_lote):
        inicio_minimo = mapa_aquisicao.get("codigo", limite_min_global) if mapa_aquisicao else limite_min_global
        if inicio_minimo > date.today():
            inicio_minimo = date.today()

        data_inicio = fake.date_between(start_date=inicio_minimo, end_date="today")

        gravidade = random.choice(['Crítica', 'Alta', 'Média', 'Baixa'])
        if gravidade == 'Crítica':
            custo = round(random.randint(30000, 120000), 2)
        elif gravidade == 'Alta':
            custo = round(random.randint(15000, 50000), 2)
        elif gravidade == 'Média':
            custo = round(random.randint(3000, 30000), 2)
        else:
            custo = round(random.randint(5000, 5000), 2)

        inicidente = {
            "id": auto_id,
            "cod_maquina": random.choice(id_maquina),
            "cod_operador": random.choice(id_operador),
            "data_ocorrencia": data_inicio,
            "tipo": random.choice(tipo_incidente),
            "gravidade": gravidade,
            "custo": custo
        }
        incidentes.append(inicidente)
        auto_id += 1

    return pd.DataFrame(incidentes)


def exportar_para_csv(
        tabelas: Dict[str, pd.DataFrame],
        pasta: str = './seeds/',
        prefixo: str = 'dados_',
        index: bool = False,
        sep: str = ',',
        encoding: str = 'utf-8'
    ) -> List[str]:
    """Salva os DataFrames em arquivos CSV."""

    caminhos = []
    for nome, df in tabelas.items():
        nome_ok = re.sub(r"[^A-Za-z0-9_.-]+", "", nome.strip()).strip("")
        base = f"{prefixo}{nome_ok}"

        caminho = os.path.join(pasta, f"{base}.csv")

        df.to_csv(caminho, index=index, sep=sep, encoding=encoding)
        caminhos.append(caminho)

    return caminhos


def main():
    """Roda a pipeline."""
    start = time.time()

    print("\nIniciando Geração de Arquivos...\n")

    df_maquinas = gerar_dados_maquinas(50)
    df_operadores = gerar_dados_operadores(30)

    lista_maquinas = df_maquinas['codigo'].to_list()
    lista_operadores = df_operadores['matricula'].to_list()
    mapa = dict(zip(df_maquinas['codigo'], df_maquinas['data_aquisicao']))

    df_manutencoes = gerar_dados_manutencoes(lista_maquinas, 150, mapa)
    df_incidentes = gerar_dados_inicentes(lista_maquinas, lista_operadores, 300, mapa)

    exportar_para_csv(
        {
            "maquinas": df_maquinas,
            "operadores": df_operadores,
            "manutencoes": df_manutencoes,
            "incidentes": df_incidentes
        },
        pasta=SEEDS_PATH,
        prefixo='dados_',
        index=False,
        sep=',',
        encoding='utf-8'
    )

    end = time.time()
    final = end - start

    print(f"\nArquivos Gerados!\nTempo de Execução: {round(final, 2)}s")
    

if __name__ == "__main__":
    main()