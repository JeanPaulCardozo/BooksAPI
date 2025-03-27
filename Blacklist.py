blacklist_tokens = set()

def blacklist_token(token: str):
    blacklist_tokens.add(token)
    
def is_token_blacklisted(token: str) -> bool:
    return token in blacklist_tokens