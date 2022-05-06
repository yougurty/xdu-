#保序加密调用库函数
#https://github.com/tonyo/pyope
# from pyope.ope import OPE
# random_key = OPE.generate_key()
# cipher = OPE(random_key)
# print(cipher.encrypt(1000))
# print(cipher.encrypt(2000))
# print(cipher.encrypt(3000))
# print(cipher.encrypt(4000))
# assert cipher.encrypt(1000) < cipher.encrypt(2000) < cipher.encrypt(3000)
# assert cipher.decrypt(cipher.encrypt(1337)) == 1337
from pyope.ope import OPE, ValueRange
cipher = OPE(b'long key' * 2, in_range=ValueRange(-100, 100),
                              out_range=ValueRange(0, 9999))
assert 0 < cipher.encrypt(10) < cipher.encrypt(42) < 9999