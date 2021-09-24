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

ham_words = {}
for k in ham_sorted.keys():
    ham_words[len(k)] = ham_words.setdefault(len(k), 0) + 1

spam_words = {}
for k in spam_sorted.keys():
    spam_words[len(k)] = spam_words.setdefault(len(k), 0) + 1

ham_length = 0
ham_sum = 0
for key, value in ham_words.items():
    ham_length += int(key) * int(value)
    ham_sum += value

spam_length = 0
spam_sum = 0
for key, value in spam_words.items():
    spam_length += int(key) * int(value)
    spam_sum += value

sms_length = ham_length + spam_length
sms_sum = ham_sum + spam_sum
average = sms_length / sms_sum

pylab.subplot(2, 2, 3)
pylab.bar(ham_words.keys(), height=ham_words.values())

pylab.subplot(2, 2, 3)
pylab.bar(spam_words.keys(), height=spam_words.values())

pylab.subplot(2, 2, 3)
pylab.bar(average, height=1300, color='red')

ham_messages = {}
spam_messages = {}
total_len = 0
total_average = 0
with open('sms-spam-corpus.csv', 'r') as r:
    csv_reader = csv.reader(r)
    for row in csv_reader:
        if re.match('ham', row[0]):
            ham_messages[len(row[1])] = ham_messages.setdefault(len(row[1]), 0) + 1
        elif re.match('spam', row[0]):
            spam_messages[len(row[1])] = spam_messages.setdefault(len(row[1]), 0) + 1
        total_len += len(row[1])
    total_average = total_len / csv_reader.line_num

pylab.subplot(2, 2, 4)
pylab.bar(ham_messages.keys(), height=ham_messages.values())

pylab.subplot(2, 2, 4)
pylab.bar(spam_messages.keys(), height=spam_messages.values())

pylab.subplot(2, 2, 4)
pylab.bar(total_average, height=80, color='red')

pylab.show()
