def run():
    print("available modes:")
    print("    help                             print this output")
    print("    daily-login-date                 print the absolute time of the first tracked time")
    print("    daily-login-since                print the relative time of the first tracked time")
    print("    week-single [large|normal]       print the statistic of the current week")
    print("        large                            print start date, end date, days, hours, minutes")
    print("        normal (default)                 print days, hours, minutes")
    print("    week-table                       print the statistic of the current week in table layout")
    print("    month-table                      print the statistic of the current month in table layout")
    print("    last-weeks-table weeks           print the statistic of the last given week in table layout")