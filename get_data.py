import serial
import time
import csv

ser = serial.Serial("COM4", timeout=1)
ser.baudrate = 115200
ser.dtr = False
ser.rts = False

datas = []
acce = []
gyro = []


def remove_symb(el):
    return el[:4]


def clean_data(data_list):
    data_list[-1] = remove_symb(data_list[-1])
    return [float(el) for el in data_list]


def write_file(filename, data_lists):
    headers = ["acce_x", "acce_y", "acce_z", "gyro_x", "gyro_y", "gyro_z"]
    with open(filename, "w", newline="", encoding="utf8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(data_lists)


def get_data(sec):
    cnt = 60
    end_time = time.time() + sec
    line = ""
    while time.time() < end_time:
        if cnt > 0:
            ser.readline()
            cnt -= 1
        else:
            line = str(ser.readline()).strip().split()[-4:]
            cleaned = []
            if line != ["b'\\x1b[0m\\r\\n'"] and line[0] == "acce":
                cleaned = clean_data(line[1:])
                acce.append(cleaned)
            elif line != ["b'\\x1b[0m\\r\\n'"] and line[0] == "gyro":
                cleaned = clean_data(line[1:])
                gyro.append(cleaned)
    return


def combine_list(list1, list2):
    big_list = []
    len_2 = len(list2)
    for i, mini_list in enumerate(list1):
        if i >= len_2:
            break
        mini_list.extend(list2[i])
        big_list.append(mini_list)
    return big_list


get_data(5)
datas = combine_list(acce, gyro)
write_file("data/down_20.csv", datas)
