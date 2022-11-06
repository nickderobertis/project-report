from typing import Optional


def get_first_non_empty_line_of_text(text: str) -> Optional[str]:
    lines = text.splitlines()
    for line in lines:
        if line.strip():
            return line
    return None
