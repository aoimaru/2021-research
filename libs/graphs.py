


class Graph(object):
    @staticmethod
    def toContent(contents):
        res = []
        if not contents:
            return []
        first = contents.pop(0)
        for content in contents:
            first.reverse()
            first = first + content
            res.append(first)
            first = content
        return res

    @staticmethod
    def toContentAfter(contents):
        res = []
        if not contents:
            return []
        contents.reverse()
        first = contents.pop(0)
        for content in contents:
            first.reverse()
            first = first + content
            res.append(first)
            first = content
        return res


