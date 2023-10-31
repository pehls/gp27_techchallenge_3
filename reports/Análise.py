import streamlit as st
import src.generate_graphs as generate_graphs
import src.get_data as get_data
from PIL import Image


st.write("""
    # Tech Challenge #03 - Grupo 27 
    ## Análise de dados da COVID - set/2020 a nov/2020
    by. Eduardo Gomes, Igor Brito e Gabriel Pehls
""")
         
st.info("""
    Nesse trabalho temos o objetivo de mostrar o processo de obtenção, ingestão e análise de dados do 
    [PNAD-COVID-19](https://www.ibge.gov.br/estatisticas/downloads-estatisticas.html?caminho=Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_PNAD_COVID19/Microdados/Dados) 
    do IBGE
""")


tab_dados, tab_tecnologia, tab_transformacao_e_ingestao = st.tabs(
    ['Dados utilizados', 'Tecnologia', 
     'Transformação e Ingestão']
    )

with tab_dados:
    st.markdown("""
Foram utilizados dados da PNAD entre setembro e novembro de 2020, devido á existência da resposta de ter covid ou não nesses meses.
Ainda, os dados foram limpos, para utilização do modelo estatístico para análise da importância das variáveis, excluindo linhas que contenham nulos, de modo a termos dados suficientes para a análise utilizando a biblioteca Pandas e Scikit-learn, em memória.
    """)

with tab_tecnologia:
    st.markdown("""
Para a manipulação dos dados, foi utilizado o PySpark, e algumas de suas transformações para manipular dados de forma paralela.
Como fonte dos dados, o BigQuery foi escolhido pela sua facilidade de utilização e manutenção.
    """)
    image = Image.open('reports/figures/tech-challenge-03-ingestao.png')
    st.image(image, caption='Ingestão de dados')
    
with tab_transformacao_e_ingestao:
    st.markdown("""
Capturando os dados da PNAD, ingerimos os mesmos em uma camada de dados crua (`raw_pnad`), que também recebeu os conteúdos das tabelas-dimensão, representando os Estados do Brasil (UF's), área de domicílio (Urbana/Rural), Sexo (Masculino/Feminino), Raça (Branca/Amarela/Parda/Indígena/Ignorado),
Escolaridade, Resposta de internação ou não, e a resposta positiva/negativa/não sabe, Faixa de Rendimento (familiar), Situação de Domicílio (próprio/aluguel/etc), e uma tabela com as questões escolhidas;
                
Foi elaborada uma segunda camada de dados (`refined_pnad`), contendo uma transformação da tabela principal (de dados da PNAD), normalizando dados das colunas com nomes mais "amigáveis", de acordo com o mapa de questões:
- "UF"-> "uf"
- "V1012"-> "semana_mes"
- "V1013"-> "mes"
- "V1022"-> "area_domicilio"
- "A002"-> "idade"
- "A003"-> "sexo"
- "A004"-> "cor_raca"
- "A005"-> "escolaridade"
- "B0011"-> "teve_febre"
- "B0014"-> "teve_dificuldade_respirar"
- "B0015"-> "teve_dor_cabeca"
- "B0019"-> "teve_fadiga"
- "B00111"-> "teve_perda_cheiro"
- "B002"-> "foi_posto_saude"
- "B0031"-> "ficou_em_casa"
- "B005"-> "ficou_internado"
- "B009B"-> "resultado_covid"
- "B007"-> "tem_plano_saude"
- "C007B"-> "assalariado"
- "C01011"-> "faixa_rendimento"
- "F001"-> "situacao_domicilio"

Nesta Camada, as tabelas dimensão seguem inalteradas, e deve ser utilizada como fonte caso seja necessário recuperar respostas numéricas, conforme o próprio questionário.
    """)
    
    image = Image.open('reports/figures/tech-challenge-03-model-db.png')
    st.image(image, caption='Modelagem banco - schema refined_pnad')

    st.markdown("""
Como último ponto, foi criada a camada de dados confiáveis (`trusted_pnad`), contendo o dado da camada refinada  com todas as transformações aplicadas, ou seja, o conteúdo de cada coluna é o conteúdo da tabela-dimensão, e existem apenas dados entre os meses de setembro e novembro de 2020, uma "regra de negócio" aplicada de acordo com o problema proposto, de utilizar apenas 3 meses de dados e no máximo 20 perguntas.
    """)

    image = Image.open('reports/figures/tech-challenge-03-bigquery.png')
    st.image(image, caption='BigQuery', width=500)
    