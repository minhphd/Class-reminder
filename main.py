import datetime as dt
import pandas as pd
from win10toast import ToastNotifier
import curses

def subtract_time(t1, t2):
    date = dt.date(1,1,1)
    dt1 = dt.datetime.combine(date, t1)
    dt2 = dt.datetime.combine(date, t2)
    return dt2 - dt1


def t_to_s(t):
    return t.hour * 3600 + t.minute * 60 + t.second


schedule = pd.read_excel('./Class-reminder/datas/schedule.xlsx')
desc = pd.read_excel('./Class-reminder/datas/courses_desc.xlsx')
today_sche = schedule[["start_time", dt.datetime.now().weekday()]]

# use ( dt.datetime.now().time() ) to get current time

state = {
    "status": "",
    "noftified": False,
}


def draw(terminal):
    
    def get_center_pos(title, width, height):
        x = width//2 - (len(title)//2)
        y = height//2
        return int(x), int(y)
    
    Running = True
    t_now = dt.datetime.now().time()
    toast = ToastNotifier()
    # class_duration = 60*40
    break_duration = 600
    t_prev = dt.time(0,0,0)
    height, width = 11, 60
    
    for i in range(8):
        t_next = today_sche.iloc[i, 0]
        if t_prev <= t_now < t_next:
            break
        t_prev = t_next
    else:
        state["status"] = "school already ended"
    
    terminal.clear()
    terminal.refresh()

    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)

    while Running:
        t_now = dt.datetime.now().time()
        s_now = t_to_s(t_now)
        t_next = today_sche.iloc[i, 0]
        s_next = t_to_s(t_next)
        class_next = today_sche.iloc[i, 1]

        # Initialization
        terminal.clear()
        curses.resize_term(height, width)
        terminal.border(0)

        # check if final class
        if pd.isnull(class_next):
            string = "no more classes, press 'q' to exit program"
            x, y = get_center_pos(string, width, height)
            terminal.addstr(y, x, string)
            if terminal.getch() == ord('q'):
                break

        # Declaration of string
        title = "Online classes reminder Version 1.0"[:width - 1]
        subtitle = "by Minh Pham Dinh"[:width - 1]
        time = t_now.strftime("%H:%M:%S")[:width - 1]
        next = "[*] Next class:"[:width - 1]
        Teacher = "[*] Teacher:"[:width - 1]
        ID = "[*] ID:"[:width - 1]
        Pass = "[*] Pass:"[:width - 1]
        ETA = "[*] Time till class:"[:width - 1]
        status = "[*] Status:"[:width - 1]

        terminal.addstr(0, get_center_pos(title, width, height)[0], title)
        terminal.addstr(height-1, get_center_pos(subtitle, width, height)[0], subtitle)
        
        # add clock at the middle
        cent_x = get_center_pos(str(time), width, height)[0]
        terminal.attron(curses.color_pair(1))
        terminal.attron(curses.A_STANDOUT)

        terminal.addstr(1, cent_x, time)
        
        terminal.attroff(curses.color_pair(1))
        terminal.attroff(curses.A_STANDOUT)

        # check for state
        if s_now < s_next - break_duration:
            state["status"] = "in class"
        elif s_now < s_next - break_duration/2:
            state["status"] = "break time"
            state["noftified"] = False
        elif s_now < s_next:
            state["status"] = "5 mins till next class"
        else:
            i += 1

        data = desc[desc["CODE"] == class_next]
        class_name = data["NAME"].values[0]
        teacher_name = data["TEACHER"].values[0]
        ID_str = str(data["ID"].values[0])
        Pass_str = str(data["PASS"].values[0])
        eta_str = str(subtract_time(t_now, t_next))[:7][:width -1]

        #add remaining strings
        terminal.addstr(3, 2, next)
        terminal.addstr(4, 2, Teacher)
        terminal.addstr(5, 2, ID)
        terminal.addstr(6, 2, Pass)
        terminal.addstr(7, 2, ETA)
        terminal.addstr(8, 2, status)

        #add remaining datas
        terminal.addstr(3, cent_x, class_name)
        terminal.addstr(4, cent_x, teacher_name)
        terminal.addstr(5, cent_x, ID_str)
        terminal.addstr(6, cent_x, Pass_str)
        terminal.addstr(7, cent_x, eta_str)
        terminal.addstr(8, cent_x, state["status"][:width-1])

        if state["status"] == "5 mins till next class" and not state["noftified"]:
            toast.show_toast("Class reminder",'noftified',duration=10)
            state["noftified"] = True

        terminal.move(0,0)
        terminal.refresh()

if __name__ == "__main__":
    curses.wrapper(draw)