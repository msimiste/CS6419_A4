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

import binascii
import struct
import os


def getOffsets(sourceFile):
    f = open(sourceFile,'rb')
    
    magic = f.read(2).decode()
    size, = struct.unpack('I',f.read(4))
    reserved1, =  struct.unpack('H', f.read(2))
    reserved2, =  struct.unpack('H', f.read(2))
    offset, = struct.unpack('I',f.read(4))
    f.close()   
    return (magic,size,offset)
    
    #***Extra information about bmp file taken from header****#
    
    #print('Offset: {} '.format(offset))
    #print('Reserved 1: %s' % struct.unpack('H', f.read(2)))
    #print('Reserved 2: %s' % struct.unpack('H', f.read(2)))
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
    
def convertMessageToBinaryString(message):
    tmp = ''.join(format(ord(i), '08b') for i in message)
    return tmp
    
def convertBinaryStringToMessage(tmp):
    listOfChars = [tmp[i:i+8] for i in range(0,len(tmp),8)]
    outMsg = ''.join(chr(int(i,2)) for i in listOfChars)
    return outMsg

def getBytesToWrite(source,offset,message,delimiter):
    f = open(source,'rb')
    f.seek(offset)
    byteArray = bytearray(b'')
    
    for i in range(0,len(message)):        
        byte = f.read(1)
        intVersion = int.from_bytes(byte,sys.byteorder)
                
        if intVersion % 2 == int(message[i]):
            byteArray.extend(byte)
        else:
            tempByte = (intVersion+1).to_bytes(1,sys.byteorder)
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
    
def checkForDelimiter(source,delimiter):
    f = open(source,'rb')
    data = f.read()
    f.close()
    msgIsHidden = delimiter in data    
    return msgIsHidden
    
    
def getDelimiterIndex(source,delimiter):
    f = open(source,'rb')
    data = f.read()
    return data.index(delimiter)

def getEmbeddedBinaryString(source,offset,index):
    f = open(source,'rb')
    f.seek(offset)
    msgBytes = f.read(index-offset)
    binaryList = [0 if x%2 == 0 else 1 for x in msgBytes]
    binaryString = ''.join(str(a) for a in binaryList)
    msg = convertBinaryStringToMessage(binaryString)
    return msg

def main(args):
    delimiter=bytes("#$#$#$#$",'utf-8')
    command = args[1]
    sourceFile = args[2]
    magic,size,offset  = getOffsets(sourceFile)    
    
    if(command == 'h'.lower()):
        message = args[3]
        binaryString = convertMessageToBinaryString(message)
        convertBinaryStringToMessage(binaryString)
        outFile,extension = os.path.splitext(sourceFile)
        outFile = outFile + "_embedded" + extension
        stegoBytes = getBytesToWrite(sourceFile,offset,binaryString,delimiter)
        embedBytes(sourceFile,stegoBytes,offset,outFile)
        print("Your Message has been embedded within: {}".format(outFile))
    
        
    elif(command == 'e'.lower()):
        containsMessage = checkForDelimiter(sourceFile, delimiter)
        index = getDelimiterIndex(sourceFile,delimiter)
        if(containsMessage):
            msg = getEmbeddedBinaryString(sourceFile,offset,index)
            print("The embedded message is: {}".format(msg))
            
     
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
