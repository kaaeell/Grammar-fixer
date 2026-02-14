import urllib.request
import urllib.parse
import json
import sys

# free api, no key. has rate limits but fine for personal use
API_URL = "https://api.languagetool.org/v2/check"


def check_text(text, lang="en"):
    # send text to LanguageTool, get back errors and suggested fixes
    data = urllib.parse.urlencode({"text": text, "language": lang}).encode()
    req = urllib.request.Request(
        API_URL,
        data=data,
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())


def apply_fixes(original, matches):
    # apply all replacements. end to start so offsets don't shift
    if not matches:
        return original

    # sort by offset descending so we replace from the end first
    sorted_matches = sorted(matches, key=lambda m: m["offset"], reverse=True)
    result = original

    for m in sorted_matches:
        offset = m["offset"]
        length = m["length"]
        replacements = m.get("replacements") or []
        if not replacements:
            continue
        # first suggestion is usually the one you want
        new_bit = replacements[0].get("value", "")
        result = result[:offset] + new_bit + result[offset + length :]

    return result


def main():
    if len(sys.argv) > 1:
        # text was passed in the command line
        text = " ".join(sys.argv[1:])
    else:
        print("Paste your text (press Enter, then Ctrl+Z and Enter on Windows, or Ctrl+D on Mac/Linux to finish):")
        try:
            lines = sys.stdin.read()
        except KeyboardInterrupt:
            sys.exit(0)
        text = lines.strip()

    if not text:
        print("No text to check.")
        sys.exit(1)

    print("Checking...")
    try:
        data = check_text(text)
    except Exception as e:
        print("Something went wrong:", e)
        sys.exit(1)

    matches = data.get("matches") or []
    fixed = apply_fixes(text, matches)

    print()
    print("--- Corrected text ---")
    print(fixed)
    print()

    if matches:
        print(f"(Fixed {len(matches)} issue(s). Powered by LanguageTool: https://languagetool.org)")
    else:
        print("Nothing to fix.")


if __name__ == "__main__":
    main()
