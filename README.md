# TradutorIA

Web application that refines Portuguese text with a language model before translating it into English, Spanish or French.

**Live demo:** https://tradutoria-bloom.streamlit.app/

## Why this exists

Machine translation degrades when the source text is unclear — long sentences, informal register, ambiguous pronouns. TradutorIA inserts a refinement step *before* translation: the Portuguese input is first rewritten by BLOOM 560M for clarity, then translated. The app exposes both paths side by side so the effect of the refinement step is visible rather than assumed.

## How it works

```
Portuguese input
      │
      ├─► direct path ──────────────► Google Translate ──► output
      │
      └─► BLOOM 560M (refinement) ──► Google Translate ──► output
```

Both outputs are shown in the interface, so the user compares refined vs. direct translation for the same input.

## Features

- Refinement of the Portuguese source with BLOOM 560M before translation
- Direct translation path for comparison
- Target languages: English, Spanish, French
- Responsive web interface (Streamlit)

## Stack

Python · Streamlit · Hugging Face Transformers (BLOOM 560M) · PyTorch · `googletrans`

## Running locally

```bash
git clone https://github.com/maxsampa/TradutorIA.git
cd TradutorIA

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
streamlit run TradutorIA.py
```

First run downloads the BLOOM 560M weights (~1.1 GB). Expect a slow cold start.

**Requirements:** Python 3.10+ and roughly 4 GB of free RAM for the refinement model.

## Known limitations

- **BLOOM 560M cost:** the model is computationally heavy. Local execution can be slow, and the first load downloads and caches the weights.
- **`googletrans` stability:** the library relies on unofficial Google Translate endpoints and can break without notice if those endpoints change. A production version would use the paid Cloud Translation API.
- **Refinement input length:** capped at 512 tokens. Longer texts are truncated before refinement.
- **Refinement quality varies:** the rewriting is model-generated. It improves clarity in most cases but is not guaranteed to preserve every nuance — see Evaluation.
- **No domain adaptation:** technical or specialized vocabulary is not handled specially.

## Not intended for

Legal, medical or contractual translation, or any use where a mistranslation carries material consequence.

## License

MIT — see [LICENSE](LICENSE).

---

Originally developed as an academic project (UPE, Especialização em IA Generativa) and maintained since.
