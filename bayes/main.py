import pandas as pd
import csv
import re
import tkinter
from tkinter import filedialog
from tkinter import ttk
from nltk.stem.porter import PorterStemmer

import stopwords

regex = '[^A-Za-z ]'

stop_words = stopwords.get_stopwords('english')

porter = PorterStemmer()


def study():
    file_name = filedialog.askopenfilename()
    ham = {}
    spam = {}

    with open(file_name) as reader:
        csv_reader = csv.reader(reader)
        for row in csv_reader:
            if re.match('ham', row[0]):
                split = row[1].split(' ')
                for word in split:
                    new_word = re.sub(regex, '', word).lower()
                    if new_word not in stop_words:
                        new_word = porter.stem(new_word)
                        ham[new_word] = ham.setdefault(new_word, 0) + 1
            elif re.match('spam', row[0]):
                for word in split:
                    new_word = re.sub(regex, '', word).lower()
                    if new_word not in stop_words:
                        new_word = porter.stem(new_word)
                        spam[new_word] = spam.setdefault(new_word, 0) + 1

    ham_sorted = dict(sorted(ham.items(), key=lambda x: x[1], reverse=True))
    spam_sorted = dict(sorted(spam.items(), key=lambda x: x[1], reverse=True))

    with open("sms_spam.csv", 'w') as sms_spam:
        writer = csv.writer(sms_spam)
        for key, value in spam_sorted.items():
            writer.writerow([key, value])

    with open("sms_ham.csv", 'w') as sms_ham:
        writer = csv.writer(sms_ham)
        for key, value in ham_sorted.items():
            writer.writerow([key, value])


def categorize():
    result_label.config(text='')
    hams = pd.read_csv('sms_ham.csv', header=None,
                       index_col=0, squeeze=True).to_dict()
    spams = pd.read_csv('sms_spam.csv', header=None,
                        index_col=0, squeeze=True).to_dict()

    input_text = str(enter_text.get())

    input_array = []
    for word in re.sub(regex, '', input_text).lower().split(" "):
        if word != '':
            if word not in stop_words:
                input_array.append(word)

    p_input_text_is_ham = 1
    p_input_text_is_spam = 1
    number_of_all_hams = 0
    number_of_all_spams = 0
    number_of_all_unknown_hams = 0
    number_of_all_unknown_spams = 0

    for word_count in hams.values():
        number_of_all_hams += int(word_count)

    for word_count in spams.values():
        number_of_all_spams += int(word_count)

    p_ham = number_of_all_hams / (number_of_all_hams + number_of_all_spams)
    p_spam = number_of_all_spams / (number_of_all_hams + number_of_all_spams)

    for word in input_array:
        if word not in hams.keys():
            number_of_all_unknown_hams += 1
        if word not in spams.keys():
            number_of_all_unknown_spams += 1

    for word in input_array:
        if word in hams.keys():
            p_input_text_is_ham *= (int(hams[word]) + 1) / \
                (len(hams) + number_of_all_unknown_hams)
        else:
            p_input_text_is_ham *= 1 / (len(hams) + number_of_all_unknown_hams)
        if word in spams.keys():
            p_input_text_is_spam *= (int(spams[word]) + 1) / \
                (len(spams) + number_of_all_unknown_spams)
        else:
            p_input_text_is_spam *= 1 / \
                (len(spams) + number_of_all_unknown_spams)

    p_input_text_is_ham *= p_ham
    p_input_text_is_spam *= p_spam

    if p_input_text_is_ham > p_input_text_is_spam:
        result_label.config(text="It's ham")
    else:
        result_label.config(text="It's spam")


master = tkinter.Tk()

enter_text = tkinter.Entry(master, width=50)
choose_file_button = ttk.Button(master, text='choose file', command=study)
search_button = ttk.Button(master, text='categorize', command=categorize)
result_label = tkinter.Label(master, text='')

enter_text.grid(column=0, row=0)
choose_file_button.grid(column=1, row=0)
search_button.grid(column=0, row=1)
result_label.grid(column=1, row=1)

master.mainloop()
