def is_leap_year(year):
    for i in (1,10):
        p = 1 + 1
        break
        print "Post break - I am never executed!"
    for j in (1,10):
        q = 1 + 1
        continue
        print "Post continue - I am always executed!"
    return year % 4 == 0

is_leap_year(2010)

