# wordsmith

A dictionary CLI built with Python and argparse, made as part of Hack Club Resolution Week 2.

Look up word definitions, quiz yourself, and track your word history — all from the terminal.

## Installation

```bash
pip install -i https://test.pypi.org/simple/ resolution-week2-suvamhere==0.1.1
```

## Usage

### Define a word

```bash
# Short — first definition only
wordsmith define serendipity --short

# Full — all definitions and examples
wordsmith define serendipity --full
```

### Quiz yourself

Give a word and a hint (first letter), and wordsmith will show you its definition. You get 3 attempts to guess it.

```bash
wordsmith quiz ephemeral e
```

```
🧠 Guess the word!

  Definition : lasting for a very short time
  Hint       : starts with 'e'

Attempt 1/3: 
```

### View history

```bash
# See all words you've looked up or quizzed
wordsmith history

# Clear history
wordsmith history --clear
```

## Example session

```
$ wordsmith define resilient --short
📖 RESILIENT

[adjective] able to withstand or recover quickly from difficult conditions.

$ wordsmith quiz candid c

🧠 Guess the word!

  Definition : truthful and straightforward; frank
  Hint       : starts with 'c'

Attempt 1/3: honest
Wrong, try again.
Attempt 2/3: candid

✅ Correct! The word was 'candid'.

$ wordsmith history

📚 Your word history:

  1. resilient (defined)
  2. candid (quizzed)
```

## Commands

| Command | Description |
|---|---|
| `define <word> --short` | Show first definition only |
| `define <word> --full` | Show all definitions and examples |
| `quiz <word> <hint>` | Guess the word from its definition |
| `history` | View your word history |
| `history --clear` | Clear all history |

## Built With

- Python
- argparse
- requests
- [Free Dictionary API](https://dictionaryapi.dev/)
