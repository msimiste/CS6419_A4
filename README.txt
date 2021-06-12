This program uses LSB steganography in order to hide a text message within a .BMP file or extract a previously hidden message from a .bmp file.
Sample files provided are:
assignment4.bmp
assignment4_embedded.bmp


To hide a message:

$ python3 A4.py h <filename> <message>

example:

$ python3 A4.py h assignment4.bmp 'Digital Forensics Course'


To extract a message:

$ python3 A4.py e <filename>


example:

$ python3 A4.py e assignment4_embedded.bmp
