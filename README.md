# Class-reminder
**Only support for Window 10 machines**

A curses-based program that reminds you to join your zoom classes based on your schedule. The program read your class schedule from datas/schedule.xlsx and notify your next class in advance. 

## Feature
- notify of the next class 10 mins in advance
- auto copy to clipboard id and pass of the next class
- live updating time remaining and status of the class in terminal

## Usage
- install all dependencies
```
pip3 install pandas
pip3 install win10toast
pip3 install pyperclip
```
- edit schedule.xlsx by with your class schedule
- run main.py
```
python3 main.py
```

![](https://github.com/minhphd/Class-reminder/blob/main/preview.gif)

## Preview of schedule.xlsx file:
### schedule: 
| start_time | 0   | 1   | 2   | 3  | 4   | 5    |
|------------|-----|-----|-----|----|-----|------|
| 7:30       | L10 | G1  | Sh5 | V4 | N18 | QP2  |
| 8:25       | L10 | L10 | H12 | V4 | H12 | Tin5 |
| 9:20       | L10 | L10 | H12 | S5 | V4  | T1   |
| 10:15      | Đ1  | N18 |     | T1 | V4  | T1   |
| 11:10      | T1  | N18 |     | T1 | Đ1  | CN3  |
| 14:00      |     |     |     |    |     |      |
| 14:50      |     |     |     |    | Td3 |      |
| 15:40      |     |     |     |    | Td3 |      |
| 16:30      |     |     |     |    |     |      |

### desc:
| TEACHER            | NAME              | CODE | ID         | PASS       |
|--------------------|-------------------|------|------------|------------|
| Triệu Lê Quang     | Vật Lý            | L10  | 3141537349 | 994494     |
| Hạ Vũ Anh          | Toán              | T1   | 8258073057 | Covid-19   |
| Khương Thị Thu Cúc | Ngữ Văn           | V4   | 9765088770 | 614989     |
| Nguyễn Mạnh Hà     | Địa Lý            | Đ1   | 6822045197 | 1234567890 |
| Trần Văn Năng      | Giáo dục công dân | G1   | 8856018255 | 123456789  |
| Mai Thành Sơn      | Tiếng Anh         | N18  | 2655252337 | 091089     |
| Nguyễn Văn Quảng   | Công Nghệ         | CN3  | 7361311308 | 002003     |
| Nguyễn Thị Thu Cúc | Hóa Học           | H12  | 5841603699 | Hoahoc11   |
| Huỳnh Thị Ái Tâm   | Sinh Học          | Sh5  | 7174188443 | 66886868   |
| Nguyễn Thu Hương   | Lịch Sử           | S5   | 3054051911 | huong24    |
| Trần Mạnh Hùng     | Thể dục           | Td3  | 5678955431 | 989938     |
| Nguyễn Văn Mạnh    | Quốc Phòng        | QP2  | 9102597428 | thaymanhdz |
| Bùi Tiến Dũng      | Tin Học           | Tin5 | 2066767262 | 123456     |


**Enjoy never forget to join classes again!**