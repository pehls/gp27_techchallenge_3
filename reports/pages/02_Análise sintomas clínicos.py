import streamlit as st
import src.generate_graphs as generate_graphs
import src.get_data as get_data

st.title('Análise sintomas clínicos')

tab_sintomas_geral, tab_sintomas_positivos, tab_sintomas_negativos = st.tabs(
    [
       "Sintomas - Geral", "Sintomas - Positivos", "Sintomas - Negativos"
    ]
)
df_base = get_data._get_sintomas_clinicos_all()

with tab_sintomas_geral:
    st.markdown("""
    - Ao analisar os sintomas, notamos que a grande maioria deles tem resposta positiva superior em casos que não tiveram covid, comparado a aqueles que positivaram;
    - Os dois sintomas de maior presença são a Fadiga (aparece em 856 casos positivos de covid) e Febre (aparece em 592 casos), com respectivamente 41,57% e  44,54% dis respondentes que tiveram tais sintomas com covid-positivo;       
    """)

    df = get_data._get_calculated_sintomas(
        df_base
        )
    questao_selecionada = st.radio('Questões', 
                                   [x.replace('teve_','').replace('_',' ').capitalize()+'?' for x in df.questao.unique()], 
                                   horizontal=True, key='geral')

    st.plotly_chart(
        generate_graphs._plot_sintomas(
            questao_selecionada, df
            )
    )
    
with tab_sintomas_positivos:
    st.markdown("""
    - Ao isolar os casos positivos, porém, notamos que em todas as perguntas, acima de 90% dos respondentes declaram não ter tido nenhum dos sintomas!
    """)

    df_positivos = get_data._get_calculated_sintomas(
        df_base.loc[df_base['resultado_covid']=="Sim"],
        groupby=['questao']
    )

    questao_selecionada_positivos = st.radio('Questões', 
                                   [x.replace('teve_','').replace('_',' ').capitalize()+'?' for x in df.questao.unique()], 
                                   horizontal=True, key='positivos')
    st.plotly_chart(
        generate_graphs._plot_sintomas(
            questao_selecionada_positivos, df_positivos
            )
    )

with tab_sintomas_negativos:
    st.markdown("""
    - Observando os negativos de forma isolada, notamos que a porcentagem de respostas negativas para cada pergunta se mantém acima de 96%.
    """)

    df_negativos = get_data._get_calculated_sintomas(
        df_base.loc[df_base['resultado_covid']=="Não"],
        groupby=['questao']
    )
    questao_selecionada_negativos = st.radio('Questões', 
                                   [x.replace('teve_','').replace('_',' ').capitalize()+'?' for x in df.questao.unique()], 
                                   horizontal=True, key='negativos')
    st.plotly_chart(
        generate_graphs._plot_sintomas(
            questao_selecionada_negativos, df_negativos
            )
    )