from .models import Book

def find_best_book_match(user_input):
    query_norm = normalize_title(user_input)

    # Load candidates (limit for performance)
    candidates = Book.objects.all().only("name")[:5000]

    best_match = None
    best_score = 0

    for book in candidates:
        book_norm = normalize_title(book.name)

        # Simple token overlap score
        input_tokens = set(query_norm.split())
        book_tokens = set(book_norm.split())

        score = len(input_tokens & book_tokens)

        if score > best_score:
            best_score = score
            best_match = book.name

    # Threshold prevents garbage matches
    if best_score >= 2:
        return best_match

    return None


import re

def normalize_title(title: str) -> str:
    title = title.lower()
    title = re.sub(r"[^\w\s]", "", title)  # remove punctuation
    title = re.sub(r"\s+", " ", title)     # normalize spaces
    return title.strip()
