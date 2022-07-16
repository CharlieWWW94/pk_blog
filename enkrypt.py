import rsa
from cryptography.fernet import Fernet

class BlogEncryptor(Fernet):
    '''
    Extension of the Fernet class. Allows creation or submission of key on initialisation.
    Also provides get_key function for accessing AES key and decoding.
    
    '''

    def __init__(self, given_key=None):
        
        if not given_key:
            self.key = Fernet.generate_key()
        else:
            self.key = given_key
        super().__init__(self.key)
    
    def encrypt(self, data):
        return super().encrypt(data.encode('UTF-8'))
    
    def decrypt(self, token):
        return super().decrypt(token).decode('UTF-8')
    
    def get_key(self):
        return self.key

    



class KeyEncryptor:
    '''
    Provides assymetric encryption,  decryption and key generation functions for use with AES key.
    No initialisation processes/constructors needed as only serves to manipulate data.

    '''
    
    def gen_pk_keys(self):
        (self.pub_key, priv_key) = rsa.newkeys(512)
        return [priv_key, self.pub_key]
    
    def encrypt_key(self, key):
        #encoded_key = key.encode('utf8')
        crypto_key = rsa.encrypt(key, self.pub_key)
        return crypto_key
    
    def decrypt_key(self, blog, private_key):
        
        try:
            decrypted_key = rsa.decrypt(blog, private_key)
        except:
            return 'Key decryption failed. Perhaps you are using the wrong RSA key?'
        
        decoded_key = decrypted_key.decode('utf8')
        return decoded_key

#tester code

blog = 'Welcome to the jungle'
blog_encrypt = BlogEncryptor()
encrypted_blog = blog_encrypt.encrypt(blog)
print(f'encrypted_blog: {encrypted_blog}')
blog_key = blog_encrypt.get_key()

pk_encryption = KeyEncryptor()
pk_keys = pk_encryption.gen_pk_keys()
encrypted_aes_key = pk_encryption.encrypt_key(blog_key)
print(f'encrypted_key: {encrypted_aes_key}')

decrypted_key = pk_encryption.decrypt_key(encrypted_aes_key, pk_keys[0])
print(f'decrypted key:{decrypted_key}')

print(BlogEncryptor(decrypted_key).decrypt(encrypted_blog))



