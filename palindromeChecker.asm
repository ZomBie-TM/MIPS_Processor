#sample code
.data
prompt: .asciiz"Enter a positive integer to check if it is a plaindrome or not. \n"
true: .asciiz"Number is a palindrome"
false: .asciiz"Number is not a palindrome"
newLine: .asciiz"\n"
num: .word 0

.text
main:
	li $t4,0
	#asking the user to enter an integer
	li $v0,4 #4 is the opcode for printing a string
	la $a0,prompt
	syscall
	#system will read an integer into register $v0
	li $v0,5 	#5 is the opcode to read an integer into the register $v0
	syscall
	sw $v0,num
	lw $s0,num	#this moves the value in $v0 to $s0
	move $t0,$s0 	#this gives us a copy of the given integer to compare when we get a palindrome
	
	#now we have an integer given by user in $s0
	li $t2,0
	li $t1,10	# $t1 register has value 10
	
gettingDigits:
	div $s0,$t1	#we divide the value of $s0 by value in $t1 which is 10
	mflo $s0	#the quotient of the div is stored in LO register so i moved it from LO to $s0	
	mfhi $t3	#t3 will store the remainder of the div ie the last digit 
	mult $t2,$t1	#we will build the palindrome in $t2 by multiplying by 10 
	mflo $t2
	add $t2,$t2,$t3	#we add the remainder to get the palindrome
	beqz $s0,checkPalindrome
	bnez $s0,gettingDigits
	
checkPalindrome:
	beq $t2,$t0,pintTrue
	bne $t2,$t0,pintFalse
	
pintTrue:
	li $v0,4
	la $a0, true
	syscall
	li $v0,10
	syscall
	
pintFalse:
	li $v0,4
	la $a0, false
	syscall
	li $v0,10
	syscall
	
	
	
	
