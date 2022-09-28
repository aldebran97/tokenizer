import re
from queue import Queue

from n_gram import NGramTokenizer
from n_gram import get_sentences
import sys

"""
DAG分词器实现
@author aldebran
@since 2022-09-25
"""


# 边的定义
class Link():

    def __init__(self):
        self.word = ''
        self.weight = 0

    def __str__(self):  # 类似Java重写tostring
        return "word: %s weight: %s" % (self.word, self.weight)


"""
DAG分析器继承自NGram分词器
（1）根据句子构造图，词存边上
（2）合理定义边的权重（设计为权重越小，词越重要）（负值存储）
（3）求一条最短路径作为结果
"""


class DAGTokenizer(NGramTokenizer):

    def __init__(self, train_data=[]):
        NGramTokenizer.__init__(self, train_data)

    # 重写n-gram方式中的分词，那个效果不太好，最终是求DAG最短路径
    def tokenize(self, text=""):
        sentences = get_sentences(text)
        result = []
        for sentence in sentences:
            for sp in self.deal_sentence(sentence):
                result.append(sp)
        return result

    # 处理子片段
    def deal_sentence(self, sentence=""):
        if (re.compile("\d+").fullmatch(sentence) or len(sentence) == 1):
            return [sentence]
        adjacent_matrix = []  # 假设分隔段不长，采用邻接矩阵方式存储，空间复杂度O(n^2)
        n = len(sentence)
        # 构造邻接矩阵，行数=列数=n+1
        for i in range(0, n + 1):
            adjacent_matrix.append([None] * (n + 1))
        for i in range(0, n):
            link = Link()
            link.weight = 1
            link.word = sentence[i]
            adjacent_matrix[i][i + 1] = link
        # print("%s" % adjacent_matrix)
        # print_matrix(adjacent_matrix)
        # 把词表插入图中
        for word in self.word_count_map:
            st = 0
            index = sentence.find(word, st)
            while index != -1:
                link = Link()
                link.word = word
                link.weight = self.get_weight(word)
                adjacent_matrix[index][index + len(word)] = link
                st += len(word)
                index = sentence.find(word, st)
        # print_matrix(adjacent_matrix)

        # 求最短路径，Dijkstra算法，只不过相反
        visit = [False] * (n + 1)
        min = [sys.maxsize] * (n + 1)
        prior = [None] * (n + 1)

        source = 0  # 源点索引为0
        min[source] = 0

        # 求最小距离的点
        def get_min_index():
            min_d = sys.maxsize
            min_index = -1
            for i in range(0, n + 1):
                if visit[i] is False and min[i] < min_d:
                    min_d = min[i]
                    min_index = i
            return min_index

        min_index = get_min_index()

        while min_index >= 0:
            # print("选出: %s" % min_index)
            for v2 in range(0, n + 1):
                link = adjacent_matrix[min_index][v2]
                if link is not None:
                    if min[v2] == -1:
                        min[v2] = link.weight
                        prior[v2] = min_index
                    elif min[v2] > min[min_index] + link.weight:
                        min[v2] = min[min_index] + link.weight
                        prior[v2] = min_index
            visit[min_index] = True
            min_index = get_min_index()

        print(prior)

        last = n
        ll = prior[last]
        result = []
        while ll is not None:
            result.append(adjacent_matrix[ll][last].word)
            last = ll
            if last is None or last == 0:
                break
            ll = prior[last]

        result.reverse()
        return result

    def get_weight(self, word):
        n = len(word)
        if n == 1:
            return -1
        else:
            return -pow(2, n - 1) * self.word_count_map[word]


# TODO 画出DAG 打算用d3.js实现 待完成
def draw_graph(self):
    pass


# 打印矩阵 默认会打印类似于object at 0x7f48aa967d68这种格式，即使重写了__str__也不行..... 这个Java/Kotlin很不同
def print_matrix(m):
    for i in range(0, len(m)):
        print(list(map(lambda it: str(it) if it is not None else '', m[i])))
    print()
