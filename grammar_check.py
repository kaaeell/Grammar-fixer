import urllib.request
import urllib.parse
import json
import sys
import os
import datetime

API_URL = "https://api.languagetool.org/v2/check"
HISTORY_FILE = "grammar_history.json"


def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return []


def save_to_history(original, corrected, fix_count, language):
    history = load_history()
    history.append({
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "language": language,
        "fixes": fix_count,
        "original": original,
        "corrected": corrected,
    })
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def show_history():
    history = load_history()
    if not history:
        print("No history yet.")
        return
    for entry in reversed(history[-10:]):
        print(f"[{entry['timestamp']}] {entry['fixes']} fix(es) | lang: {entry['language']}")
        print(f"  before: {entry['original'][:80]}")
        print(f"  after:  {entry['corrected'][:80]}")
        print()


def check_text(text, language):
    params = urllib.parse.urlencode({
        "text": text,
        "language": language,
    }).encode("utf-8")

    req = urllib.request.Request(
        API_URL,
        data=params,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def apply_fixes(text, matches):
    # go from the end so offsets don't shift
    for match in sorted(matches, key=lambda m: m["offset"], reverse=True):
        replacements = match.get("replacements", [])
        if not replacements:
            continue
        start = match["offset"]
        end = start + match["length"]
        text = text[:start] + replacements[0]["value"] + text[end:]
    return text


def fix(text, language):
    result = check_text(text, language)
    matches = result.get("matches", [])
    lang = result.get("language", {}).get("detectedLanguage", {}).get("code", language)
    fixed = apply_fixes(text, matches)

    if not matches:
        print("No issues found!")
    else:
        print(f"{len(matches)} change(s):")
        for m in matches:
            start = m["offset"]
            end = start + m["length"]
            before = text[start:end]
            repls = m.get("replacements", [])
            after = repls[0]["value"] if repls else "(removed)"
            note = m.get("rule", {}).get("description") or m.get("message", "")
            print(f'  "{before}" -> "{after}"  ({note})')
        print(f"\nCorrected:\n{fixed}")

    save_to_history(text, fixed, len(matches), lang)


def main():
    args = sys.argv[1:]
    language = "auto"

    if "--lang" in args:
        i = args.index("--lang")
        if i + 1 < len(args):
            language = args[i + 1]
            args = args[:i] + args[i + 2:]

    if "--history" in args:
        show_history()
        return

    if args:
        fix(" ".join(args), language)
    else:
        print("Paste your text, then Ctrl+D (Mac/Linux) or Ctrl+Z + Enter (Windows):\n")
        text = sys.stdin.read().strip()
        if text:
            fix(text, language)


if __name__ == "__main__":
    main()
