# Grammar fixer

You write something (a sentence or a paragraph) and the script fixes the grammar and spelling. You get back the corrected text. It uses the free [LanguageTool](https://languagetool.org) API so no API key needed.

## Concept

You give it text—either as a command-line argument or by pasting it when the script asks. The script sends the text to LanguageTool, gets back a list of suggested fixes (grammar, spelling, punctuation, etc.), applies those fixes, and prints the corrected version.

## What I use

* **Python 3** – only built-in modules (`urllib`, `json`, `os`, `datetime`).
* **LanguageTool public API** – free grammar/spell check. Rate limits apply (see their site) but it's enough for normal use.

## How to use

**Option 1 – pass text as argument**

```
python grammar_check.py "This is an test. I has a apple."
```

**Option 2 – run and paste**

```
python grammar_check.py
```

Then paste your text, press Enter, then:

* **Windows:** Ctrl+Z then Enter to finish.
* **Mac/Linux:** Ctrl+D to finish.

**Option 3 – fix text in another language**

```
python grammar_check.py --lang de "Das ist ein Fehler."
```

Pass any LanguageTool language code (`en-US`, `en-GB`, `de`, `fr`, `es`, `pt`, etc.). Defaults to `auto`.

**Option 4 – view past corrections**

```
python grammar_check.py --history
```

## What was added

**It now shows what changed** – before it just printed the corrected text. Now it lists each fix with a short reason:

```
2 change(s):
  "an test" -> "a test"  (Use of 'a' vs. 'an')
  "I has" -> "I have"  (Agreement: subject and verb)

Corrected:
This is a test. I have an apple.
```

**History** – corrections get saved to `grammar_history.json` automatically. Run `--history` to see the last 10 with timestamps and a before/after preview.

**`--lang` flag** – lets you check text in other languages, not just English.
