from pyspark.sql.functions import udf
from pyspark.sql.types import IntegerType, StringType

def _get_uf(codigo):
    uf = {
        "11": "Rondônia",
        "12": "Acre",
        "13": "Amazonas",
        "14": "Roraima",
        "15": "Pará",
        "16": "Amapá",
        "17": "Tocantins",
        "21": "Maranhão",
        "22": "Piauí",
        "23": "Ceará",
        "24": "Rio Grande do Norte",
        "25": "Paraíba",
        "26": "Pernambuco",
        "27": "Alagoas",
        "28": "Sergipe",
        "29": "Bahia",
        "31": "Minas Gerais",
        "32": "Espírito Santo",
        "33": "Rio de Janeiro",
        "35": "São Paulo",
        "41": "Paraná",
        "42": "Santa Catarina",
        "43": "Rio Grande do Sul",
        "50": "Mato Grosso do Sul",
        "51": "Mato Grosso",
        "52": "Goiás",
        "53": "Distrito Federal",
    }

    if codigo in uf:
        return uf[codigo]
    
    return 'NA'

def _get_area_domicilio(codigo):
    area = {
        '1': 'Urbana',
        '2': 'Rural',
    }

    if codigo in area:
        return area[codigo]
    
    return 'NA'

def _get_sexo(codigo):
    sexo = {
        '1': 'masculino',
        '2': 'feminino',
    }

    if codigo in sexo:
        return sexo[codigo]
    
    return 'NA'

def _get_cor_raca(codigo):
    cor_raca = {
        '1': 'Branca',
        '2': 'Preta',
        '3': 'Amarela',
        '4': 'Parda',
        '5': 'Indígena',
        '9': 'Ignorado',
    }
    if codigo in cor_raca:
        return cor_raca[codigo]
    return 'NA'

def _get_escolaridade(codigo):
    escolaridade = {
        '1': 'Sem instrução',
        '2': 'Fundamental incompleto',
        '3': 'Fundamental completa',
        '4': 'Médio incompleto',
        '5': 'Médio completo',
        '6': 'Superior incompleto',
        '7': 'Superior completo',
        '8': 'Pós-graduação, mestrado ou doutorado',
    }
    if codigo in escolaridade:
        return escolaridade[codigo]
    return 'NA'

def _get_resposta_covid(codigo):
    resposta = {
        '1': 'Sim',
        '2': 'Não ',
        '3': 'Não sabe',
        '9': 'Ignorado',
    }
    if codigo in resposta:
        return resposta[codigo]
    return 'NA'

def _get_internado(codigo):
    resposta = {
        '1': 'Sim',
        '2': 'Não ',
        '3': 'Não foi atendido',
        '9': 'Ignorado',
    }
    if codigo in resposta:
        return resposta[codigo]
    return 'NA'

def _get_assalariado(codigo):
    assalariado = {
        '1': 'Sim, tem carteira de trabalho assinada',
        '2': 'Sim, é servidor público estatutário',
        '3': 'Não',
    }
    if codigo in assalariado:
        return assalariado[codigo]
    return 'NA'

def _get_faixa_rendimento(codigo):
    faixa = {
        '00': '0 - 100',
        '01':	'101 - 300',
        '02':	'301 - 600',
        '03':	'601 - 800',
        '04':	'801 - 1.600',
        '05':	'1.601 - 3.000',
        '06':	'3.001 - 10.000',
        '07':	'10.001 - 50.000',
        '08':	'50.001 - 100.000',
        '09':	'Mais de 100.000',
    }
    if codigo in faixa:
        return faixa[codigo]
    return 'NA'

def _get_situacao_domicilio(codigo):
    situacao = {
        '1': 'Próprio - já pago ',
        '2': 'Próprio - ainda pagando',
        '3': 'Alugado',
        '4': 'Cedido por empregador',
        '5': 'Cedido por familiar ',
        '6': 'Cedido de outra forma ',
        '7': 'Outra condição',
    }
    if codigo in situacao:
        return situacao[codigo]
    return 'NA'

_transform_uf = udf(_get_uf, StringType())
_transform_int = udf(int, IntegerType())
_transform_area_domicilio = udf(_get_area_domicilio, StringType())
_transform_sexo = udf(_get_sexo, StringType())
_transform_cor_raca = udf(_get_cor_raca, StringType())
_transform_escolaridade = udf(_get_escolaridade, StringType())
_transform_resposta_covid = udf(_get_resposta_covid, StringType())
_transform_internado = udf(_get_internado, StringType())
_transform_assalariado = udf(_get_assalariado, StringType())
_transform_faixa_rendimento = udf(_get_faixa_rendimento, StringType())
_transform_situacao_domicilio = udf(_get_situacao_domicilio, StringType())

def transform(df):
    """
    Seleciona somente as colunas previamente escolhidas para análise
    Renomeia colunas
    Realiza 'de/para' de valores
    """

    columns = [
        "UF",
        "V1012",
        "V1013",
        "V1022",
        "A002",
        "A003",
        "A004",
        "A005",
        "B0011",
        "B0014",
        "B0015",
        "B0019",
        "B00111",
        "B002",
        "B0031",
        "B005",
        "B007",
        "C007B",
        "C01011",
        "F001",
    ]

    df = df.select(columns)

    df = (
        df.withColumnRenamed("UF", "uf")
        .withColumnRenamed("V1012", "semana_mes")
        .withColumnRenamed("V1013", "mes")
        .withColumnRenamed("V1022", "area_domicilio")
        .withColumnRenamed("A002", "idade")
        .withColumnRenamed("A003", "sexo")
        .withColumnRenamed("A004", "cor_raca")
        .withColumnRenamed("A005", "escolaridade")
        .withColumnRenamed("B0011", "teve_febre")
        .withColumnRenamed("B0014", "teve_dificuldade_respirar")
        .withColumnRenamed("B0015", "teve_dor_cabeca")
        .withColumnRenamed("B0019", "teve_fadiga")
        .withColumnRenamed("B00111", "teve_perda_cheiro")
        .withColumnRenamed("B002", "foi_posto_saude")
        .withColumnRenamed("B0031", "ficou_em_casa")
        .withColumnRenamed("B005", "ficou_internado")
        .withColumnRenamed("B007", "tem_plano_saude")
        .withColumnRenamed("C007B", "assalariado")
        .withColumnRenamed("C01011", "faixa_rendimento")
        .withColumnRenamed("F001", "situacao_domicilio")
    )

    df = df.withColumn('uf', _transform_uf(df.uf))
    df = df.withColumn('semana_mes', _transform_int(df.semana_mes))
    df = df.withColumn('mes', _transform_int(df.mes))
    df = df.withColumn('area_domicilio', _transform_area_domicilio(df.area_domicilio))
    df = df.withColumn('idade', _transform_int(df.idade))
    df = df.withColumn('sexo', _transform_sexo(df.sexo))
    df = df.withColumn('cor_raca', _transform_cor_raca(df.cor_raca))
    df = df.withColumn('escolaridade', _transform_escolaridade(df.escolaridade))
    df = df.withColumn('teve_febre', _transform_resposta_covid(df.teve_febre))
    df = df.withColumn('teve_dificuldade_respirar', _transform_resposta_covid(df.teve_dificuldade_respirar))
    df = df.withColumn('teve_dor_cabeca', _transform_resposta_covid(df.teve_dor_cabeca))
    df = df.withColumn('teve_fadiga', _transform_resposta_covid(df.teve_fadiga))
    df = df.withColumn('teve_perda_cheiro', _transform_resposta_covid(df.teve_perda_cheiro))
    df = df.withColumn('foi_posto_saude', _transform_resposta_covid(df.foi_posto_saude))
    df = df.withColumn('ficou_em_casa', _transform_resposta_covid(df.ficou_em_casa))
    df = df.withColumn('ficou_internado', _transform_internado(df.ficou_internado))
    df = df.withColumn('tem_plano_saude', _transform_resposta_covid(df.tem_plano_saude))
    df = df.withColumn('assalariado', _transform_assalariado(df.assalariado))
    df = df.withColumn('faixa_rendimento', _transform_faixa_rendimento(df.faixa_rendimento))
    df = df.withColumn('situacao_domicilio', _transform_situacao_domicilio(df.situacao_domicilio))

    return df
