# Query ast.
# Follows Jay Conrod's tutorial:
# http://www.jayconrod.com/posts/39/a-simple-interpreter-from-scratch-in-python-part-3


class And:

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return 'And(%s, %s)' % (self.left, self.right)

    def eval(self, env):
        pass


class Or:

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return 'Or(%s, %s)' % (self.left, self.right)

    def eval(self, env):
        pass


class Not:

    def __init__(self, term):
        self.term = term

    def __repr__(self):
        return 'Not(%s)' % (self.term)

    def eval(self, env):
        pass


class Like:

    def __init__(self, term):
        self.term = term

    def __repr__(self):
        return 'Like(%s)' % (self.term)

    def eval(self, env):
        pass
