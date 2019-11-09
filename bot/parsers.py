import re

def keyboard_to_list(keyboard):
    l = list()
    for key in keyboard:
        l.append(key[0])
    return l

def email_validator(text):
    m = re.search(".+@open.ru", text)
    if m:
        """promise of code???"""
        return True
    else:
        return False
