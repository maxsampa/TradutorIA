
# 2024.10.29
# Aluno: Fábio Ribeiro
# Professor: Marco Revoredo
# ATENÇÃO: executar com o código: streamlit run TradutorIA.py

#!pip install transformers
#!pip install streamlit
#!pip install torch
#!pip install googletrans

# Lendo a biblioteca do Transformers, Streamlit e Google Translator
from transformers import AutoTokenizer, AutoModelForCausalLM    # Biblioteca para trabalhar com modelos de IA
import streamlit as st                                          # Cria a interface web
from googletrans import Translator                              # API do Google para traduções
import torch                                                    # biblioteca para machine learning

# Função para importar o modelo Bloom 560M multi-idiomas
@st.cache_resource # recurso para não recarregar o modelo a toda consulta
def carregar_modelo():                                          #
  try:
    tokenizer = AutoTokenizer.from_pretrained("bigscience/bloom-560m") # Carregando o tokenizador (qeu converte textos em números que o modelo entende)
    modelo = AutoModelForCausalLM.from_pretrained("bigscience/bloom-560m") # Carregando o modelo Bloom 560 milhões de parâmetros
    return tokenizer, modelo
  except Exception as e:
    st.error(f'Erro ao carregar o modelo: {str(e)}') # Mensagem se houver erro ao carregar o modelo
    return None,None
  

# Função para gerar o texto com o modelo Bloom
def gerar_texto_bloom(texto, tokenizer, modelo):
  try:  # Converte o texto em tokens
    entradas = tokenizer(texto, return_tensors='pt', padding=True, truncation=True) #Tokenizar o texto

    # Gerar novo texto usando o modelo
    with torch.no_grad():           # Desativa cálculso de gradiente para economia de memória
      saidas = modelo.generate(
        entradas.input_ids,
        max_length = 50,            # Tamanho máximo do texto gerado
        temperature = 0.9,          # Contra criatividade: quanto maior, mais criativo (aleatório)
        num_return_sequences = 1,   # Versões diferentes para gerar
        repetition_penalty=1.2,           # Evita repetições
        no_repeat_ngram_size=3,          # Evitar repetir sequências de 3 palavras
        do_sample=True,                   # Usar amostragem probabilística
        top_k=50,                        # Considera as 50 palavras mais prováveis
        top_p=0.95,                      # Controle adicional de probabilidade
        pad_token_id = tokenizer.pad_token_id
      )

# Decodificar o resultado (converte os números do token para texto)
    texto_gerado = tokenizer.decode(saidas[0], skip_special_tokens=True)
    return texto_gerado
  except Exception as e:
    raise Exception (f'Erro na geração de texto: {str(e)}')

# Função para traduzir o texto em português carregando no modelo
def traduzindo(texto):
  try:
    texto_traduzido = Translator()
    # Traduz o texto do português para o idioma selecionado
    traducao = texto_traduzido.translate(texto, src='pt', dest=idiomas[selecao])
    return traducao.text # Retorna só o texto traduzido
  except Exception as e:
    raise Exception (f'Erro na tradução: {str(e)}')
  

# Dicionário Python contendo 3 principais idiomas e o seu código correspondente para a seleção
idiomas = {
    'Inglês': 'en',
    'Espanhol': 'es',
    'Francês': 'fr'
}

# Interface do Streamlit - Título cabeçalho web
st.title('Super Tradutor')
st.header('Powered by Google Translator & Bloom')


# Carregar Modelo e tokenizer
tokenizer, modelo = carregar_modelo()

# Caixa de seleção no Streamlit do idioma desejado
selecao = st.selectbox('Selecione o idioma', list(idiomas.keys()))

# Caixa para registro do texto pelo usuário
texto_original = st.text_area ('Digite o texto a ser traduzido em português: (Confirme com CTRL+Enter)')

# Processamento da tradução e geração de texto
if texto_original.strip():  # Só processa se houver texto. A função .strip() remove os espaços em branco
    coluna1, coluna2 = st.columns(2)    # Divide a tela em 2 colunas
    
    with coluna1:
        if st.button('Traduzir com IA'):    # Botão para tradução com IA
            try:
                # Primeiro usa o Bloom para processar o texto
                texto_processado = gerar_texto_bloom(texto_original, tokenizer, modelo)
                st.info("Texto processado pela IA:")
                st.write(texto_processado)
                
                # Depois traduz o resultado
                texto_traduzido = traduzindo(texto_processado)
                st.success("Tradução:")
                st.write(texto_traduzido)
            except Exception as e:
                st.error(f'Erro no processamento: {str(e)}')
    
    with coluna2:
        if st.button('Apenas Tradução (sem IA)'):   # Botão para tradução sem IA
            try:
                texto_traduzido = traduzindo(texto_original)
                st.success("Tradução direta:")
                st.write(texto_traduzido)
            except Exception as e:
                st.error(f'Erro na tradução: {str(e)}')

elif texto_original:  # Se o usuário começou a digitar mas só tem espaços
    st.error('Digite o texto')