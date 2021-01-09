

class tt():
    def __init__(self,
                 size=5):
        self.size = size
        print(size)


    def call(self, training=False):

        x = self.size + 1
        return x

if __name__=='__main__':
    l = [(1, 2, 3, 4, 5, 6) for i in range(5)]
    print(l)