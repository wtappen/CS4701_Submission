from datetime import datetime
from pathlib import Path

log_file = ''
log_dir = Path('./logs')
log_path = ''
csv_path = ''


def right_now():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")


def right_now_fname():
    now = datetime.now()
    return now.strftime("%d_%m_%Y_%H_%M_%S")


def separator():
    return '\n\n' + '_'*80 + '\n\n'


def set_path_logger(s):
    global log_path
    global csv_path
    log_path = Path(s + right_now_fname() + '.txt')
    csv_path = Path(s + right_now_fname() + '.csv')


def set_logger(s):
    global log_file
    global log_path
    global csv_path
    log_file = s
    log_path = log_dir / (s + '.txt')
    csv_path = log_dir / (s + '.csv')


def log(s):

    if log_path == '':
        print('\nPlease set the log file.')
        quit()

    f = open(log_path, 'a+')
    f.write(right_now() + ' |\t' + str(s) + '\n')
    print(s)
    f.close


def list_to_sep_str(lst):
    return ",".join([str(x) for x in lst]) + '\n'


def log_csv(lst):

    if csv_path == '':
        print('\nPlease set the log file.')
        quit()

    f = open(csv_path, 'a+')
    f.write(list_to_sep_str(lst))
    f.close
