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
import xml.etree.ElementTree as axml

def main():
    # detect_smali_folders('C:/Users/kirill/Desktop/apktool/target/')
    generate_manifest()
    
    # apk_path1 = input("Введите путь до первого апк >> ")
    # apk_path2 = input("Введите путь до второго апк >> ")
    # print("Слияние апк началось...")
    # decompilled_apk1 = decompile_apk(apk_path = apk_path1)
    # decompilled_apk2 = decompile_apk(apk_path = apk_path2)
    pass

def decompile_apk(apk_path):
    name = os.path.splitext(apk_path)[0][:os.path.splitext(apk_path)[0].index('.')]
    print(f'Декомпиляция апк. Путь: {apk_path} Имя {name}')
    subprocess.call(f"java -jar /tools/apktool.jar d {apkpath} -o /tmp/{name}")
    return f'/tmp/{name}/'

def detect_smali_folders(decompilled_apk_path):
    listdirs = listdir(decompilled_apk_path)
    smali_dirs = []
    for dirname in listdirs:
        if not dirname.find('smali'):
            smali_dirs.append(dirname)
    
    return smali_dirs


def copy_files(path1, path2):
    shutil.copytree(path1+'/', 'tmp/output/') # копирование целиком path1 в output
    detected_smali_folders = detect_smali_folders(path2) # находим папки smali в path2
    for file in detect_smali_folders(detected_smali_folders): # проходимся по папкам
        shutil.copytree(path2+'/'+file, 'tmp/output/') # копируем содержимое smali папок в output
    shutil.copytree(path2+'/unknown/', 'tmp/output/unknown') # копируем содержимое папки unknown в output/unknown
    pass

def generate_manifest():
    data = axml.parse('tmp/output/main.xml') # подгружаем изменяемый xml файл
    data2 = axml.parse('tmp/output/target.xml') # подгружаем второй xml файл

    root = data.getroot() # получаем root (tag <Manifest>)
    root2 = data2.getroot() # получаем root второго xml (tag <manifest>)

    activityes = root.find('application').findall('activity') #получаем список активити
    activityes2 = root2.find('application').findall('activity') #получаем список активити

    #перенос всех ненайденных активити
    for act in activityes2:
        act_name = act.attrib['{http://schemas.android.com/apk/res/android}name']
        if act_name not in activityes:
            print(f"Добавлено активити {act_name}")
            root.find('application').append(act)

    #перенос всех ненайденых сервисов

    services = root.find('application').findall('service')
    services2 = root2.find('application').findall('service')

    for serv  in services2:
        serv_name = serv.attrib['{http://schemas.android.com/apk/res/android}name']
        if serv_name not in services:
            print(f"Добавлен сервис {serv_name}")
            root.find('application').append(serv)


    #перенос всех ненайденных разрешений
    perms = root.findall('uses-permission')
    perms2 = root2.findall('uses-permission')

    for perm in perms2:
        perm_name = perm.attrib['{http://schemas.android.com/apk/res/android}name']
        if perm_name not in perms:
            print(f"Добавлено ненайденное разрешение {perm_name}")

    # 
            
        

    # выбор главного активити
    activityes = root.find('application').findall('activity')
    activity_list = []
    idx = 0
    for activity in activityes:
        act_name = activity.attrib['{http://schemas.android.com/apk/res/android}name']
        activity_list.append(act_name)
        print(str(idx) + ". " +act_name)
        idx += 1

    #удаляем все intent filter
    for act in activityes:
        if act.find('intent-filter'):
            act.remove(act.find('intent-filter'))
    
    main_act_index = input("Выберите главное активити >> ")
    choosed_main_act_name = activity_list[int(main_act_index)]
    for i in activityes:
        act_name = i.attrib['{http://schemas.android.com/apk/res/android}name']
        if act_name == choosed_main_act_name:
            #добавляем launcher intent filter
            intent_filter = axml.Element('intent-filter')
            action = axml.Element('action')
            action.set('{http://schemas.android.com/apk/res/android}name', 'android.intent.action.MAIN')
            category = axml.Element('category')
            category.set('{http://schemas.android.com/apk/res/android}name', 'android.intent.category.LAUNCHER')
            intent_filter.append(action)
            intent_filter.append(category)
            i.append(intent_filter)

    data.write('output.xml')
    pass

def build(target):
    pass


if __name__ == '__main__':
    main()