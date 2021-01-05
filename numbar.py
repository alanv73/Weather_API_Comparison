# Print bar chart of a number
def printNumBar(value, total, decimals=1, length=100, fill='█', bar_label=None, print_output=True):
    """
    @params:
        value   - Required  : value of bar
        total       - Required  : Max value possible
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    try:
        percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                         (value / float(total)))
    except ZeroDivisionError:
        percent = 0

    try:
        filledLength = int(length * value // total)
    except ZeroDivisionError:
        filledLength = 0

    bar = fill * filledLength
    if (print_output):
        print('%s %s' % (bar, value if bar_label is None else bar_label))
    else:
        return '%s %s' % (bar, value if bar_label is None else bar_label)


if __name__ == '__main__':
    printNumBar(44.3, 88, length=20)
    printNumBar(22, 88, length=20)
    printNumBar(68, 88, length=20)
    printNumBar(88, 88, length=20)
