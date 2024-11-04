import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
from googletrans import Translator
import torch

# Configuração da página
st.set_page_config(
    page_title="TradutorIA",
    page_icon="🌎",
    layout="centered"
)

# Cache do modelo para economia de memória
@st.cache_resource(show_spinner=False)
def carregar_modelo():
    try:
        # Configuração para usar menos memória
        config = {
            "low_cpu_mem_usage": True,
            # Removemos torch_dtype para usar o padrão
        }
        
        tokenizer = AutoTokenizer.from_pretrained(
            "bigscience/bloom-560m",
            **config
        )
        modelo = AutoModelForCausalLM.from_pretrained(
            "bigscience/bloom-560m",
            **config
        )
        return tokenizer, modelo
    except Exception as e:
        st.error(f'Erro ao carregar o modelo: {str(e)}')
        return None, None

# Função otimizada para gerar texto
def gerar_texto_bloom(texto, tokenizer, modelo, max_length=50):
    try:
        with torch.inference_mode():
            # Adiciona um prompt mais específico para manter o foco
            prompt = f"Traduza o seguinte texto mantendo o significado original: {texto}"
            
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
                temperature=0.3,          # Reduzido de 0.7 para 0.3 (menos criativo)
                num_return_sequences=1,
                repetition_penalty=1.5,   # Aumentado para evitar repetições
                no_repeat_ngram_size=3,
                do_sample=True,
                top_k=20,                 # Reduzido de 40 para 20 (mais focado)
                top_p=0.7,                # Reduzido de 0.9 para 0.7 (mais conservador)
                pad_token_id=tokenizer.pad_token_id
            )
            
            texto_gerado = tokenizer.decode(saidas[0], skip_special_tokens=True)
            
            # Remove o prompt da saída se necessário
            if "Traduza o seguinte texto" in texto_gerado:
                texto_gerado = texto_gerado.split(": ", 1)[-1]
                
            return texto_gerado
    except Exception as e:
        raise Exception(f'Erro na geração de texto: {str(e)}')

# Função de tradução otimizada
@st.cache_data(show_spinner=False)
def traduzir(texto, idioma_destino):
    try:
        tradutor = Translator()
        traducao = tradutor.translate(texto, src='pt', dest=idioma_destino)
        return traducao.text
    except Exception as e:
        raise Exception(f'Erro na tradução: {str(e)}')

# Interface principal
def main():
    st.title("🌎 TradutorIA")
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
                if st.button('Traduzir com IA', type='primary'):
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
    st.markdown("💡 **Dica**: Textos mais curtos têm melhor performance.")

if __name__ == "__main__":
    main()
