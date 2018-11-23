import hashlib

from django.conf import settings


def set_password(password):
    new_psd = "{}{}".format(password,settings.SECRET_KEY)
    h = hashlib.md5(new_psd.encode("utf-8"))
    return h.hexdigest()


# def verif