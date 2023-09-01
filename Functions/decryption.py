from cryptography.fernet import Fernet

def decrypt(encryptedString):
    with open("Functions/encryptionKey.txt", "rb") as file:
        key = file.read()
    cipher = Fernet(key)
    return cipher.decrypt(encryptedString).decode("UTF-8")