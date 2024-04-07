import csv
import json
from cryptography.fernet import Fernet


def encrypt_token(created_token, created_key):
    cipher_suite = Fernet(created_key)
    ciphered_text = cipher_suite.encrypt(bytes(str(created_token), encoding='utf-8'))
    return ciphered_text


def decrypt_token(ciphered_text, read_key):
    cipher_suite = Fernet(read_key)
    un_cipher_text = (cipher_suite.decrypt(ciphered_text))
    plain_text_encrypted_password = bytes(un_cipher_text).decode("utf-8")  # convert to string
    return plain_text_encrypted_password


def write_serial(serial):
    with open('app_bytes.bin', 'wb') as file_object:  file_object.write(serial)


def read_serial():
    with open('app_bytes.bin', 'rb') as file_object:
        for line in file_object:
            encrypted_pwd = line
        return encrypted_pwd


def write_key(generated):
    with open('keys.csv', 'w+') as f:
        writer = csv.DictWriter(f)
    writer.writeheader()
    writer.writerow({'key': generated})


# TODO test
# key = Fernet.generate_key()
# key = b'pRmgMa8T0INjEAfksaq2aafzoZXEuwKI7wDe4c1F8AY='
# token = "96181431069618143106"
# try:
#     # write serial
#     write_serial(encrypt_token(token, key))
#     # print(read_token())
#     serial = read_serial()
#     # get_key = bytes(str(temp_key), encoding='utf-8')
#     decrypt_token(serial, key)
#
# except Exception as e:
#     print(str(e))


def read_data():
    try:
        with open("user.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def write_data(dic):
    with open("user.json", "w+") as f:
        json.dump(dic, f)


json_lines = {}


def reset_data():
    with open("user.json", 'w+') as open_file:
        #open_file.writelines('\n'.join(json_lines))
        json.dump(json_lines, open_file)



# dictionary = {
#     "user": "9618143113",
#     "pass": "968143113",
#     "url": "https://google.com",
#
# }
#
# write_data(dictionary)
# print(read_data())
# reset_data()
# print("----")
# print(read_data())
# print("----")
# result = read_data()
# print(result.get('user'))
# print(result.get('url'))
