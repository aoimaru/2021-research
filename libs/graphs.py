


class Graph(object):
    @staticmethod
    def toContent(contents):
        res = []
        first = contents.pop(0)
        for content in contents:
            first.reverse()
            first = first + content
            res.append(first)
            first = content
        return res



