# -*- coding: utf-8 -*-
import os
import base64
from passlib import totp
from passlib.exc import TokenError, MalformedTokenError
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
from flask import current_app


def _generate_aes_key(salt=None):
    """ Generate a secret key for AES using PBKDF2_SHA265 """

    if not salt:
        salt = os.urandom(16)
    backend = default_backend()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=backend)
    secret_key = current_app.config['SECRET_KEY']
    if isinstance(secret_key, str):
        secret_key = secret_key.encode('utf-8')
    key = kdf.derive(secret_key)
    return salt, key


def _encrypt_key(otp_key):
    """ Encrypt OTP key using AES_CBC_PKCS7. """

    salt, aes_key = _generate_aes_key()
    encryptor = Fernet(key=base64.b64encode(aes_key))
    token = encryptor.encrypt(otp_key)
    return base64.b64encode(salt + token).decode('utf-8')


def _decrypt_key(otp_enckey):
    """ Decrypt OTP encrypted key. """

    ciphertext = base64.b64decode(otp_enckey.encode('utf-8'))
    salt = ciphertext[:16]
    token = ciphertext[16:]
    salt, aes_key = _generate_aes_key(salt=salt)
    encryptor = Fernet(key=base64.b64encode(aes_key))
    return encryptor.decrypt(token=token)


def generate_otp_key():
    """ Generate an OTP key. """

    otp_key = totp.generate_secret()
    otp_key = base64.b32encode(otp_key.encode('utf-8'))
    otp_enckey = _encrypt_key(otp_key=otp_key)
    return otp_enckey


def generate_opt_code(otp_enckey):
    """ Generate an OTP code. """

    otp_key = _decrypt_key(otp_enckey=otp_enckey)
    otp = totp.TOTP(
        key=otp_key,
        issuer=current_app.config['TOTP_ISSUER'],
        digits=current_app.config['TOTP_DIGITS'],
        alg='sha512',
        period=current_app.config['TOTP_PERIOD'])
    return otp.generate()


def validate_opt_code(otp_enckey, otp_code, last_counter):
    """ Validate OTP code. """

    otp_key = _decrypt_key(otp_enckey=otp_enckey)
    otp = totp.TOTP(
        key=otp_key,
        issuer=current_app.config['TOTP_ISSUER'],
        digits=current_app.config['TOTP_DIGITS'],
        alg='sha512',
        period=current_app.config['TOTP_PERIOD'])
    match = None
    try:
        match = otp.match(
            token=otp_code,
            last_counter=last_counter,
            window=current_app.config['TOTP_WINDOW'])
    except (MalformedTokenError, TokenError) as err:
        current_app.logger.warning('Error while validating otp code: %s' % str(err))
    return match


def base64_decodestring(val):
    _str = base64.b64decode(val.encode('utf-8'))
    return str(_str, 'utf-8')


def base64_encodestring(val):
    _str = base64.b64encode(val.encode('utf-8'))
    return str(_str, 'utf-8')
