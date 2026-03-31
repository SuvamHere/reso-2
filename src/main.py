import argparse
import sys
import os
import json
import requests

HISTORY_FILE = "history.json"
API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"

QUIZ_WORDS = [
    "serendipity", "ephemeral", "eloquent", "resilient", "ambiguous",
    "benevolent", "candid", "diligent", "empathy", "fervent",
    "gregarious", "humble", "integrity", "jubilant", "keen"
]


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as file:
        return json.load(file)


def save_history(history):
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=2)


def add_to_history(word, action):
    history = load_history()
    history.append({"word": word, "action": action})
    save_history(history)


def fetch_word(word):
    res = requests.get(API_URL + word)
    if res.status_code == 404:
        print(f"Word '{word}' not found. Check spelling and try again.")
        sys.exit(1)
    elif res.status_code != 200:
        print(f"API error ({res.status_code}). Try again later.")
        sys.exit(1)
    return res.json()


def cmd_define(args):
    data = fetch_word(args.word)
    add_to_history(args.word, "defined")

    phonetic = next((e["phonetic"] for e in data if e.get("phonetic")), "")
    print(f"\n📖 {args.word.upper()} {phonetic}\n")

    for entry in data:
        for meaning in entry.get("meanings", []):
            part = meaning["partOfSpeech"]
            definitions = meaning.get("definitions", [])
            if not definitions:
                continue

            if args.short:
                print(f"[{part}] {definitions[0]['definition']}")
                return

            print(f"[{part}]")
            for i, d in enumerate(definitions, 1):
                print(f"  {i}. {d['definition']}")
                if d.get("example"):
                    print(f"     Example: \"{d['example']}\"")
            print()


def cmd_quiz(args):
    word = args.word
    hint = args.hint

    data = fetch_word(word)
    add_to_history(word, "quizzed")

    # grab first available definition
    chosen_def = None
    for entry in data:
        for meaning in entry.get("meanings", []):
            defs = meaning.get("definitions", [])
            if defs:
                chosen_def = defs[0]["definition"]
                break
        if chosen_def:
            break

    if not chosen_def:
        print(f"Could not get a definition for '{word}'. Try another word.")
        sys.exit(1)

    print(f"\n🧠 Guess the word!\n")
    print(f"  Definition : {chosen_def}")
    print(f"  Hint       : starts with '{hint}'\n")

    for attempt in range(1, 4):
        guess = input(f"Attempt {attempt}/3: ").strip().lower()
        if guess == word.lower():
            print(f"\n✅ Correct! The word was '{word}'.\n")
            return
        print("Wrong, try again." if attempt < 3 else f"\n❌ Out of attempts. The word was '{word}'.\n")


def cmd_history(args):
    history = load_history()

    if args.clear:
        save_history([])
        print("History cleared.")
        return

    if not history:
        print("No words looked up yet. Try: wordsmith define <word>")
        return

    print("\n📚 Your word history:\n")
    for i, entry in enumerate(history, 1):
        print(f"  {i}. {entry['word']} ({entry['action']})")
    print()


def main():
    parser = argparse.ArgumentParser(
        prog="wordsmith",
        description="A dictionary CLI — define words, quiz yourself, track history.",
        epilog="Examples:\n  wordsmith define serendipity --full\n  wordsmith quiz ephemeral e\n  wordsmith history --clear",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True

    # define
    define_parser = subparsers.add_parser("define", help="Look up a word's definition")
    define_parser.add_argument("word", type=str, help="Word to define")
    group = define_parser.add_mutually_exclusive_group()
    group.add_argument("--short", action="store_true", help="Show only the first definition")
    group.add_argument("--full", action="store_true", help="Show all definitions and examples")

    # quiz — two positional args
    quiz_parser = subparsers.add_parser("quiz", help="Guess a word from its definition")
    quiz_parser.add_argument("word", type=str, help="The word to be quizzed on")
    quiz_parser.add_argument("hint", type=str, help="A hint e.g. first letter of the word")

    # history
    history_parser = subparsers.add_parser("history", help="View or clear your word history")
    history_parser.add_argument("--clear", action="store_true", help="Clear all history")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    if args.command == "define":
        cmd_define(args)
    elif args.command == "quiz":
        cmd_quiz(args)
    elif args.command == "history":
        cmd_history(args)


if __name__ == "__main__":
    main()  