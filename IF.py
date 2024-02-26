#function to convert from hexadecimal value of length 8 digits to decimal
def hex_to_dec(n):
    st = n[2:10]
    return int(st, 16)

#function to convert any decimal value into hexadecimal string of length 8 digits
def dec_to_hex(n):
    dec = hex(n)
    if len(dec) < 10:
        dec = ('0' * (10 - len(dec))) + dec[2:]
    dec = '0x' + dec[:]
    return dec

#comverts any binary file into required byte addressable instruction memory
def bin_ins(f):
    instructions = []                   #this is a list of dictionaries, each dictionary
                                        #is 32 bits long, indicating one memory location
    n = 4194304 #starting of the instruction memory in decimal
    for x in f.readlines():
        t = {}
        t[dec_to_hex(n)] = x[0:8]
        t[dec_to_hex(n + 1)] = x[8:16]
        t[dec_to_hex(n + 2)] = x[16:24]
        t[dec_to_hex(n + 3)] = x[24:32]
        instructions.append(t)
        n += 4
    
    return instructions

#decide which file to run
prompt = '''Which program do you want to run:
1. Fibonacci Sequence with Odd and Even Numbers
2. Palindrome Checker
3. Prime Number Checker'''

print(prompt)

c = int(input("Choose an option from the above: "))

global binary_instructions

#data is harcoded as it requires input
if c == 1:
    f = open(r".\Dump folder\fib_binary.txt", "r")
    
    binary_instructions = bin_ins(f)
    data = {
        '0x10010000' : '\nEnter a number: ',
        '0x10010012' : ' ',
        '0x10010014' : 'Sequence: ',
        '0x1001001f' : '\nOdd: ',
        '0x10010026' : 'Even: ',
        '0x10010030' : 10,                      #used for mod
        '0x10010034' : 0,                       #x
        '0x10010038' : 1,                       #y
        '0x1001003c' : 0,                       #odd
        '0x10010040' : 0                        #even
    }
elif c == 2:
    f = open(r".\Dump folder\pal_binary.txt", "r")
    
    binary_instructions = bin_ins(f)
    data = {
        '0x10010000' : 'Enter a positive integer to check if it is a plaindrome or not. \n',
        '0x10010042' : 'Number is a palindrome',
        '0x10010059' : 'Number is not a palindrome',
        '0x10010074' : '\n',
        '0x10010078' : 0                       #stores required value
    }
elif c == 3:
    f = open(r".\Dump folder\prime_binary.txt", "r")
    
    binary_instructions = bin_ins(f)
    data = {
        '0x10010000' : 'Enter a number :',
        '0x10010011' : 'NOT PRIME\n',
        '0x1001001c' : 'PRIME\n',
        '0x10010024' : 0                    #stores required value
    }
else:
    print("INVALID OPTION!!")
    quit()
    
#for x in binary_instructions:
#    print(x)