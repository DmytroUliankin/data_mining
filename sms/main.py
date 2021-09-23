import pandas as pd  # csv
import stopwords  # stop-word dictionary
import re  # for splitting string and using regex
import csv  # open file for create dictionaries
import pylab  # plot
import numpy  # arrays

from nltk.stem import PorterStemmer  # stemming

regex = '[^A-Za-z ]'

stop_words = stopwords.get_stopwords('english')

porter = PorterStemmer()
ham_without_stop_words = []
spam_without_stop_words = []

ham = {}
spam = {}

with open('sms-spam-corpus.csv') as reader:
    csv_reader = csv.reader(reader)
    for row in csv_reader:
        if re.match('ham', row[0]):
            split = row[1].split(' ')
            for word in split:
                new_word = re.sub(regex, '', word).lower()
                if new_word not in stop_words:
                    new_word = porter.stem(new_word)
                    ham[new_word] = ham.setdefault(new_word, 0) + 1
                    ham_without_stop_words.append(row[1])
        elif re.match('spam', row[0]):
            for word in split:
                new_word = re.sub(regex, '', word).lower()
                if new_word not in stop_words:
                    new_word = porter.stem(new_word)
                    spam[new_word] = spam.setdefault(new_word, 0) + 1
                    spam_without_stop_words.append(row[1])

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

ham_sample = pd.read_csv("sms_ham.csv", header=None, index_col=0, squeeze=True).to_dict()
ham_sample = sorted(ham_sample.items(), key=lambda item: int(item[1]), reverse=True)
ham_list = list(ham_sample)[:20]
ham_dict = {x[0]: int(x[1]) / len(ham_sample) for x in ham_list}

pylab.subplot(2, 2, 1)
pylab.bar(range(len(ham_dict)), height=ham_dict.values())
pylab.xticks(numpy.arange(len(ham_dict)), ham_dict.keys(), rotation='vertical')

spam_sample = pd.read_csv("sms_spam.csv", header=None, index_col=0, squeeze=True).to_dict()
spam_sample = sorted(spam_sample.items(), key=lambda item: int(item[1]), reverse=True)
spam_list = list(spam_sample)[:20]
spam_dict = {x[0]: int(x[1]) / len(spam_sample) for x in spam_list}

pylab.subplot(2, 2, 2)
pylab.bar(range(len(spam_dict)), height=spam_dict.values())
pylab.xticks(numpy.arange(len(spam_dict)), spam_dict.keys(), rotation='vertical')

pylab.show()
