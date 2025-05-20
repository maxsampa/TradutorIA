🤖 TradutorIA: Aplicativo web de tradução com Inteligência Artificial

Aplicação que utiliza o modelo de linguagem BLOOM para refinar o texto em português antes de traduzi-lo com o Google Translate para inglês, espanhol e francês.

🎯 Funcionalidades
- **Tradução com Refinamento IA**: O texto em português é pré-processado pelo modelo BLOOM para clareza e polimento, e depois traduzido pelo Google Translate.
- **Tradução Direta**: Utiliza o Google Translate diretamente para tradução.
- Suporte para 3 idiomas de destino: inglês, espanhol e francês.
- Interface web responsiva e amigável.

🛠️ Tecnologias
- Python
- Streamlit
- Transformers (para o modelo BLOOM 560M)
- Google Translate (via biblioteca `googletrans`)
- PyTorch

🚀 Executando Localmente

1.  **Clone o repositório:**
    ```bash
    git clone <https://github.com/seu-usuario/TradutorIA.git> # Substitua pela URL correta do seu repositório
    cd TradutorIA
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    ```
    *   No Windows:
        ```bash
        venv\Scripts\activate
        ```
    *   No macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

3.  **Instale as dependências:**
    Certifique-se de ter um arquivo `requirements.txt` no seu projeto com todas as bibliotecas necessárias (streamlit, transformers, googletrans, torch).
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute a aplicação Streamlit:**
    ```bash
    streamlit run TradutorIA.py
    ```

⚠️ Limitações e Considerações
- **Recursos do Modelo BLOOM:** O modelo BLOOM 560M é computacionalmente intensivo. Sua execução local pode ser lenta ou exigir uma quantidade significativa de RAM, especialmente na primeira vez que o modelo é baixado e carregado.
- **Estabilidade do `googletrans`:** A biblioteca `googletrans` depende de APIs não oficiais do Google Translate e pode apresentar instabilidade ou parar de funcionar se o Google alterar suas APIs.
- **Limite de Comprimento para Refinamento IA:** O pré-processamento de texto com o modelo BLOOM está configurado para um comprimento máximo (atualmente 512 tokens). Textos mais longos que isso serão truncados durante a etapa de refinamento.
- **Qualidade do Refinamento:** A qualidade do texto refinado pelo BLOOM pode variar. O objetivo é melhorar a clareza, mas o resultado é gerado por IA e pode não ser perfeito.

🎓 Projeto Acadêmico para aprendizado
Instituição: UPE

🔗 Links
App: https://tradutoria-bloom.streamlit.app/ (Nota: Este link pode apontar para uma versão anterior ou não estar atualizado com as últimas modificações locais.)
LinkedIn: https://www.linkedin.com/in/fabio-a-ribeiro/
