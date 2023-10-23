import streamlit as st
import src.generate_graphs as generate_graphs
import src.get_data as get_data

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

with tab_modelo:
    st.markdown("""
        Utilizando um modelo de árvores chamado `Random Forest`, que cria várias árvores de decisão, de maneira aleatória, gerando uma espécie de votação para realizar decisões sobre a classe a qual o dado pertence, 
        iremos observar a importância das features, utilizando o método de permutação.
        Tal método visa capturar a influência que cada variável tem nas predições do modelo, ao alterar aleatoriamente os valores de cada coluna, uma coluna por vez.
    """)
    st.plotly_chart(
        generate_graphs._plot_modelo_completo(get_data._get_importance_data_allfeatures()),
        use_container_width=True,
    )

    st.markdown("""
        Utilizando a função `seasonal_decompose` não foi identificado nenhum padrão sazonal.
        Foi utilizado o valor 5 no parâmetro _period_ por ser esse o ciclo de dias da bolsa
    """)
    st.plotly_chart(
        generate_graphs._plot_modelo_completo(get_data._get_importance_data_sintomas()),
        use_container_width=True,
    )