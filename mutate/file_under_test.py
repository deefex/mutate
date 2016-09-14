def is_leap_year(year):
    if (year < 3000) and (year > 1000):     # Test conditional with comparator and logical
        month = 0
        num1 = 5
        num2 = 2
        res = num1 + num2                   # Test arithmetic operator +
        res = num1 - num2                   # Test arithmetic operator -
        res = num1 * num2                   # Test arithmetic operator *
        res = num1 / num2                   # Test arithmetic operator /
        res = num1 % num2                   # Test arithmetic operator %
        res = num1 ^ num2                   # Test arithmetic operator ^
        bool_res = num1 or num2             # Test boolean operator or
        bool_res = num1 and num2            # Test boolean operator and
        +num1                               # Test unary operator +
        -num1                               # Test unary operator -
        +year + 1                           # Test unary and arithmetic - TODO possible unary problem
        -year - 1                           # Test unary and arithmetic - TODO possible unary problem
        print 'String ' + 'concatenation'   # Test arithmetic operator not mutated for string concatenation
        print 'String repetition' * 2       # Test arithmetic operator not mutated for string replication
        print 'String with %s' % 'extra'    # Test arithmetic operator not mutated for string substitution
        for i in (1, 10):
            continue
        return year % 4 == 0
    elif (year > 3000) and (year < 1000):
        return True
    else:
        return False


def explore_return_values():
    # This won't make sense but it's just to view the AST
    myboolean = False
    mynumber = 3
    mystring = 'woohoo'
    mylist = ('number', 'one')
    mydict = {'first': 'number one', 'second': 'number_two'}
    for i in (1, 10):
        break
    if True:
        return myboolean
    if True:
        return False
    if True:
        return mynumber
    if True:
        return 3
    if True:
        return mystring
    if True:
        return 'woohoo'
    if True:
        return None
    if True:
        return mylist
    if True:
        return 'number', 'one'
    if True:
        return mydict
    if True:
        return {'first': 'number one', 'second': 'number_two'}

is_leap_year(2010)
