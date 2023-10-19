import streamlit as st
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import src.generate_graphs as generate_graphs
import src.get_data as get_data

st.write("""
    # Tech Challenge #03 - Grupo 27 
    ## Análise de dados da COVID - set/2020 a nov/2020
    by. Eduardo Gomes, Igor Brito e Gabriel Pehls
""")
         
st.info("""
    
""")
        

tab_grafico_historico, tab_seasonal, tab_adf, tab_acf, tab_models = st.tabs(['Gráfico Histórico', 'Decompondo sazonalidade', 'Teste ADFuller', 'Autocorrelação - ACF/PACF', 'Modelos - Teste'])

with tab_grafico_historico:
    df = get_data._get_all_indicators_data()
    st.plotly_chart(
        generate_graphs._grafico_historico(df),
        use_container_width=True,
    )

    st.markdown(f"""
        
    """)
