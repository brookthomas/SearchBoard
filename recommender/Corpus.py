import re

class Corpus:

    def __init__(self, corpus, open_tag, close_tag):
        self.corpus = open(corpus)
        self.re_open_tag = re.compile(open_tag)
        self.re_close_tag = re.compile(close_tag)

    def getNext(self):
        _buffer = {'id':None, 'text':""}

        while True:
            line = self.corpus.readline()

            if len(line) == 0:
                self.reset()
                return None

            if re.match(self.re_open_tag, line):
                _buffer['id'] = int(re.match(self.re_open_tag, line).groups(1)[0])
                continue

            if re.match(self.re_close_tag, line):
                return _buffer
                break

            _buffer['text'] += line


    def reset(self):
        self.corpus.seek(0)

    def close(self):
        self.corpus.close()
