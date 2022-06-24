'''what if the data is not a string but an int'''
import hashlib
import json

def crypto_hash(*args):
    '''
    Return a sha-256 hash of the given arguments.
    '''
    stringified_args = sorted(map(lambda data: json.dumps(data), args))
    # use sorted to make sure the order will not change the hash_index
    joined_data = ''.join(stringified_args)
    return hashlib.sha256(joined_data.encode('utf-8')).hexdigest() # utf-8 byte string --> get a 64 character length hexadecimal string

#debug
def main():
    print(f"crypto_hash('one', 2, [3]): {crypto_hash('one', 2, [3])}")
    print(f"crypto_hash(2, 'one', [3]): {crypto_hash(2, 'one', [3])}")
 
# if check, to see if the name value is main.
if __name__ == '__main__':
    main()

