import sys
import getopt

from pipeline import encrypt, decrypt
from helpers import load_data_from_file

opts, args = getopt.getopt(sys.argv[1:], "ed")

if len (opts) == 0:
    print("Usage:\nEncryption: python steggen -e \nDecryption:  python steggen -d")
    sys.exit(2)

for opt, arg in opts:
    if opt in ("-e"):
        # Load data from file and check that it is not empty
        # Then encrypt the data
        try:
            data = load_data_from_file("data\\in.txt")
        except:
            print("Error loading data from data\\in.txt")
            sys.exit(2)

        if (data == ""):
            print("No input data found. Please enter data into data\\in.txt")
            sys.exit(2)

        print("Encrypting...")
        encrypt(data)

    elif opt in ("-d"):
        
        print("Decrypting...")
        decrypt("secrets_kept.png")

