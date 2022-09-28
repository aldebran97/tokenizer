from DAG import DAGTokenizer
from n_gram import groups, get_sentences, NGramTokenizer
import os
import jieba


def test_groups():
    print(groups("我们在国家博物馆游玩", 2))
    print(groups("我们在国家博物馆游玩", 1))
    print(groups("我们在国家博物馆游玩", 3))
    pass


def test_get_sentences():
    string = "其中尤以黎族文物为重，可以说是国内黎族文物收集最为全面、精品最为丰富的博物馆之一。"
    print(get_sentences(string))

    string = "2018年10月11日，入选“全国中小学生研学实践教育基地”名单。"
    print(get_sentences(string))


def test_NGramTokenizer_0():
    tokenizer = NGramTokenizer()
    tokenizer.train(["其中尤以黎族文物为重，可以说是国内黎族文物收集最为全面、精品最为丰富的博物馆之一。"])
    print(tokenizer.word_count_map)

    print(tokenizer.tokenize("其中尤以黎族文物为重，可以说是国内黎族文物收集最为全面、精品最为丰富的博物馆之一。"))
    pass


def test_NGramTokenizer():
    tokenizer = NGramTokenizer()

    files = list(map(lambda it: 'train/' + it, os.listdir('train')))
    print(files)
    tokenizer.train_from_files(files)
    print(tokenizer.word_count_map)

    tokenizer.filtration()

    print(tokenizer.word_count_map)
    print(tokenizer.tokenize("""
    博物馆是为社会服务的非营利性常设机构，它研究、收藏、保护、阐释和展示物质与非物质遗产。
    向公众开放，具有可及性和包容性，博物馆促进多样性和可持续性。博物馆以符合道德且专业的方式进行运营和交流，
    """))


def test_DAGTokenizer():
    tokenizer = DAGTokenizer()

    files = list(map(lambda it: 'train/' + it, os.listdir('train')))
    print(files)
    tokenizer.train_from_files(files)

    extra = dict()
    max = 10000000000
    extra["的"] = max
    extra["是"] = max
    extra["而且"] = max
    extra["具有"] = max

    tokenizer.add_words(extra)
    print(tokenizer.word_count_map)

    tokenizer.filtration()

    print(tokenizer.word_count_map)
    print(tokenizer.tokenize("""
    中国国家博物馆位于北京
    """))

    print(tokenizer.tokenize("""
    博物馆是为社会服务的非营利性常设机构，它研究、收藏、保护、阐释和展示物质与非物质遗产。
    向公众开放，具有可及性和包容性，博物馆促进多样性和可持续性。博物馆以符合道德且专业的方式进行运营和交流，
    """))


def test_jieba():
    print(list(jieba.tokenize("""
    博物馆是为社会服务的非营利性常设机构，它研究、收藏、保护、阐释和展示物质与非物质遗产。
    向公众开放，具有可及性和包容性，博物馆促进多样性和可持续性。博物馆以符合道德且专业的方式进行运营和交流，
    """)))


if __name__ == '__main__':
    pass
