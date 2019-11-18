import base64
import hashlib
import hmac
import time
import datetime
import random as _random
from helpers.director.kv import get_value,set_value
def valide_google_code(code):
    secret = get_value('google_validate_code')
    if not secret:
        secret = random_base32()
        set_value('google_validate_code',secret)
    return generate_otp(secret) == code


'''
如何使用：
客户端使用：
首先使用random_base32函数生成一个随机密钥，然后把这个密钥带入到（otpauth://totp/账号?secret=密钥）这个URI中，账号可以随便填写，然后使用二维码生成器生成二维码，使用谷歌身份验证器软件扫描。
服务端使用：
把上面生成的密钥传入generate_otp函数，可计算出当前动态密码。

'''
def byte_secret(secret):
    missing_padding = len(secret) % 8
    if missing_padding != 0:
        secret += '=' * (8 - missing_padding)
    return base64.b32decode(secret, casefold=True)

def int_to_bytestring(i, padding=8):
    result = bytearray()
    while i != 0:
        result.append(i & 0xFF)
        i >>= 8
    return bytes(bytearray(reversed(result)).rjust(padding, b'\0'))

#根据约定的密钥计算当前动态密码
def generate_otp(secret):
    for_time = datetime.datetime.now()
    i = time.mktime(for_time.timetuple())
    input =  int(i / 30)
    digest = hashlib.sha1
    digits = 6
    if input < 0:
        raise ValueError('input must be positive integer')
    hasher = hmac.new(byte_secret(secret),int_to_bytestring(input),digest)
    hmac_hash = bytearray(hasher.digest())
    offset = hmac_hash[-1] & 0xf
    code = ((hmac_hash[offset] & 0x7f) << 24 |
            (hmac_hash[offset + 1] & 0xff) << 16 |
            (hmac_hash[offset + 2] & 0xff) << 8 |
            (hmac_hash[offset + 3] & 0xff))
    str_code = str(code % 10 ** digits)
    while len(str_code) < digits:
        str_code = '0' + str_code
    return str_code

#随机生成一个base32密钥
def random_base32(length=16, random=_random.SystemRandom(),
                  chars=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ234567')):
    return ''.join(
        random.choice(chars)
        for _ in range(length)
    )