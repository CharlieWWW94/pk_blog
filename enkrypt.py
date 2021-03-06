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
        return priv_key
    
    def encrypt_key(self, key):
        crypto_key = rsa.encrypt(key, self.pub_key)
        return crypto_key
    
    def decrypt_key(self, encrypted_key, private_key):
        
        try:
            decrypted_key = rsa.decrypt(encrypted_key, private_key)
        except:
            return 'Key decryption failed. Perhaps you are using the wrong RSA key?'
        
        decoded_key = decrypted_key.decode('utf8')
        return decoded_key


'''
  bytes_key = str(dumps(access_key))
        print(bytes_key)
        print(type(bytes_key))
        new_access = loads(eval(bytes_key))
        #print(type(access_key))
        decrypted_key = key_encryption.decrypt_key(encrypted_key, new_access)
        print(f"Here is the decrypted key, as evidence:{decrypted_key}")
        blog_decryptor = BlogEncryptor(decrypted_key)
        print(f"Here is the decrypted blog as evidence: {blog_decryptor.decrypt(new_blog.blog_content)}")

'''