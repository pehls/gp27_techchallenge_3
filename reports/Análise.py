import streamlit as st

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


tab_dados, tab_tecnologia, tab_transformacao, tab_ingestao, tab_modelo = st.tabs(['Dados utilizados', 'Tecnologia', 'Transformação', 'Ingestão', 'Modelo'])

