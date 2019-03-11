
class Pipeline:

    def __init__(self, data):
        self.data = data

    def __call__(self, *args, **kwargs):
        return Pipeline(**kwargs)

    def then(self, cb):
        pass

    def filter(self, cb):
        pass
