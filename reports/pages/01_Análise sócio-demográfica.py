import streamlit as st
import src.generate_graphs as generate_graphs
import src.get_data as get_data

st.title('Análise sócio-demográfica')

tab_analise_inicial, tab_positivos = st.tabs(['Definição dos Meses',"Localização dos Positivos"])

with tab_analise_inicial:
    st.markdown("""
                ##### Para definirmos os meses a serem estudados, primeiro buscamos entender como os dados estão distribuídos por mês durante o ano de 2020 e quantos casos positivos tivemos em cada um deles
                

""")
    st.plotly_chart(
        generate_graphs._plot_inicial(
            get_data._get_initial_data()
        )
    )
    st.markdown("""
- Com base nos dados acima, é possível identificar que os 3 meses com uma quantidade de registros ccom o valor resultado_covid diferente de NA tem uma amostra mais relevante nos últimos 3 meses da comparação. Nesse caso, optamos por utilizar os meses de novembro(11), outubro(10) e setembro(9).
- Abaixo vemos como os dados estão segmentados por "categoria" dentro do resultado_covid durante os meses citados
""")
    st.plotly_chart(
        generate_graphs._plot_inicial_porcentagens(
            get_data._get_initial_data_percentage(
                get_data._get_initial_data()
            )
        )
    )

with tab_positivos:
    st.markdown("""
    """)
    st.write(get_data._get_localizacao())

    st.plotly_chart(
        generate_graphs._map_plot(
            get_data._get_localizacao()
        )
    )