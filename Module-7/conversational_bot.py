"""
Module 7 Lab: Build a Simple Conversational Bot
Author: Vrajkumar Patel
Date: 11/10/2025
This script implements a simple conversational bot that:
- Greets the user and explains how to quit.
- Accepts user input in a loop until the user types "quit".
- Responds with random, generic conversational prompts using random.choice().
- Occasionally mirrors the user's input via simple string manipulation.

Run this file directly with Python:
    python conversational_bot.py
"""

import random


def get_random_prompt() -> str:
    """Return a random conversational prompt from a predefined list.

    The list contains simple, generic prompts designed to keep a conversation
    flowing. These prompts do not perform any real understanding.
    """
    prompts = [
        "That’s interesting. Can you tell me more?",
        "How does that make you feel?",
        "What do you think led to that?",
        "Why do you think that is?",
        "What happened next?",
        "How long has this been on your mind?",
        "What would you like to do about it?",
        "Has this happened before?",
        "What else comes to mind when you think about this?",
        "If you could change one thing, what would it be?",
        "How are you handling this so far?",
        "What makes this important to you?",
    ]
    return random.choice(prompts)


def reflect_pronouns(text: str) -> str:
    """Naively reflect some first- and second-person pronouns in a string.

    This is a very lightweight approach to create the illusion of understanding
    and works adequately for simple mirroring. It is not grammatically perfect.
    """
    # Token-based replacement keeps things simple. We lower-case to match keys
    # but preserve original casing in a basic way by reusing the original token
    # when replacement is not found.
    replacements = {
        "i": "you",
        "me": "you",
        "my": "your",
        "mine": "yours",
        "am": "are",
        "you": "I",
        "your": "my",
        "yours": "mine",
    }

    tokens = text.split()
    reflected = []
    trailing_punct = set([".", ",", "!", "?", ";", ":"])
    for tok in tokens:
        # Separate trailing punctuation to avoid affecting replacement.
        punct = ""
        if tok and tok[-1] in trailing_punct:
            punct = tok[-1]
            core = tok[:-1]
        else:
            core = tok

        lower = core.lower()
        if lower in replacements:
            rep = replacements[lower]
            if core and core[0].isupper():
                rep = rep.capitalize()
            reflected.append(rep + punct)
        else:
            reflected.append(core + punct)
    return " ".join(reflected)


def maybe_mirror_response(user_text: str, probability: float = 0.3) -> str | None:
    """Occasionally produce a mirrored response based on the user's input.

    With a given probability, attempt light pattern matching to mirror the
    user's input, otherwise return None to indicate no mirroring.
    """
    cleaned = user_text.strip()
    if not cleaned:
        return None

    if random.random() >= probability:
        return None

    lowered = cleaned.lower()

    # If the user asks a question, invite their perspective.
    if cleaned.endswith("?"):
        return "What do you think the answer might be?"

    # Helper to extract the remainder after any matching prefix.
    def after_prefix(text: str, prefixes: list[str]) -> str | None:
        lt = text.lower()
        for p in prefixes:
            if lt.startswith(p):
                return text[len(p) :].strip()
        return None

    # Tailored mirroring patterns for common phrases
    feel = after_prefix(cleaned, ["i feel ", "i’m feeling ", "i am feeling "])
    if feel:
        return f"Why do you feel {feel}?"

    identity = after_prefix(cleaned, ["i am ", "i’m "])
    if identity:
        return f"Why are you {identity}?"

    think = after_prefix(cleaned, ["i think "])
    if think:
        return f"What makes you think {think}?"

    want = after_prefix(cleaned, ["i want "])
    if want:
        return f"Why do you want {want}?"

    like = after_prefix(cleaned, ["i like "])
    if like:
        return f"What about {like} makes you feel that way?"

    dislike = after_prefix(cleaned, ["i don’t like ", "i don't like "])
    if dislike:
        return f"What about {dislike} bothers you?"

    cant = after_prefix(cleaned, ["i can’t ", "i can't ", "i cannot "])
    if cant:
        return f"What makes you feel you can’t {cant}?"

    have = after_prefix(cleaned, ["i have "])
    if have:
        return f"How long have you had {have}?"

    possessive = after_prefix(cleaned, ["my "])
    if possessive:
        return f"Tell me more about your {possessive}."

    itis = after_prefix(cleaned, ["it is ", "it’s ", "it's "])
    if itis:
        return f"Why do you think it is {itis}?"

    because = after_prefix(cleaned, ["because "])
    if because:
        return f"What makes {because} important here?"

    # De-emphasize shifting to the bot
    you_start = after_prefix(cleaned, ["you "])
    if you_start:
        return "Let’s focus on you—how does that affect you?"

    # General reflection fallback
    mirrored = reflect_pronouns(cleaned)
    return f"Why do you say {mirrored}?"


def main() -> None:
    """Run the conversational bot loop until the user types 'quit'."""
    print("Bot: Hi! I’m Erica, a simple conversational bot.")
    print("Bot: Tell me anything, and type 'quit' to end our chat.")

    while True:
        try:
            user = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBot: It was nice chatting. Goodbye!")
            break

        # End the conversation when the user types 'quit' (case-insensitive).
        if user.lower() == "quit":
            print("Bot: Thanks for chatting! Take care.")
            break

        # Occasionally mirror the user's input. Otherwise, use a random prompt.
        mirrored = maybe_mirror_response(user)
        if mirrored:
            print(f"Bot: {mirrored}")
        else:
            print(f"Bot: {get_random_prompt()}")


if __name__ == "__main__":
    main()