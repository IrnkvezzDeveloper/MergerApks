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
    # detect_smali_folders('C:/Users/kirill/Desktop/apktool/target/')
    
    
    # apk_path1 = input("Введите путь до первого апк >> ")
    # apk_path2 = input("Введите путь до второго апк >> ")
    # print("Слияние апк началось...")
    # decompilled_apk1 = decompile_apk(apk_path = apk_path1)
    # decompilled_apk2 = decompile_apk(apk_path = apk_path2)
    pass


def detect_smali_folders(decompilled_apk_path):
    listdirs = listdir(decompilled_apk_path)
    smali_dirs = []
    for dirname in listdirs:
        if not dirname.find('smali'):
            smali_dirs.append(dirname)
    
    return smali_dirs

def decompile_apk(apk_path):
    name = os.path.splitext(apk_path)[0][:os.path.splitext(apk_path)[0].index('.')]
    print(f'Декомпиляция апк. Путь: {apk_path} Имя {name}')
    subprocess.call(f"java -jar /tools/apktool.jar d {apkpath} -o /tmp/{name}")
    return f'/tmp/{name}/'

def generate_manifest():
    pass

if __name__ == '__main__':
    main()