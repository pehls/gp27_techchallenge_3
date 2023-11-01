import streamlit as st

st.title('Conclusão')

st.markdown("""
    Apesar da seleção do curto período de três meses e de poucas variáveis, nesse trabalho conseguimos abordar desde a coleta até a análise dos dados.

    Passamos pelo download e extração dos arquivos PNAD com `Python`, processamento desses dados através do `Apache Spark` selecionando algumas questões para criação de um banco no `BigQuery` para análise. Pensando no uso de dados numéricos para trabalhar com alguns modelos e para melhor organização, foram criados alguns _schemas_ no banco, estruturando os dados em tabelas _fato_ e _dimensão_. 
    
    Para análise e consulta, usamos a tabela em **trusted** que já conta com os dados transformados.
""")