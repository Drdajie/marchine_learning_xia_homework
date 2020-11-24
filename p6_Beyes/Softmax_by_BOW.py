"""
思路：
    Softmax 不用多说，但是要运用到分类问题中。首先还是要根据类型种类初始化参数。
"""

import p6_Beyes.Get_Data as Get_Data
import numpy as np

TYPE_NUM = 6
FILE_PRE = '../Data/Tsinghua'
FILE_NAME = ['体育','政治','教育','法律','电脑','经济']
STOP_WORDS = Get_Data.get_stopWords(FILE_PRE + '/stop_words_zh.txt')
TRAIN_DATA = Get_Data.get_all_trainData([FILE_PRE + '/train/' + FILE_NAME[x] + '.txt' for x in range(len(FILE_NAME))])
def get_BOW_index():
    """
    得到BOW的索引表，即将 train data 中所有出现过的词进行序列化 -> 这样每个句子都可以转化为一个固定维度的向量。
    :return: 一个索引表 -> 即哪个词对应的下标是多少。
    """
    index = 0                         #新加入的词的索引值
    wordsIndexList = {}
    #访问每个文件
    for i in range(len(TRAIN_DATA)):
        #访问每个文件中的每个句子
        for j in range(len(TRAIN_DATA[i])):
            #访问每个词
            for k in range(len(TRAIN_DATA[i][j])):
                if(TRAIN_DATA[i][j][k] in wordsIndexList or TRAIN_DATA[i][j][k] in STOP_WORDS):
                    continue
                else:
                    wordsIndexList[TRAIN_DATA[i][j][k]] = index
                    index += 1
    return wordsIndexList,index
WORD_INDEX_LIST,WORD_TOTAL_NUM = get_BOW_index()


class Softmax_by_SGD:
    def __init__(self):
        pass

    def hypothesis(self,x):
        """
        计算 y_hat
        :param x: input
        :param y: ground truth
        :return: 每种类别对应的最后结果，以及 y_hat
        """
        under = 0.              #分母
        up = []                 #分子，所有最后的结果的分子
        for i in range(TYPE_NUM):
            up.append(np.exp(x @ self.theta[:,i]))
            under += up[0]
        ans = [up[i]/under for i in range(len(up))]
        y_hat = up.index(max(up))
        return ans,y_hat

    def train(self):
        #初始化参数
        self.theta = np.ones((WORD_TOTAL_NUM,TYPE_NUM))
        a = 0.1                        #learning rate
        #分别访问每个 train file
        for i in range(TYPE_NUM):
            train_data = TRAIN_DATA[i]
            #访问每个句子，对每个句子训练
            for j in range(len(train_data)):
                #将每个句子转化为 BOW 表示
                sntnRepr = np.array([0 for i in range(WORD_TOTAL_NUM)])      #sentence representation
                for k in range(len(train_data[j])):
                    if train_data[j][k] in WORD_INDEX_LIST:
                        sntnRepr[WORD_INDEX_LIST[train_data[j][k]]] += 1
            #更新参数
            #0_准备
            #求出 softmax 对当前 input 的所有种类的结果
            hAns = self.hypothesis(sntnRepr)[0]
            def error_feature(x,h,y,k):
                """
                即 (1{y = k} - h_k(x))x
                其中 k 代表现在更新的对应 k 种类的参数
                """
                if y == k:
                    return (1 - h) * x
                else:
                    return -h * x

            for j in range(TYPE_NUM):
                self.theta[:,j] += a * error_feature(sntnRepr,hAns[j],i,j)

if __name__ == "__main__":
    softm = Softmax_by_SGD()
    softm.train()