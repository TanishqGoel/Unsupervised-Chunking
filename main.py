import re
import numpy as np

f = open('abc.txt', 'r') # file input
raw = f.read()
raw = raw.rstrip("\n")
raw = raw+"\n"
raw = re.split("\n", raw)

# print(f)
# print(raw)
total_sent = []
temp = []
for i in raw:
    if (i == ""):
        total_sent.append(temp)
        temp = []
        continue
    i = re.split("\t", i)
    temp.append(tuple(i))
# print(total_sent)

poslist = ['DM_DMD', 'N_NNP', 'PSP', 'RP_INTF', 'JJ', 'N_NN', 'QT_QTC', 'V_VM', 'RD_PUNC', 'PR_PRP', 'V_VAUX', 'N_NST', 'CC_CCD',
           'PR_PRL', 'RP_RPD', 'RD_SYM', 'QT_QTF', 'PR_PRF', 'PR_PRQ', 'RP_NEG', 'RB', 'QT_QTO', 'CC_CCS', 'RD_UNK', 'RP_INJ', 'RD_ECH']

cluster_list = []

for sent in total_sent:

    temp1 = []
    for index,word in enumerate(sent):
        temp = []
        if (re.search(".*N_N.*", word[1]) or re.search("V_V[^AUX].*", word[1]) or re.search(".*CC.*", word[1]) or re.search("PR_*", word[1]) or (word[0] == '।')):
            temp.append(index)
            temp1.append(temp)
    cluster_list.append(temp1)

# print(cluster_list)

for sent_num, sent in enumerate(total_sent):

    sent_copy1 = [i for i,ii in enumerate(sent)] # sent is like actual sentence. sent_copy has all the indexes of the words i order of sentence
    sent_copy = list(sent_copy1)
    # sent_copy1 = list(sent)
    # print(sent)
    # print(sent_copy)
    # print(sent_copy1)
    iter = 0
    while len(sent_copy1)!=0:
        iter += 1
        initial_length = len(sent_copy1)
        sent_copy = list(sent_copy1)
        for word_ind in sent_copy:
            # print(word_ind,sent[word_ind])
            for cluster in cluster_list[sent_num]:
                
                # print(cluster)
                if word_ind in cluster:
                    sent_copy1.remove(word_ind)
                
                elif (word_ind == (cluster[0]-1)):
                    # print("AAAA")
                    temp_pos = [sent[k][1] for k in cluster]
                    # print(temp_pos)
                    for zz in temp_pos:

                        if re.search(".*N_N.*", zz):
                            if re.search("DM.*|JJ.*|QT.*|RP_INTF", sent[word_ind][1]):
                                cluster.insert(0,word_ind)

                                sent_copy1.remove(word_ind)
                                break
                        
                        elif re.search("V_.*", zz):
                            if re.search(".*NEG.*", sent[word_ind][1]):
                                cluster.insert(0, word_ind)

                                sent_copy1.remove(word_ind)
                                break
                elif (word_ind == (cluster[-1]+1)):
                    temp_pos = [sent[k][1] for k in cluster]
                    for zz in temp_pos:

                        if re.search(".*N_N.*", zz):
                            if re.search("PSP|RP_[^INTF]", sent[word_ind][1]):
                                cluster.append(word_ind)
                                sent_copy1.remove(word_ind)
                                break
                        
                        elif re.search("V_.*", zz):
                            if re.search("PSP|.*AUX.*|.*NEG.*", sent[word_ind][1]):
                                cluster.append(word_ind)
                                sent_copy1.remove(word_ind)
                                break

            # print("===========")

        if len(sent_copy) == initial_length:
            # print(sent_copy1)
            for remain_word_ind in sent_copy1:
                for cluster in cluster_list[sent_num]:

                    if remain_word_ind == cluster[-1]+1:
                        cluster.append(remain_word_ind)
                        sent_copy1.remove(remain_word_ind)
                        break
        # if iter >= 4:
        #     break


print(cluster_list)


