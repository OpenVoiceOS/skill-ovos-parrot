import os
import shutil
from os.path import dirname, join, exists

base_folder = dirname(dirname(__file__))
res_folder = join(base_folder, "locale")
voc_folder = join(base_folder, "vocab")
dialog_folder = join(base_folder, "dialog")

if exists(voc_folder):
    for lang in os.listdir(voc_folder):
        path = join(voc_folder, lang)
        os.makedirs(join(res_folder, lang), exist_ok=True)
        for f in os.listdir(path):
            shutil.move(join(path, f), join(res_folder, lang, f))
        shutil.rmtree(path)
    shutil.rmtree(voc_folder)

if exists(dialog_folder):
    for lang in os.listdir(dialog_folder):
        path = join(dialog_folder, lang)
        os.makedirs(join(res_folder, lang), exist_ok=True)
        for f in os.listdir(path):
            shutil.move(join(path, f), join(res_folder, lang, f))
        shutil.rmtree(path)
    shutil.rmtree(dialog_folder)
