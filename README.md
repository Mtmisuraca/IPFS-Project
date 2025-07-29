M Thomas Misuraca III
W0562266
CMPS 652 – Advanced Storage Technologies


GitHub Link: https://github.com/Mtmisuraca/IPFS-Project.git

How to Use this


Requirements:
• Python 3 installed
• Flask installed (for the key server)
• IPFS installed and initialized
• Internet access or local IPFS daemon running




1. open a cmd window and start IPFS

run:
ipfs daemon
 
2. open another cmd window, cd to the project folder, and start the key server:

   cd to your project folder (ex: cd C:\Users\Thomas\Desktop\Project)

run:
  	python key_server.py
 
3. open a third cmd window, cd to the project folder, and run the login
   cd to your project folder (ex: cd C:\Users\Thomas\Desktop\Project)
run:
python login.py

  (example: thomas / password123 for admin level access or bob / user456 for user level access)


 

4. upload a file 
run:
python upload.py

enter in the name of a file located locally
   (example: example.txt or testfile.txt)
 
   this gives you an IPFS hash and creates a .key file
Save the IPFS hash for later


5. download a file 
Run:
python download.py
   (example: example.txt or testfile.txt, then paste the hash from step 5)

 
   this gives you example.txt.decrypted


We can now test access control. Lets try to download that as bob, a non-admin (Doesn’t work)

 

and that is reflected in the key server and the key log and the audit log

 

Note:
make sure the .key file is there when downloading
only allowed users can decrypt (check policy.json)

Only admins can upload new files








