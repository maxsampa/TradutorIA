import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
from googletrans import Translator
import torch
import logging

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Configuração da página
st.set_page_config(
    page_title="TradutorIA",
    layout="centered"
)

# Cache do modelo para economia de memória
@st.cache_resource(show_spinner=False)
def carregar_modelo():
    try:
        tokenizer = AutoTokenizer.from_pretrained(
            "bigscience/bloom-560m",
            low_cpu_mem_usage=True
        )
        modelo = AutoModelForCausalLM.from_pretrained(
            "bigscience/bloom-560m",
            low_cpu_mem_usage=True
        )
        return tokenizer, modelo
    except Exception as e:
        logging.exception("Erro ao carregar o modelo de IA.")
        st.error(f'Erro ao carregar o modelo: {str(e)}')
        return None, None

# Função otimizada para gerar texto
def gerar_texto_bloom(texto, tokenizer, modelo, max_length=512):
    try:
        with torch.inference_mode():
            prompt = f"Refine e reescreva o seguinte texto em português, mantendo o significado original e tornando-o mais claro e polido: {texto}"

            entradas = tokenizer(
                prompt,
                return_tensors='pt',
                padding=True,
                truncation=True,
                max_length=max_length
            )

            saidas = modelo.generate(
                entradas.input_ids,
                max_length=max_length,
                temperature=0.3,
                num_return_sequences=1,
                repetition_penalty=1.5,
                no_repeat_ngram_size=3,
                do_sample=True,
                top_k=20,
                top_p=0.7,
                pad_token_id=tokenizer.pad_token_id
            )

            texto_gerado = tokenizer.decode(saidas[0], skip_special_tokens=True)

            # Remove o prompt da saída se presente
            prompt_prefix = "Refine e reescreva o seguinte texto em português, mantendo o significado original e tornando-o mais claro e polido: "
            if texto_gerado.startswith(prompt_prefix):
                texto_gerado = texto_gerado[len(prompt_prefix):].strip()
            elif ": " in texto_gerado:
                partes = texto_gerado.split(": ", 1)
                if len(partes) > 1:
                    texto_gerado = partes[1].strip()

            return texto_gerado
    except Exception as e:
        logging.exception(f"Erro na geração de texto para entrada: '{texto[:50]}...'")
        raise Exception(f'Erro na geração de texto: {str(e)}') from e

# Função de tradução otimizada
@st.cache_data(show_spinner=False)
def traduzir(texto, idioma_destino):
    try:
        tradutor = Translator()
        traducao = tradutor.translate(texto, src='pt', dest=idioma_destino)
        return traducao.text
    except Exception as e:
        logging.exception(f"Erro na tradução para o texto: '{texto[:50]}...' e idioma_destino: {idioma_destino}")
        raise Exception(f'Erro na tradução: {str(e)}') from e

# Interface principal
def main():
    st.title("TradutorIA")
    st.markdown("---")
    
    # Dicionário de idiomas
    idiomas = {
        'Inglês': 'en',
        'Espanhol': 'es',
        'Francês': 'fr'
    }
    
    # Interface mais leve
    with st.container():
        selecao = st.selectbox('Idioma de destino:', list(idiomas.keys()))
        texto_original = st.text_area('Texto em português: ', max_chars=500)
        
        col1, col2 = st.columns(2)
        
        if texto_original.strip():
            with col1:
                if st.button('Traduzir com Refinamento IA', type='primary'): # Changed button label
                    try:
                        tokenizer, modelo = carregar_modelo()
                        if tokenizer and modelo:
                            with st.spinner('Processando...'):
                                texto_processado = gerar_texto_bloom(texto_original, tokenizer, modelo)
                                traducao = traduzir(texto_processado, idiomas[selecao])
                                st.success(traducao)
                    except Exception as e:
                        st.error(f'Erro: {str(e)}')
            
            with col2:
                if st.button('Tradução Direta'):
                    try:
                        with st.spinner('Traduzindo...'):
                            traducao = traduzir(texto_original, idiomas[selecao])
                            st.success(traducao)
                    except Exception as e:
                        st.error(f'Erro: {str(e)}')

    # Footer leve
    st.markdown("---")
    st.markdown("**Dica**: Textos mais curtos têm melhor performance.")

if __name__ == "__main__":
    main()
