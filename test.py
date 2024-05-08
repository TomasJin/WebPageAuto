import login_gmail_selenium.util as LGS_util
import login_gmail_selenium.common as LGS_common
import time
import os
from login_upwork import LoginUpwork
import json
import threading
import shutil

def data_load(i):
    with open(str(i)+'//data.json') as file:
        data = json.load(file)
    return data

def main_func(num, option):
    data = data_load(num)
    option = option
    # shutil.rmtree(LGS_common.constant.TEMP_FOLDER)
    if option == 1:
        # No proxy
        profile = LGS_util.profile.ChromeProfile(str(num),
                                                 data['First_Name'],
                                                 'backup',
                                                 )
    elif option == 2:
        # For private proxy
        proxy_folder = os.path.join(LGS_common.constant.PROXY_FOLDER, f'proxy_auth')
        profile = LGS_util.profile.ChromeProfile(str(num),
                                                 data['First_Name'],
                                                 'backup',
                                                 'public',
                                                 None,
                                                 '168.119.3.245:27017',
                                                 'http',
                                                 proxy_folder)
    else:
        # For public proxy
        profile = None


    driver = profile.retrieve_driver()
    time.sleep(1)
    driver.set_window_size(500, 360);
    login_upwork = LoginUpwork(driver, num)
    login_upwork.start()

if __name__ == '__main__':
    threads = []
    for i in range(1, 2):
        thread = threading.Thread(target=main_func, args=(str(i), 1))
        threads.append(thread)
        thread.start()
        time.sleep(60)

    for thread in threads:
        thread.join()
