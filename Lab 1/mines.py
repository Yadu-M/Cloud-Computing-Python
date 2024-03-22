from hashlib import sha256
import random
from map import mine_check
from threading import Thread, Event, current_thread, Lock


dig_lock = Lock()  # Create a lock for synchronization

def disarm_mine(row: int, col: int, mine_list: list):
    print(f' attempting to disarm mine at ({row - 1}, {int(col/2)})')
    stop_event = Event()

    def run_disarm():
        for mine_info in mine_list:
            if stop_event.is_set():
                return

            mine_info = mine_info.split()
            if row == int(mine_info[0]) and col == int(mine_info[1]):
                solved = False
                i = 0
                while not solved:
                    serial_num = str(mine_info[2] + f'{i}')
                    hashed_data = sha256(serial_num.encode()).hexdigest()
                    if hashed_data[0:6] == '000000':
                        solved = True
                        with dig_lock:  # Acquire the lock
                            print(f'Disarmed mine at ({row - 1}, {int(col/2)}) \nHash: {hashed_data}\nSerial Num: {serial_num}'
                                  f', Pin: {i}, Temp Mine Key: {i}{serial_num}')
                            print(f'Thread info: {current_thread().name}')
                            stop_event.set()  # Set stop_event here
                        return

                    i += 1

    threads = []
    for _ in range(3):
        t = Thread(target=run_disarm)
        threads.append(t)
        t.start()

    stop_event.wait()  # Wait for any thread to set the stop_event

    for t in threads:
        t.join()
    
    


def get_mines_location(row, col):
    location_list = []
    for i in range(row):
        for j in range(col):
            if mine_check(i + 1, j * 2):
                # print(j * 2)
                location_list.append((i + 1, j * 2))
            # if f.read(1) == "1":
            #     location_list.append((i, j))

    return location_list


def generate_mines_txt(row, col):
    mine_info_list = []
    mine_list = get_mines_location(row, col)
    f = open("mines.txt", "w")
    serial_num_list = random.sample(range(1000, 10000), len(mine_list))

    for row, col in mine_list:
        serial_num = serial_num_list.pop()
        f.write(f'{row - 1} {int(col/2)} {serial_num}\n')
        mine_info_list.append(f'{row} {col} {serial_num}')

    f.close()

    return mine_info_list
