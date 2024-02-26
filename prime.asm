.data
    mymessage: .asciiz "Enter a number: "
    Not_Prime: .asciiz "NOT PRIME\n"
    Prime: .asciiz "PRIME\n"
    Mynumber: .word 0

.text
main:
    # Print mymessage
    li $v0, 4              # syscall code to print string
    la $a0, mymessage      # load address of mymessage into $a0
    syscall

    # Read user input
    li $v0, 5              # syscall code to read integer
    syscall
    sw $v0, Mynumber       # store user input in Mynumber
    move $t8, $v0          # store user input in $t8

    # check if input is less than 2
    li $t7, 2              # load 2 into $t7
    ble $t8, $t7, notPrime # if the input in $t8 <= 2 then jump to notPrime

    # start checking by dividing from 2
    li $t6, 2              # load 2 into $t6 (divisor)
loop:
    beq $t6, $t8, prime    # if divisor == number, then it is a prime
    div $t8, $t6           # dividing the number by divisor
    mfhi $t5               # get remainder in $t5
    beq $t5, $zero, notPrime # if number is exactly divisible by any number between 2 to that number then it is not prime
    add $t6, $t6, 1        # divisor++
    j loop                 # jump unconditionally

prime:
    # to print the number entered is prime (when the number is prime)
    li $v0, 4              # syscall code to print string
    la $a0, Prime          # load address of string Prime to $a0
    syscall
    j exit                 # jump to exit

notPrime:
    # to print the number entered is not prime (when the number is not prime)
    li $v0, 4              # syscall code to print string
    la $a0, Not_Prime      # load address of string Not_Prime to $a0
    syscall
    j exit                 # jump to exit

exit:
    li $v0, 10             # syscall code to exit
    syscall
