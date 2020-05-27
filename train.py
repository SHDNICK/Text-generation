import random
import argparse
import json
import re
import os
from sys import stdin
from collections import defaultdict


# функция, которая ищет слова состоящие из букв английского и русского алфавита
def split(line):
    result = re.findall(r'[A-Za-zА-Яа-я]+', line)
    return result


# функция, которая  приводит слова в строке(если надо) к нижнему регистру
def lower_case(cur_list, args):
    if args.lc:
        for i in range(len(cur_list)):
            cur_list[i] = cur_list[i].lower()
    return cur_list


# функция, которая по заданной строке составляет словарь
def dictionary_entry(line, Dictionary, last_word_in_line, is_first_in_line, args):
    cur_line = split(line)
    if len(cur_line) > 0:
        cur_line = lower_case(cur_line, args)
        if is_first_in_line:
            Dictionary[last_word_in_line][cur_line[0]] += 1
            is_first_in_line = False
        for first, second in zip(cur_line, cur_line[1:]):
            Dictionary[first][second] += 1
        last_word_in_line = cur_line[len(cur_line) - 1]
    is_first_in_line = True
    return Dictionary, last_word_in_line, is_first_in_line

 
# инициализация парсера с аргументами
def init_parser():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--input-dir", action="store", required=False,
       metavar="input.txt", help="Path to the file")
    parser.add_argument("--model", action="store", required=True, 
        metavar="model.txt", help="Path to the model file")
    parser.add_argument("--lc", action="store_true", 
        required=False, help="Bring texts to lowercase")
    args = parser.parse_args()
    return args

    
#функция создания словаря
def dictionary_construction(args):
    path_f = []
    is_first_in_line = True
    last_word_in_line = ""
    Dictionary = defaultdict(lambda: defaultdict(int))
    # создание списка с названиями всех файлов находящихся в дирректории input-dir
    # и строим словарь в зависимости от типа ввода
    if not args.input_dir is None:
        for d, dirs, files in os.walk(args.input_dir):
            for f in files:
                path = os.path.join(d,f)
                path_f.append(path)
        for name_File in path_f:
            with open(name_File, 'r') as File:
                for line in File:
                    Dictionary, last_word_in_line, is_first_in_line = dictionary_entry(line,
                    Dictionary, last_word_in_line,
                    is_first_in_line, args)
    else:
        source = stdin
        for line in source:
            Dictionary, last_word_in_line, is_first_in_line = dictionary_entry(line,
            Dictionary, last_word_in_line, 
            is_first_in_line, args)
    return Dictionary


# записываем словарь в файл в формате json
def write_dict(args, Dictionary):
    with open(args.model, "w") as File:
        json.dump(Dictionary, File)


#функция выполняющая решение
def decision(args):
    Dictionary = dictionary_construction(args)
    write_dict(args, Dictionary)


#функция выполняющая main
def main():
    decision(init_parser())


#запуск функции main
if __name__ == '__main__':
    main()

