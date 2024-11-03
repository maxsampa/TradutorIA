# TradutorIA

Aplicativo de tradução desenvolvido com Python e Streamlit, utilizando o modelo Bloom para processamento de linguagem natural e Google Translator para traduções.

## Funcionalidades

- Tradução de textos do português para:
  - Inglês
  - Espanhol
  - Francês
- Processamento de texto usando modelo Bloom
- Interface web amigável
- Opção de tradução com ou sem IA

## Como usar

1. Selecione o idioma desejado no menu dropdown
2. Digite o texto em português na caixa de texto
3. Escolha entre:
   - "Traduzir com IA" para usar processamento Bloom + tradução
   - "Apenas Tradução" para tradução direta

## Instalação local

1. Clone o repositório:
```bash
git clone https://github.com/SEU_USUARIO/TradutorIA.git
cd TradutorIA
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o aplicativo:
```bash
streamlit run TradutorIA.py
```

## Tecnologias utilizadas

- Python
- Streamlit
- Transformers (Bloom)
- Google Translator
- PyTorch

## Autor

- Nome: Fabio R.
- Data: 29/10/2024

## Licença

Este projeto está sob a licença MIT.