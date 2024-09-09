from decimal import Decimal, getcontext

PRECISION = 10

def decimal_add(a,b):
    getcontext().prec = PRECISION
    res = Decimal(a) + Decimal(b)
    return float(res)

def decimal_sub(a,b):
    getcontext().prec = PRECISION
    res = Decimal(a) - Decimal(b)
    return float(res)

def decimal_mult(a,b):
    getcontext().prec = PRECISION
    res = Decimal(a) - Decimal(b)
    return float(res)

def decimal_divide(a,b):
    getcontext().prec = PRECISION
    res = Decimal(a) / Decimal(b)
    return float(res)

