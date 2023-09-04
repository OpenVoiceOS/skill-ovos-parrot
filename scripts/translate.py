from os.path import dirname, join, isdir, exists
from pathlib import Path
import shutil
import os
import re
from ovos_utils.bracket_expansion import expand_options
from ovos_translate_plugin_deepl import DeepLTranslator


API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError

single_lang = os.getenv("TARGET_LANG")
target_langs = (single_lang,) if single_lang else ("de-de",
                                                   "ca-es",
                                                   "cs-cz",
                                                   "da-dk",
                                                   "es-es",
                                                   "fr-fr",
                                                   "hu-hu",
                                                   "it-it",
                                                   "nl-nl",
                                                   "pl-pl",
                                                   "pt-pt",
                                                   "ru-ru",
                                                   "sv-fi",
                                                   "sv-se")


base_folder = dirname(dirname(__file__))
res_folder = join(base_folder, "locale")

# old structure
old_voc_folder = join(base_folder, "vocab")
old_dialog_folder = join(base_folder, "dialog")
old_res_folder = [old_voc_folder, old_dialog_folder]

src_lang="en-us"
src_files={}
# note: regex/namedvalues are just copied, this cant be auto translated reliably
ext = [".voc", ".dialog", ".intent", ".entity", ".rx", ".value", ".word"]
untranslated = [".rx", ".value", ".entity"]

tx = DeepLTranslator({"api_key": API_KEY})


def file_location(f: str, base: str) -> bool:
    for root, dirs, files in os.walk(base):
        for file in files:
            if f == file:
                return join(root, file)
    return None

def translate(lines: list, target_lang: str) -> list:
    translations = []
    for line in lines:
        replacements = dict()
        for num, var in enumerate(re.findall(r"(?:{{|{)[ a-zA-Z0-9_]*(?:}}|})", line)):
            line = line.replace(var, f'@{num}', 1)
            replacements[f'@{num}'] = var
        try:
            translated = tx.translate(line, target=target_lang, source=src_lang)
        except Exception as e:
            continue
        for num, var in replacements.items():
            translated = translated.replace(num, var)
        translations.append(translated)

    return translations


def entities(file: str) -> set:
    vars = set()
    if not exists(file):
        return vars
    
    lines = get_lines(file)
    for line in lines:
        for var in re.findall(r"(?:{{|{)[ a-zA-Z0-9_]*(?:}}|})", line):
            vars.add(var)
    return vars


def get_lines(file: str):
    with open(file, "r") as f:
        # entity files often include #-placeholder
        if file.endswith(".entity"):
            lines = [exp for l in f.read().split("\n") for exp
                        in expand_options(l) if l]
        else:
            lines = [exp for l in f.read().split("\n") for exp
                        in expand_options(l) if l and not l.startswith("#")]
    return lines


def migrate_locale(folder):
    for lang in os.listdir(folder):
        path = join(folder, lang)
        for root, dirs, files in os.walk(path):
            for file in files:
                if file_location(file, join(res_folder, lang)) is None:
                    rel_path = root.replace(folder, "").lstrip("/")
                    new_path = join(res_folder, rel_path)
                    os.makedirs(new_path, exist_ok=True)
                    shutil.move(join(root, file),
                                join(new_path, file))
        shutil.rmtree(path)
    shutil.rmtree(folder)


for folder in  old_res_folder:
    if not isdir(folder):
        continue
    migrate_locale(folder)

src_folder = join(res_folder, src_lang)
for root, dirs, files in os.walk(src_folder):
    if src_lang not in root:
        continue
    for f in files:
        if any(f.endswith(e) for e in ext):
            file_path = join(root, f)
            rel_path = file_path.replace(src_folder, "").lstrip("/")
            src_files[rel_path] = file_path

for lang in target_langs:
    # service cant translate
    if not tx.get_langcode(lang):
        continue
    for rel_path, src in src_files.items():
        filename = Path(rel_path).name
        dst = file_location(filename, join(res_folder, lang)) or \
                join(res_folder, lang, rel_path)
        if entities(src) != entities(dst):
            if exists(dst):
                os.remove(dst)
        elif not exists(dst):
            pass
        else:
            continue
        os.makedirs(dirname(dst), exist_ok=True)

        lines = get_lines(src)
        if any(filename.endswith(e) for e in untranslated):
            tx_lines = lines
            is_translated = False
        else:
            tx_lines = translate(lines, lang)
            is_translated = True
        if tx_lines:
            tx_lines = list(set(tx_lines))
            with open(dst, "w") as f:
                if is_translated:
                    f.write(f"# auto translated from {src_lang} to {lang}\n")
                for translated in set(tx_lines):
                    f.write(translated + "\n")
