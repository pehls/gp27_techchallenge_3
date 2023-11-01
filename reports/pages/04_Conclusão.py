import streamlit as st

st.title('Conclusão')

st.markdown("""
    Apesar da seleção do curto período de três meses e de poucas variáveis, nesse trabalho conseguimos abordar desde a coleta até a análise dos dados.

    Passamos pelo download e extração dos arquivos PNAD com `Python`, processamento desses dados através do `Apache Spark` selecionando algumas questões para criação de um banco no `BigQuery` para análise. Pensando no uso de dados numéricos para trabalhar com alguns modelos e para melhor organização, foram criados alguns _schemas_ no banco, estruturando os dados em tabelas _fato_ e _dimensão_. 
    
    Para análise e consulta, usamos a tabela em **trusted** que já conta com os dados transformados.
            
    Consultando os dados, apenas o mês de Novembro/2020 tem quantidade relevante de respostas para a pergunta sobre Covid _"Qual o resultado? (B009B)"_, e que ~23% responderam 'Sim'. 
            
    Para os que afirmaram ter tido Covid, a maioria (>90%) disse 'Não' ter apresentado sintomas como febre, dor de cabeça, fadiga, perda de cheiro e dificuldade para respirar.
            
    Olhando apenas números absolutos, observamos que a região Norte tem predominância nos casos positivos, e que os estados do Acre, Pará e Amazonas se destacam.
            
    Por fim, com um olhar pelo aspecto econômico observamos que quanto maior o nível de instrução maior o número de positivos, e com isso fica a dúvida se é devido a qualidade de informação recebida.
""")