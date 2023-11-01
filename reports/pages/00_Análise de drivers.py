import streamlit as st
import src.generate_graphs as generate_graphs
import src.get_data as get_data

st.write("""
    # Análise de Drivers
""")

st.markdown("""
    Utilizando um modelo de árvores chamado `Random Forest`, que cria várias árvores de decisão, de maneira aleatória, gerando uma espécie de votação para realizar decisões sobre a classe a qual o dado pertence, 
    iremos observar a importância das features, utilizando o método de permutação.
""")

st.markdown("""
    Tal método visa capturar a influência que cada variável tem nas predições do modelo, ao alterar aleatoriamente os valores de cada coluna, uma coluna por vez.
""")

st.plotly_chart(
    generate_graphs._plot_modelo_completo(get_data._get_importance_data_allfeatures()),
    use_container_width=True,
)

st.markdown("""
    Notamos que a variável `uf` (Estado), `idade`, `escolaridade`, `cor_raca`, `tem_plano_saude`, `situacao_domicilio` e `sexo` despontam com uma importância relativa maior do que qualquer um dos sintomas;
""")
st.plotly_chart(
    generate_graphs._plot_modelo_completo(get_data._get_importance_data_sintomas()),
    use_container_width=True,
)

st.markdown("""
    Mesmo removendo algumas destas variáveis, vemos itens como `idade`, `tem_plano_saude` e `sexo` destoando como principais drivers!
""")
