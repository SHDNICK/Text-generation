import argparse
import random
import json
from sys import stdout


# переводит строку, когда ее длина становится достаточно большой
def line_break(s, cnt):
    cnt += 1
    if cnt > 10:
            s += '\n'
            cnt = 0
    return cnt


# инициализируем парсер с входными параметрами
def init_parser():
    parser = argparse.ArgumentParser(description="Texting generation")
    parser.add_argument("--model", action='store', metavar='model.txt', 
        required=True, help="Path to the model file")
    parser.add_argument("--seed", action='store', required=False, 
        metavar="You", help="First word")
    parser.add_argument("--length", type=int, action='store', 
        required=True, metavar="10", help="Length of the text")
    parser.add_argument("--output", action='store',
        metavar='output.txt', required=False, help="Path to output file")
    args = parser.parse_args()
    return args


# работа с входными параметрами
def get_first_word(args, Dictionary):
    if args.seed is None:
        first_word = random.choice(list(Dictionary.keys()))
    else:
        first_word = args.seed
    return first_word


# загружаем словарь в формате json, на основе которого будем генерировать наш текст
def get_dict(args):
    with open(args.model, "r") as File:
        Dictionary = json.load(File)
        File.close()
        return Dictionary


#получить длину текста
def get_length(args):
    length_of_text = args.length
    return length_of_text


#получить файл для записи
def get_file_for_write(args):
    if args.output is None:
        File = stdout
    else:
        File = open(args.output, "w")
    return File

# работа с первым словом(вдруг его нет в словаре, тогда сгенерируем случайное из списка ключей словаря)
def first_word_write(Dictionary, File, first_word):
    File.write(first_word+" ")
    cur_word = ""
    start_pos = 0
    if first_word not in Dictionary.keys():
            cur_word = random.choice(list(Dictionary.keys()))
            File.write(cur_word + " ")
            start_pos = 1
    return cur_word, start_pos


# генерируем наш строку, на основе взятого словаря, возвращаем также последнее слово
def generate(Dictionary, length_line, cur_word):
    cnt = 0
    result = ""
    for i in range(length_line):
            temp_list = list()
            if not cur_word in Dictionary.keys():
                result += cur_word+" "
                cur_word = random.choice(list(Dictionary.keys()))
                continue
            if len(Dictionary[cur_word].keys()) == 0:
                cur_word = random.choice(list(Dictionary.keys()))
                result += cur_word+" "
                cnt = line_break(File, cnt)
            else:
                sum_cnt = 0
                for key in Dictionary[cur_word].keys():# считаем сумму по значениям в словаре текущего слова
                    sum_cnt += Dictionary[cur_word][key]
                num = random.randint(1, sum_cnt) # выбираем рандомное число в диапазоне
                part_amount = 0
                for key in Dictionary[cur_word].keys():# считаем частичную сумму, пока она не станет больше выбранного числа
                    part_amount += Dictionary[cur_word][key]
                    if part_amount >= num:
                        cur_word = key
                        break
            if i == length_line - 1:
                return result

#записываем сгенерированные строки в файл
def write_to_file(Dictionary, length_of_text, File, first_word):
    cur_word, start_pos = first_word_write(Dictionary, File, first_word)
    length_line = 20;
    sum_words = 0
    while(length_of_text - start_pos > sum_words):
        line = generate(Dictionary, length_line, cur_word)#функция генерирующая строку и текующее слово
        words_line = list(line.split())
        cur_word = words_line[len(words_line) - 1]
        sum_words += length_line
        line += (cur_word + '\n')
        File.write(line)
    File.close()

#функция выполняющая решение
def decision(args):

    #получение данных из args
    Dictionary = get_dict(args)
    first_word = get_first_word(args, Dictionary)
    File = get_file_for_write(args)
    length_of_text = get_length(args)

    #запись сгенерированного текста в файл
    write_to_file(Dictionary, length_of_text, File, first_word)


#функция main 
def main():
    decision(init_parser())

#запуск функции main
if  __name__ == '__main__':
    main()

