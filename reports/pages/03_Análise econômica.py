import streamlit as st
import src.generate_graphs as generate_graphs
import src.get_data as get_data

st.title('Análise Econômica')

tab_cor_raca, tab_escolaridade, tab_rendimento, tab_plano_saude, tab_situacao_domiciliar, tab_idade = st.tabs(
    [
       'Cor/Raça','Escolaridade', "Faixa de Rendimento", "Tem Plano de Saúde?", "Situação Domiciliar", "Idade"
    ]
)

with tab_cor_raca:
    st.markdown("""
    - Notamos uma menor presença de respostas positivas em categorias mais carentes de cores/raças, como Pretos/Pardos/Indígenas;
    - Isto poderia ser um reflexo da falta de acesso a itens como saúde de qualidade e informação?
    """)

    df = get_data._get_cor_raca()

    st.plotly_chart(
        generate_graphs._plot_analise_economica(
            df, order={
                'Resposta Pergunta':[
                    'Indígena','Parda','Preta', 'Branca', 'Amarela', 'Ignorado'
                ],
                'Resposta Covid':[
                    'Sim', 'Não', 'Não sabe', 'Ignorado'
                ]
            }
        )
    )

with tab_escolaridade:
    st.markdown("""
    - Novamente, em categorias mais "elevadas", como Superior Completo, incompleto, pós-graduação/mestrado/doutorado, a porcentagem de positivados é superior a outras categorias;
    - Novamente, um reflexo da falta de acesso a informação e saúde de qualidade?
    """)

    df = get_data._get_escolaridade()

    st.plotly_chart(
        generate_graphs._plot_analise_economica(
            df, order={
                'Resposta Pergunta':[
                    'Sem instrução',
                    'Fundamental incompleto', 'Fundamental completa', 
                    'Médio incompleto', 'Médio completo', 
                    'Superior incompleto', 'Superior completo',
                    'Pós-graduação, mestrado ou doutorado'
                ],
                'Resposta Covid':[
                    'Sim', 'Não', 'Não sabe', 'Ignorado'
                ]
            }
        )
    )

with tab_rendimento:
    st.markdown("""
    - Reafirmando o ponto levantado no primeiro item, quão maior a faixa de Rendimento familiar, maiores são as porcentagens de positivados
    """)

    df = get_data._get_faixa_rendimento()
    st.plotly_chart(
        generate_graphs._plot_analise_economica(
            df.loc[df['Resposta Pergunta']!='NA'], 
            order={
                'Resposta Pergunta':[
                    '0 - 100', '101 - 300', '301 - 600',
                    '601 - 800', '801 - 1.600', '1.601 - 3.000',
                    '3.001 - 10.000', '10.001 - 50.000', '50.001 - 100.000'
                ],
                'Resposta Covid':[
                    'Sim', 'Não', 'Não sabe', 'Ignorado'
                ]
            }
        )
    )

with tab_plano_saude:
    st.markdown("""
    """)

    df = get_data._get_tem_plano_saude()
    st.plotly_chart(
        generate_graphs._plot_analise_economica(
            df.loc[df['Resposta Pergunta']!='NA'], 
            order={
                'Resposta Pergunta':[
                    '0 - 100', '101 - 300', '301 - 600',
                    '601 - 800', '801 - 1.600', '1.601 - 3.000',
                    '3.001 - 10.000', '10.001 - 50.000', '50.001 - 100.000'
                ],
                'Resposta Covid':[
                    'Sim', 'Não', 'Não sabe', 'Ignorado'
                ]
            }
        )
    )
    
with tab_situacao_domiciliar:
    st.markdown("""
    """)

    df = get_data._get_situacao_domicilio()
    st.plotly_chart(
        generate_graphs._plot_analise_economica(
            df.loc[df['Resposta Pergunta']!='NA'], 
            order={
                'Resposta Pergunta':[
                    'Outra condição',
                    'Cedido por empregador', 'Cedido por familiar ',
                    'Cedido de outra forma ','Alugado',
                    'Próprio - ainda pagando', 'Próprio - já pago '

                ],
                'Resposta Covid':[
                    'Sim', 'Não', 'Não sabe', 'Ignorado'
                ]
            }
        )
    )

with tab_idade:
    st.markdown("""
    """)

    df = get_data._get_idade()

    st.plotly_chart(
        generate_graphs._plot_analise_economica(
            df.loc[df['Resposta Pergunta']!='NA'], 
            order={
                'Resposta Pergunta':[
                    '0-9 anos','10-19 anos', '20-29 anos',
                    '30-39 anos', '40-49 anos', '50-59 anos',
                    '60-69 anos', '+70'
                ],
                'Resposta Covid':[
                    'Sim', 'Não', 'Não sabe', 'Ignorado'
                ]
            }
        )
    )