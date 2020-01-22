class Pixel:
    numbit = 8
    def __init__(self, *args, **kwargs):
        self.bits = []
        for i in range(0, Pixel.numbit):
            self.bits.append(0)
        if kwargs.get('number'):
            number = kwargs.get('number')
            self.bits = self.tobinary(number)
    def tobinary(self, number):
        num = bin(number).split('b')[1]
        while (len(num) < 8):
            num = '0' + num
        num = list(num)
        for i in range(0, Pixel.numbit):
            num[i] = int(num[i])
        return num
    def tonumber(self):
        set = []
        numb = 0
        for i in range(Pixel.numbit-1, -1, -1):
            set.append(2 ** i)
        for bit, i in zip(self.bits, set):
            numb += bit*i
        return numb
    @staticmethod
    def xor(p1, p2):
        tmp = []
        for bit1, bit2 in zip(p1.bits, p2.bits):
            tmp.append(bit1^bit2)
        return tmp
    @staticmethod
    def isequal(a, b):
        if a.tonumber == 6:
            print(a)
        if a.bits == b.bits:
            return True
        else:
            return False
    @staticmethod
    def isinlist(p, lst):
        for pixel in lst:
            if Pixel.isequal(p, pixel):
                return True
        return False
    @staticmethod
    def indexinlist(p, lst):
        for pixel in lst:
            if Pixel.isequal(p, pixel):
                return lst.index(pixel)
        return False

class ECA42attractores:
    def __init__(self):
        self.attractores = []
        self.create()
    def __isinAttces(self, p):
        for attractor in self.attractores:
            if Pixel.isinlist(p, attractor):
                return True
        return False
    def create(self):
        for i in range(0, 2 ** Pixel.numbit - 1):
            p = Pixel(number=i)
            if self.__isinAttces(p):
                pass
            else:
                tmpstates = []
                gene = ECARule42(p)
                while(not Pixel.isinlist(p, tmpstates)):
                    tmpstates.append(p)
                    p = gene.nextstat()
                index = Pixel.indexinlist(p, tmpstates)
                if not self.__isinAttces(p):
                    self.attractores.append(tmpstates[index:])


class ECARule42:
    def __init__(self, initpixel):
        self.current = initpixel
    def nextstat(self):
        tmp = Pixel()
        for i in range(0, Pixel.numbit):
            q = self.current.bits[i]
            if i == 0:
                p = self.current.bits[Pixel.numbit-1]
                r = self.current.bits[i + 1]
            elif i == Pixel.numbit - 1:
                r = self.current.bits[0]
                p = self.current.bits[i - 1]
            else:
                p = self.current.bits[i - 1]
                r = self.current.bits[i + 1]

            tmp.bits[i] = ((1 + p * q) * r) % 2
        self.current = tmp
        return tmp
