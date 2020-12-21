from time import time
timeStarted = time()

def reportTime():
    elapsed = int(time() - timeStarted)
    secs = elapsed % 60
    mins = elapsed // 60
    hours = elapsed // 3600
    days = elapsed // 86400
    out = ""
    if days:
        out += "{} day{}, ".format(days, "s" if days != 1 else "")
    if hours:
        out += "{} hour{}, ".format(hours, "s" if hours != 1 else "")
    if mins:
        out += "{} minute{}, ".format(mins, "s" if mins != 1 else "")
    out += "{} second{} elapsed.".format(secs, "s" if secs != 1 else "")
    print(out)
