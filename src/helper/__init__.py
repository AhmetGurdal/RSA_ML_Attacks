class Helper:
    # r == 0 -> returns nearest even
    # r == 1 -> returns nearest odd
    @staticmethod
    def roundodd(f,r):
        rf = round(f)
        if(rf % 2 == r):
            return rf
        else:
            if(rf - f > 0):
                return rf - 1
            else:
                return rf + 1
            
    @staticmethod
    def matrixSizes(size):
        x = size
        y = 1
        if((x ** 0.5).is_integer()):
            x = int(x ** 0.5)
            y = x
        else :
            x = int((x / 2) ** 0.5)
            y = int(size / x)
        return x,y