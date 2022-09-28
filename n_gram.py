"""
n-gram分词器
@auther aldebran
@since 2022-09-24
"""
import re

# 对句子分组
from collections import defaultdict


# NGramTokenizer 实现
# TODO 目前只处理了2字和3字词
class NGramTokenizer():
    def __init__(self, train_data=[]):  # train_data是由文章构成的列表
        self.sentences_count = 0
        self.decrease_count = 500  # 每隔decrease_count个句子缩减一下词表，可以自定义
        self.word_count_map = defaultdict(int)
        self.current_id = 0  # word id是auto_increment的
        self.word_id_map = dict()  # 用于给每个'词'唯一编号
        self.train(train_data)  # 支持构造训练
        pass

    # 从文件中训练
    def train_from_files(self, files):
        for file in files:
            with open(file, 'r', encoding='utf-8') as file_obj:
                self.train([file_obj.read()])
        pass

    # 从句子中训练（其实就是求词频）
    def train(self, train_data=[]):
        for article in train_data:
            sentences = get_sentences(article)
            for sentence in sentences:
                # print(self.sentences_count)
                if (self.sentences_count % self.decrease_count == 0):
                    # print('开始缩减列表......')
                    # TODO 为防止map过大，可能考虑定期删除低频词
                    # self.filtration()
                    pass
                for group_size in [2, 3]:
                    for word in groups(sentence, group_size):
                        self.word_count_map[word] = self.word_count_map[word] + 1
                        if (word not in self.word_id_map):
                            self.word_id_map[word] = self.current_id
                            self.current_id = self.current_id + 1
                self.sentences_count = self.sentences_count + 1  # py不支持i++语法...
        pass

    def add_words(self, words_count_map):
        for word in words_count_map:
            self.word_count_map[word] = words_count_map[word]
            if word not in self.word_id_map:
                self.word_id_map[word] = self.current_id
                self.current_id += 1

    # 过滤无效词，它会影响结果、内存效率和时间效率
    def filtration(self):
        exclude_rate = 0.15
        l = sorted(set(self.word_count_map.values()), reverse=True)
        end = int(len(l) * (1 - exclude_rate))
        print(l)
        if end > 0:
            l = l[0:end]
        print(l)
        min_v = min(l)
        exclude_keys = []
        for k in self.word_count_map.keys():
            v = self.word_count_map[k]
            if (v < min_v):
                exclude_keys.append(k)
        for k in exclude_keys:
            del self.word_count_map[k]
            del self.word_id_map[k]

    # 分词 这种方式效果不好（不推荐使用!）
    def tokenize(self, text=""):
        result = []
        sentences = get_sentences(text)
        for sentence in sentences:
            # print(sentence)
            if (re.compile('\d+').fullmatch(sentence)):  # 数字直接追加
                result.append(sentence)
            i = 0
            while i < len(sentence):
                p = 0.0  # 最终概率
                word = ""  # 最终词
                # 2字、3字
                for chars_count in [2, 3, ]:
                    end = i + chars_count
                    if (end <= len(sentence)):  # 有可能剩余长度不够了...
                        current_word = sentence[i:end]  # 获取当前词
                        current_p = self.word_count_map[current_word] / len(self.word_count_map)  # 计算当前词概率

                        # print("current_word: %s, current_p: %s" % (current_word, current_p))
                        if (current_p > p):  # 考虑更高的频率
                            word = current_word
                            p = current_p
                if (word == ""):  # 如果没有匹配，输出单字
                    word = sentence[i]
                result.append(word)
                i += len(word)  # i移动的位数取决于单词长度
        return list(filter(lambda it: len(it) != 0, result))

    pass


def groups(sentence="", group_size=1):
    # 最后的索引(从1开始)必然是len(sentence)-(group_size-1)=len(sentence)-group_size+1
    # range左闭右开，所以结尾索引（从0开始）是len(sentence)-group_size+1
    result = []
    for i in range(0, len(sentence) - group_size + 1):
        result.append(sentence[i:i + group_size])
    return result


# 预处理一下句子
def get_sentences(sentence=""):
    return list(filter(
        lambda it: it is not None and it != '',
        re.split(re.compile(',|，|。|:|：|\d+|（|）|\(|\)|\s+|、|\'|"|“|”|；|;|《|》|·|[a-z|A-Z]+|/'), sentence)))
