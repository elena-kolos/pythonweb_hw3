import re

CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")

TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def normalize(name: str) -> str:
    t_name = name.translate(TRANS)
    # t_name = re.sub(r'\W', '_', t_name)
#     filename, fileExtension = split(t_name)
    t_name = re.sub(r'\W{2}', '_', t_name)
    return t_name

    #     t_name = .join(filename, fileExtension)
    #     # t_name = re.sub(r'[\w|.]', '_', t_name)

# def normalize(name: str) -> str:
#     t_name = name.translate(TRANS)
#     #t_name = re.sub(r'\W', '_', t_name)
#     filename, fileExtension = split(t_name)
#     t_name = re.sub(r'\W{2}', '_', t_name)
#     t_name = .join(filename, fileExtension)
#     # t_name = re.sub(r'[\w|.]', '_', t_name)


# def normalize(name: str) -> str:
#     t_name = name.translate(TRANS)
#     #t_name = re.sub(r'\W', '_', t_name)
#     t_name.split
#     t_name = re.sub(r'\W{2}', '_', t_name)
    # t_name = re.sub(r'[\w|.]', '_', t_name)
    # filename, fileExtension = os.path.splitext(file)
#     filename.replace(target_folder / normalize(filename.name))
#     file = os.path.join(filename, fileExtension)
