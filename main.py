import curses
from time import localtime, gmtime
import datetime
import pandas as pd
from win10toast import ToastNotifier

schedule = pd.read_excel('./datas/schedule.xlsx')
courses_desc = pd.read_excel('./datas/courses_desc.xlsx')
today_schdl = schedule[["start_time", localtime().tm_wday]]

def t_to_s(t):
    return t.hour * 3600 + t.minute * 60 + t.second

def s_to_t(sec):
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    return f'{h:d}:{m:02d}:{s:02d}'

def draw_menu(terminal):
    k = 0
    i = 0
    prev_s = 0
    next_class = None
    nofti = False
    toast = ToastNotifier()

    def get_center_pos(title, width, height):
        x = width//2 - (len(title)//2)
        y = height//2
        return int(x), int(y)
    
    # get blank canvas
    terminal.clear()
    terminal.refresh()

    # Must be called to use colors in the future
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)

    while k != ord('q'):
        current_t = localtime()
        current_s = current_t.tm_hour * 3600 + current_t.tm_min * 60 + current_t.tm_sec
        next_class_t = datetime.time(23,59,0)

        # Initialization
        terminal.clear()
        curses.resize_term(10, 60)
        height, width = terminal.getmaxyx()
        terminal.border(0)

        # Declaration of string
        title = "Online classes reminder Version 1.0"[:width - 1]
        subtitle = "by Minh Pham Dinh"[:width - 1]
        time = s_to_t(current_s)
        next = "[*] Next class:"[:width - 1]
        Teacher = "[*] Teacher:"[:width - 1]
        ID = "[*] ID:"[:width - 1]
        Pass = "[*] Pass:"[:width - 1]
        ETA = "[*] Time till break:"[:width - 1]

        terminal.addstr(0, get_center_pos(title, width, height)[0], title)
        terminal.addstr(height-1, get_center_pos(subtitle, width, height)[0], subtitle)
        
        # add clock at the middle
        cent_x = get_center_pos(time, width, height)[0]
        terminal.attron(curses.color_pair(1))
        terminal.attron(curses.A_STANDOUT)

        terminal.addstr(1, cent_x, time)
        
        terminal.attroff(curses.color_pair(1))
        terminal.attroff(curses.A_STANDOUT)

        # iterate to the next class
        for i in range(i, 8, 1):
            if prev_s <= current_s < t_to_s(today_schdl.iloc[i, 0]):
                next_class = today_schdl.iloc[i, 1]
                next_class_t = today_schdl.iloc[i, 0]
                break
            prev_s = t_to_s(today_schdl.iloc[i, 0])

        if not pd.isnull(next_class):
            print(pd.isnull(next_class), next_class)
            print(today_schdl)
            if current_s >= t_to_s(next_class_t):
                nofti = False
        
            data = courses_desc[courses_desc["CODE"] == next_class]
            class_name = data["NAME"].values[0]
            teacher_name = data["TEACHER"].values[0]
            ID_str = str(data["ID"].values[0])
            Pass_str = str(data["PASS"].values[0])
            eta_str = s_to_t(t_to_s(next_class_t) - current_s)

            #add remaining strings
            terminal.addstr(3, 2, next)
            terminal.addstr(4, 2, Teacher)
            terminal.addstr(5, 2, ID)
            terminal.addstr(6, 2, Pass)
            terminal.addstr(7, 2, ETA)

            #add remaining datas
            terminal.addstr(3, cent_x, class_name)
            terminal.addstr(4, cent_x, teacher_name)
            terminal.addstr(5, cent_x, ID_str)
            terminal.addstr(6, cent_x, Pass_str)
            terminal.addstr(7, cent_x, eta_str)

            if current_s > t_to_s(today_schdl.iloc[i, 0]) - 600 and not nofti:
                data = courses_desc[courses_desc["CODE"] == next_class]
                toast.show_toast("Class reminder",f'Tiếp theo có tiết { class_name } của giáo viên { teacher_name }. Lấy ID trong terminal',duration=10)
                nofti = True
        
        # stop condition
        if pd.isnull(next_class) or i == 7:
            string = "no more classes, press 'q' to exit program"
            x, y = get_center_pos(string, width, height)
            terminal.addstr(y, x, string)
            k = terminal.getch()

        #ending
        terminal.move(0,0)
        terminal.refresh()

def main():
    curses.wrapper(draw_menu)

main()