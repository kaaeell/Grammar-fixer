# Grammar fixer

You write something (a sentence or a paragraph) and the script fixes the grammar and spelling. You get back the corrected text. It uses the free [LanguageTool](https://languagetool.org) API so no API key needed.

## Concept

You give it text—either as a command-line argument or by pasting it when the script asks. The script sends the text to LanguageTool, gets back a list of suggested fixes (grammar, spelling, punctuation, etc.), applies those fixes, and prints the corrected version.

## What I use

- **Python 3** – only built-in modules (`urllib`, `json`).
- **LanguageTool public API** – free grammar/spell check. Rate limits apply (see their site) but it’s enough for normal use.

## How to use

**Option 1 – pass text as argument**

```bash
python grammar_check.py "This is an test. I has a apple."
```

**Option 2 – run and paste**

```bash
python grammar_check.py
```

Then paste your text, press Enter, then:
- **Windows:** Ctrl+Z then Enter to finish.
- **Mac/Linux:** Ctrl+D to finish.

The script prints the corrected text. No install, no config.
