import sys
from IF import binary_instructions, dec_to_hex, data

#increase recursion limit to allow for higher numbers
sys.setrecursionlimit(10 ** 9)

#converts any givne memory dictionary into it's binary code
def convert_to_binary(ins):
    st = ''
    for x in ins.values():
        st += x
    
    return st

#converts binary to decimal number
def bin_to_dec(n): 
    return int('0b' + n, 2)

#instance of our processor
class MIPSProcessor:
    def __init__(self):
        self.registers = { # maps register binary location with the register values
            f"{bin(0)[2:]:0>5}":0,  #$0
            f"{bin(1)[2:]:0>5}":0,  #$at
            f"{bin(2)[2:]:0>5}":0,  #$v0
            f"{bin(3)[2:]:0>5}":0,  #$v1
            f"{bin(4)[2:]:0>5}":0,  #$a0
            f"{bin(5)[2:]:0>5}":0,  #$a1
            f"{bin(6)[2:]:0>5}":0,  #$a2
            f"{bin(7)[2:]:0>5}":0,  #$a3
            f"{bin(8)[2:]:0>5}":0,  #$t0
            f"{bin(9)[2:]:0>5}":0,  #$t1
            f"{bin(10)[2:]:0>5}":0, #$t2
            f"{bin(11)[2:]:0>5}":0, #$t3
            f"{bin(12)[2:]:0>5}":0, #$t4
            f"{bin(13)[2:]:0>5}":0, #$t5
            f"{bin(14)[2:]:0>5}":0, #$t6
            f"{bin(15)[2:]:0>5}":0, #$t7
            f"{bin(16)[2:]:0>5}":0, #$s0
            f"{bin(17)[2:]:0>5}":0, #$s1
            f"{bin(18)[2:]:0>5}":0, #$s2
            f"{bin(19)[2:]:0>5}":0, #$s3
            f"{bin(20)[2:]:0>5}":0, #$s4
            f"{bin(21)[2:]:0>5}":0, #$s5
            f"{bin(22)[2:]:0>5}":0, #$s6
            f"{bin(23)[2:]:0>5}":0, #$s7
            f"{bin(24)[2:]:0>5}":0, #$t8
            f"{bin(25)[2:]:0>5}":0, #$t9
            f"{bin(26)[2:]:0>5}":0, #$k0
            f"{bin(27)[2:]:0>5}":0, #$k1
            f"{bin(28)[2:]:0>5}":0, #$gp
            f"{bin(29)[2:]:0>5}":0, #$sp
            f"{bin(30)[2:]:0>5}":0, #$fp
            f"{bin(31)[2:]:0>5}":0  #$ra
            }
        self.instruction_memory = binary_instructions  # Initialize instruction memory
        self.data_memory = data  # Initialize data memory
        self.pc = 4194304 #Initialize program counter
    
    #define fetch cycle
    def fetch(self):
        for x in self.instruction_memory:
            for m in x:
                if m == dec_to_hex(self.pc):
                    ins = x
                    self.pc += 4
                    return ins
        return 0

#R-Type Instruction
class R(MIPSProcessor):
    def __init__(self, i):
        super().__init__()
        self.rs = str(i[6:11])
        self.rt = str(i[11:16])
        self.rd = str(i[16:21])
        self.shamt = str(i[21:26]) 
        self.funct = str(i[26:])

#I-type Instruction
class I(MIPSProcessor):
    def __init__(self, i):
        super().__init__()
        self.op = i[0:6]
        self.rs = i[6:11]
        self.rt = i[11:16]
        self.imm = i[16:32]

#J-type Instruction
class J(MIPSProcessor):
    def __init__(self, i):
        super().__init__()
        self.op = str(i[0:6])
        self.add = '0000' + str(i[6:]) + '00'
    
#Begin Porcessor Instance  
proc = MIPSProcessor()

#Decode/Execute/Mem Access/WB Function
def decode(mem_loc):
    #print(f'pc: {dec_to_hex(proc.pc - 4)}')
    
    #Convert each memory dictionary to it's binary code
    code = convert_to_binary(mem_loc)
    
    if code == '00000000000000000000000000001100':      #Syscall
        #access previous instruction
        req1 = convert_to_binary(binary_instructions[binary_instructions.index(mem_loc) - 1])
        req = I(req1)
        if req.op == '001001':  #if addu
            if req.imm == '0000000000000101': #if given imm take input
                for key in proc.registers:
                    if req.rt == key:
                        proc.registers[key] = int(input())
            elif req.imm == '0000000000001010': #else exit
                quit()
            else:
                print(f"INAVLID SYSCALL OPERATION at PC: {dec_to_hex(proc.pc - 4)}!")
        elif req.op == '001101': #if ori, print string
            hexKey = dec_to_hex(bin_to_dec(req.imm))
            print(proc.data_memory["0x1001" + hexKey[6:]], end = '')
        elif req.op == '100011': #if addiu, print integer
            print(proc.data_memory['0x1001' + dec_to_hex(bin_to_dec(req.rs) + bin_to_dec(req.imm) - 1)[6:]])
            #print('address: ', '0x1001' + dec_to_hex(bin_to_dec(req.rs) + bin_to_dec(req.imm) - 1)[6:])
        elif req.op == '001000': #if lw, print rs reg value
            print(proc.registers[req.rs], end  = '')
        else:
            print(f"INAVLID SYSCALL OPERATION at PC: {dec_to_hex(proc.pc - 4)}!")
    elif code[0:6] == '000000': #Check for R-type instruction
        code = R(code)
        if code.funct == '100000':  # add
            proc.registers[code.rd] = proc.registers[code.rs] + proc.registers[code.rt]
            
        elif code.funct == '100001':  # addu
            proc.registers[code.rd] = (proc.registers[code.rs] + proc.registers[code.rt]) & 0xFFFFFFFF
            
        elif code.funct == '100010':  # sub
            proc.registers[code.rd] = proc.registers[code.rs] - proc.registers[code.rt]
            
        elif code.funct == '011010':  # div
            if proc.registers[code.rt] != 0:
                quotient = proc.registers[code.rs] // proc.registers[code.rt]  # Integer division
                remainder = proc.registers[code.rs] % proc.registers[code.rt]  # Remainder
                proc.registers['33'] = remainder       #hi   register
                proc.registers['32'] = quotient        #lo register
                
        elif code.funct == '011000':  # mul
            proc.registers['32'] = proc.registers[code.rs] * proc.registers[code.rt] #store multiplied value in LO reg
            '''
            result = f'{bin(proc.registers[code.rs] * proc.registers[code.rt])[2:]:0>32}'
            proc.registers['33'] = int(result[:16], 2)
            proc.registers['32'] = int(result[16:], 2)
            '''
            
        elif code.funct == '101010':  # slt
            proc.registers[code.rd] = int(proc.registers[code.rs] < proc.registers[code.rt])   # If rs < rt, set rd to 1; otherwise, set rd to 0
            
        elif code.funct == '010000':  # mfhi
            proc.registers[code.rd] = proc.registers['33']  # Copy value from HI register to rd
            
        elif code.funct == '010010':  # mflo
            proc.registers[code.rd] = proc.registers['32']  # Copy value from LO register to rd
            
        elif code.funct == '001000':  #jr
            proc.pc = proc.registers['11111']     # Get the target address from the source register (ra)
            
    elif code[0:6] == '000010':     #j
        code = J(code)
        address = bin_to_dec(code.add)      #extract the target address
        proc.pc = address               #set the pc to  the target address

    elif code[0:6] == '000011':                              #jal
        code = J(code)
        address = int(code.add, 2)        # Extract target address
        proc.registers['11111'] = proc.pc  # Save return address to ra
        proc.pc = address                #set the pc to the target address
        
    #Check for I-type instructions
    else:
        code = I(code)
        if code.op=='100011':                          #lw
            imm = int(code.imm,2)
            address = proc.registers[code.rs] + imm
            proc.registers[code.rt] = proc.data_memory[dec_to_hex(address)[2:]]
            
        elif code.op=='101011':                        #sw
            imm = int(code.imm,2)
            address = proc.registers[code.rs] + imm
            proc.data_memory[dec_to_hex(address)[2:]] = proc.registers[code.rt]
            
        elif code.op=='001000':                               #addi
            imm = int(code.imm,2)
            proc.registers[code.rt] = proc.registers[code.rs] + imm
            
        elif code.op=='001101':                                #ori
            imm = int(code.imm,2)
            proc.registers[code.rt] = proc.registers[code.rs] | imm
            
        elif code.op == '001111':                                # lui
            imm = int(code.imm, 2)
            proc.registers[code.rt] = imm << 16
            
        elif code.op == '001001':  # addiu
            if code.imm[0] == 1:
                imm = int(code.imm[1:], 2) - (2 ** 15)
            else:
                imm = int(code.imm, 2)
            proc.registers[code.rt] = (proc.registers[code.rs] + imm) & 0xFFFFFFFF
            
        elif code.op == '000100':  # beq
            rs = int(code.rs, 2)
            rt = int(code.rt, 2)
            imm = int(code.imm, 2)
            if proc.registers[code.rs] == proc.registers[code.rt]:      # Calculate the target address of the branch
                proc.pc += imm * 4          # Set the program counter (pc) to the target address
                
        elif code.op == '000101':  # bne
            if code.imm[0] == '1':
                imm = int(code.imm[1:], 2) - (2 ** 15)
            else:
                imm = int(code.imm, 2)
            if proc.registers[code.rs] != proc.registers[code.rt]:
                proc.pc += imm * 4
                
        elif code.op == '100000':  # lb
            rs = int(code.rs, 2)  
            rt = int(code.rt, 2)  
            imm = int(code.imm, 2) 
            address = proc.registers[code.rs] + imm  # Calculate memory address
            # Load the byte from memory at the calculated address and sign-extend it to a 32-bit value
            # Convert the byte value to its binary representation
            binary_value = bin(proc.data_memory[address])[2:].zfill(8)
            # Assign the binary value to the register
            proc.registers[code.rt] = int(binary_value, 2)
 
#start execution till exit code is reached           
while True:
    decode(proc.fetch())