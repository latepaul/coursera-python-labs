def format(t):

    # break time down into elements
    minutes = t // 600
    seconds = (t % 600) // 10
    tenths = (t % 600) - (seconds * 10)

    #add leading zero for single digit seconds
    secs_str = str(seconds)
    if seconds < 10:
        secs_str = "0"+secs_str

    #rubric says behaviour after ten minutes is programmer's choice
    #my choice is to have it wrap around to 0:00.0
    #easiest way to do this is change minutes to 0
    if minutes > 9:
        minutes = 0

    return str(minutes)+':'+secs_str+'.'+str(tenths)

import sys

if __name__ == "__main__":
    print 'argv[1]=',sys.argv[1]
    print '=',format(int(sys.argv[1]))
else:
    print 'name=',__name__
    print sys.argv[1]