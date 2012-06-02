# Query combinators.
# Follows Jay Conrod's tutorial:
# http://www.jayconrod.com/posts/38/a-simple-interpreter-from-scratch-in-python-part-2


class Result:

    def __init__(self, value, pos):
        self.value = value
        self.pos = pos

    def __repr__(self):
        return 'Result(%s, %d)' % (self.value, self.pos)


class Parser:

    @abstractmethod
    def __call__(self, tokens, pos):
        raise NotImprementedError


class Reserved(Parser):

    def __init__(self, value, tag):
        self.value = value
        self.tag = tag

    def __call__(self, token, pos):
        if pos < len(tokens) and \
        tokens[pos][0] == self.value and \
        tokens[pos][1] is self.tag:
            return Result(tokens[pos][0], pos+1)
        else:
            return None


class Tag(Parser):

    def __init__(self, value, tag):
        self.value = value
        self.tag = tag

    def __call__(self, tokens, pos):
        if pos < len(tokens) and \
        tokens[pos][1] is self.tag:
            return Result(tokens[pos][0], pos+1)
        else:
            return None


class Concat(Parser):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, tokens, pos):
        left = self.left(tokens, pos)
        if left:
            right = self.right(tokens, left.pos)
            if right:
                both = (left.value, right.value)
                return Result(both, right.pos)
        return None


class Alternate(Parser):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, tokens, pos):
        left = self.left(tokens, pos)
        if left:
            return left
        else:
            right = self.right(tokens, pos)
            return right


class Opt(Parser):

    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        if result: return result
        else: return Result(None, pos)


class Rep(Parser):

    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, pos):
        results = []
        result = self.parser(tokens, pos)
        while result:
            results.append(result.value)
            pos = result.pos
            result = self.parser(tokens, pos)
        return Result(results, pos)


class Process(Parser):

    def __init__(self, parser, function):
        self.parser = parser
        self.function = function

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        if result:
            result.value = self.function(result.value)
            return result


class Phrase(Parser):

    def __init__(self, parser, function):
        self.parser = parser

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        if result and result.pos == len(tokens):
            return result
        else: return None
