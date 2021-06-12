#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  A4.py
#  
#  Copyright 2021 simdevs <simdevs@simdevs>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import argparse
import binascii
import struct
import os


def getOffsets(sourceFile,message):
    f = open(sourceFile,'rb')
    
    magic = f.read(2).decode()
    size, = struct.unpack('I',f.read(4))
    
    print('Type:', magic)
    print('Size: {}'.format(size))
    print('Reserved 1: %s' % struct.unpack('H', f.read(2)))
    print('Reserved 2: %s' % struct.unpack('H', f.read(2)))
    offset, = struct.unpack('I',f.read(4))
    #print('Offset: {} '.format(offset))
    #print('DIB Header Size: %s' % struct.unpack('I', f.read(4)))
    #print('Width: %s' % struct.unpack('I', f.read(4)))
    #print('Height: %s' % struct.unpack('I', f.read(4)))
    #print('Colour Planes: %s' % struct.unpack('H', f.read(2)))
    #print('Bits per Pixel: %s' % struct.unpack('H', f.read(2)))
    #print('Compression Method: %s' % struct.unpack('I', f.read(4)))
    #print('Raw Image Size: %s' % struct.unpack('I', f.read(4)))
    #print('Horizontal Resolution: %s' % struct.unpack('I', f.read(4)))
    #print('Vertical Resolution: %s' % struct.unpack('I', f.read(4)))
    #print('Number of Colours: %s' % struct.unpack('I', f.read(4)))
    #print('Important Colours: %s' % struct.unpack('I', f.read(4)))
    f.seek(offset)
    #bytes8 = [b for b, in struct.unpack('s',f.read(1)) for r in range(0,8)]
    #for i in range(0,8):
    ##    b, = struct.unpack('c',f.read(1))
    #   print(bin(b))
    
    
        
    #lengthBytes = f.read(16)
    #print(lengthBytes)
    #lengthBits = ''.join(format(c,'08b') for c in lengthBytes)
    #hexTest = [binary2Hex(c) for c in [lengthBits[i:i+8] for i in range(0,len(lengthBits),8)]]
    #print(hexTest)
    #binaryTest = [hex2binary(c) for c in lengthBytes]
    #print(binaryTest)
    #print(test.decode())
    #test1 = ''.join(format(c,'08b') for c in test)
    #print(len(test1)/8)
    #print([test1[i:i+8] for i in range(0,len(test1),8)])
    #test1 = [bin(ord(b.decode())) for b in test]
    #print(test1)
    
    #print(bytes8)
    #byte = struct.unpack('c',f.read(1))
    #print(byte)
    #byte = struct.unpack('c',f.read(1))
    #print(byte)
    #byte = struct.unpack('c',f.read(1))
    #print(byte)
    #byte = struct.unpack('c',f.read(1))
    #print(byte)
    #
    #byte = struct.unpack('c',f.read(1))
    #print(byte)
    
    
    
   
    return (magic,size,offset)
    f.close()
    
    
def convertMessageToBinaryString(message):
    tmp = ''.join(format(ord(i), '08b') for i in message)
    return tmp
    
def convertBinaryStringToMessage(tmp):
    listOfChars = [tmp[i:i+8] for i in range(0,len(tmp),8)]
    outMsg = ''.join(chr(int(i,2)) for i in listOfChars)
    #print("Outmsg: {}".format(outMsg))
    return outMsg

def binary2Hex(byte):
    #[hex(int(c,2)) for c in [byte[i:i+8] for i in range(0,len(byte),8)]]
    return hex(int(byte,2))
    
def hex2binary(byte):
    print(byte)
    print(''.join(format(ord(byte),'08b')))
    #return ''.join(format(bytes(byte),'08b'))
    

#def insertMsgLength(imageBytes, lengthBytes):

#todo, get len of binary string
#store message length 

def getBytesToWrite(source,offset,message,delimiter):
    f = open(source,'rb')
    f.seek(offset)
    byteArray = bytearray(b'')
    
    
    for i in range(0,len(message)):
        
        byte = f.read(1)
        intVersion = int.from_bytes(byte,sys.byteorder)
        #print("here")
        #print("Byte: {}".format(byte)) 
        #print("Intver: {}".format(intVersion))
        #print("Msg I: {}".format(message[i]))
        #print("Mod :{}".format(intVersion %2))
        #print("Same mod: {}".format(intVersion %2 == int(message[i])))
        #print("Byte Convert: {}".format((intVersion+1).to_bytes(1,sys.byteorder)))
        
        if intVersion %2 == int(message[i]):
            byteArray.extend(byte)
            #print(byteArray)
        else:
            tempByte = (intVersion+1).to_bytes(1,sys.byteorder)
            #print(tempByte)
            byteArray.extend(tempByte)
    byteArray.extend(delimiter)
    return byteArray
    
def embedBytes(inSource,stegoBytes,offset,outSource):
    inFile = open(inSource,'rb')
    outFile = open(outSource,'wb')
    chunk1 = inFile.read(offset)
    outFile.write(chunk1)
    outFile.write(stegoBytes)
    inFile.seek(offset+len(stegoBytes))
    chunk2 = inFile.read()
    outFile.write(chunk2)
    inFile.close()
    outFile.close()


def main(args):
    delimiter=bytes("#$#$",'utf-8')
    #print(bytes(delimiter,'utf-8'))
    command = args[1]
    sourceFile = args[2]
    outFile,extension = os.path.splitext(sourceFile)
    print(outFile,extension)
    outFile = outFile + "_embedded" + extension
    if(command == 'e'.lower()):
        message = args[3]
    #print(command in ['e'.lower(),'h'.lower()])
    #print(sourceFile)
    #print(message.encode('ascii'))
    binaryString = convertMessageToBinaryString(message)
    convertBinaryStringToMessage(binaryString)
    magic,size,offset  = getOffsets(sourceFile,binaryString)
    #print("Magic: {0} Size: {1} Offset: {2}".format(magic,size,offset))
    #print("Msg Length: {}".format(format(len(binaryString),'08b')))
    stegoBytes = getBytesToWrite(sourceFile,offset,binaryString,delimiter)
    print(stegoBytes)
    embedBytes(sourceFile,stegoBytes,offset,outFile)
    #t = [hex(s) for s in stegoBytes]
    #print(t)
     
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
