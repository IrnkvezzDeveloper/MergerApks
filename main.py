#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import codecs
import os 
from pathlib import Path
from os import listdir
import shutil
import subprocess
import datetime

def main():
    apk_path1 = input("Введите путь до первого апк >> ")
    apk_path2 = input("Введите путь до второго апк >> ")
    print("Слияние апк началось...")
    decompilled_apk1 = decompile_apk(apk_path = apk_path1)
    decompilled_apk2 = decompile_apk(apk_path = apk_path2)
    

def detect_smali_folders(decompilled_apk_path):
    pass

def decompile_apk(apk_path):
    name = os.path.splitext(apk_path)[0][:os.path.splitext(apk_path)[0].index('.')]
    print(f'Декомпиляция апк. Путь: {apk_path} Имя {name}')
    subprocess.call(f"java -jar /tools/apktool.jar d {apkpath} -o /tmp/{name}")
    return f'/tmp/{name}/'

def generate_manifest():
    pass

if __name__ == '__main__':
    main()