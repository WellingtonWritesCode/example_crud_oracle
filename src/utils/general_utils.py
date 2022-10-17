def capitalize_name(name: str) -> str:
    return " ".join(map(str.capitalize, name.split(" ")))