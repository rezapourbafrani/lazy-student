import json

import requests

import App_gui
import threading
import saveData
import attendSession
from types import SimpleNamespace
from cryptography.fernet import Fernet

# ---------------------        init --------------------

driver = ""
driver_address = ""
url = "https://el.ardakan.ac.ir/login/index.php"
apiUrl = "https://suamto1.pythonanywhere.com/"
clock_webservice_address = "https://api.codebazan.ir/time-date/?td=time"
insert_data_url = "save_detail?"
###########################################################

# --------------------- api --------------------

api_url = 'https://sumato1.pythonanywhere.com/'
token = '56ef53606d18d178606abbeb361ee5d506fb3dc3'
parameter_interducer_code = 'interducer_code'
# introducer code
parameter_phone_number = 'phone_number'
parameter_key = 'key'
parameter_username = 'username'
parameter_password = 'password'
parameter_url = 'url'

api_key_validate = 'key_validate'
api_save_customer_details = 'save_details'
api_phone_validate = 'phone_validate'
api_inderducer_code_validate = 'interducer_validate'
###########################################################

"""
         insert    check mobile and save   (mob,user,pass,key,url)    and create serial by mob+user
         run       check json data         decode serial and compare username 
         shit
         commit

"""


# ------------------------------------------------- Verify
class Verify:
    def __init__(self, mob, user, password, site_url):
        global phone_validate_response
        self.mobile = mob
        self.user = user
        self.password = password
        self.url = site_url
        self.result_code = -1

        # TODO reza web api
        try:
            phone_validate_response = requests.get(api_url + api_phone_validate,
                                                   headers={'Authorization': 'Token ' + token},
                                                   params={parameter_phone_number: self.mobile})
        except Exception as e:
            print(str(e))
            self.result_code = 0

        # web api check
        try:
            # TODO phone validate
            obj = json.loads(phone_validate_response.text, object_hook=lambda d: SimpleNamespace(**d))
            check_value = obj.result_code
        except Exception:
            print("phone not validate")
            self.result_code = 0
            check_value = 0
        # print('check value :' + str(check_value))
        try:
            # create key and save data
            if check_value == 1:
                self.user_key = Fernet.generate_key()  # key = b'pRmgMa8T0INjEAfksaq2aafzoZXEuwKI7wDe4c1F8AY='
                check_serial = self.mobile + "-" + self.user  # token = "09167534689-9828153553"
                # json
                user_data = {'mob': self.mobile, 'user': self.user, 'pass': self.password, 'url': self.url,
                             'key': self.user_key.decode('utf-8')}
                json_data = json.dumps(user_data)
                # print(user_data)
                # just store
                # TODO save user details
                save_details_response = requests.post(api_url + api_save_customer_details,
                                                      headers={'Authorization': 'Token ' + token},
                                                      json={parameter_phone_number: self.mobile,
                                                            parameter_key: self.user_key.decode('utf-8'),
                                                            parameter_url: self.url,
                                                            parameter_username: self.user,
                                                            parameter_password: self.password})

                # write serial  first time
                detail_obj = json.loads(save_details_response.text, object_hook=lambda d: SimpleNamespace(**d))
                # print(detail_obj)
                # print(detail_obj.result_code)
                detail_obj.result_code = 1
                self.result_code = 1

                if detail_obj.result_code == 1:
                    self.result_code = 1
                    try:
                        saveData.read_data()
                        # print(saveData.read_data())
                        # key is created !
                        print('key is already created')
                        self.result_code = 0

                    except Exception:
                        # print('good json file is empty')
                        saveData.write_serial(saveData.encrypt_token(check_serial, self.user_key))
                        saveData.write_data(user_data)
                        self.result_code = 1
                        print('details save is done')
            else:
                print('phone not valid')
                self.result_code = 2
        except Exception as e:
            print('in verify ' + str(e))

    def get_result_code(self):
        return self.result_code

    @staticmethod
    def check_mobile():
        try:
            serial = saveData.read_serial()
            user_data = saveData.read_data()
            # user data
            mobile = user_data.get("mob")
            username = user_data.get("user")
            user_key = user_data.get("key")
            # key
            get_key = bytes(user_key, encoding='utf-8')
            # print(" check mobile user : {} mob : {} key : {}".format(username, str(mobile), str(get_key)))
            created_token = saveData.decrypt_token(serial, get_key)
            print("Now check token ->->")
            # print(created_token)
            # print(mobile + "-" + username)
            # login in class
            if created_token == mobile + "-" + username:
                print("Your serial number is valid ^_^ ")
                print("--------------------------------")
                return 1
            # fuck you :) serial isn't for you bitch
            else:
                print("Your serial number is not valid :-( ")
                print("------------------------------------ ")
                return 2
        except Exception as e:
            # don't login
            print(str(e))
            print("Check serial failed")
        return 0


class App:
    def __init__(self):
        gui_thread = threading.Thread(target=create_gui)
        gui_thread.start()


def create_gui():
    App_gui.Gui()


if __name__ == '__main__':
    print("App started->->")
    print("---- Class Robot ----")
    print(requests.get(clock_webservice_address).text[:5])
    App()
