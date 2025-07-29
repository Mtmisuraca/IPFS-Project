how to use

1. open a cmd window and run:
   ipfs daemon

2. open another cmd window and start the key server:
   python key_server.py

3. open a third cmd window:
   cd to your project folder (cd C:\Users\Thomas\Desktop\Project)

4. login (python login.py)
   (example: thomas / password123)

5. upload a file (python upload.py)
   (example: example.txt)

   this gives you an ipfs hash and creates a .key file

6. download a file (python download.py)
   (example: example.txt, then paste the hash from step 5)

   this gives you example.txt.decrypted

make sure the .key file is there when downloading
only allowed users can decrypt (check policy.json)

requires:
• Python 3 installed
• Flask installed (for the key server)
• IPFS installed and initialized
• Internet access or local IPFS daemon running# IPFS-Project
