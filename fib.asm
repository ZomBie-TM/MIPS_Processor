.data

	question1: .asciiz "\nEnter a Number: "
	
	space: " "
	
	prompt1: .asciiz "Sequence: "
	prompt2: .asciiz "\nOdd: "
	prompt3: .asciiz "\nEven: "
	
	Lmod: .word 10	#stores 10 for mod usage
	
	x: .word 0
	y: .word 1
	odd: .word 0
	even: .word 0

.text
	
lw $t4, Lmod

li $v0, 4
la $a0, question1
syscall

li $v0, 5			#get n
syscall
move $t0, $v0			# $t0 <- $v0, value which was entered


#This is for printing the sequnce
li $v0, 4
la $a0, prompt1
syscall

#Start program here
j main		#stores pointer to line in $ra

exec:
	#print odd numbers
	li $v0, 4
	la $a0, prompt2
	syscall

	li $v0, 1
	lw $a0, odd
	syscall

	#print even numbers
	li $v0, 4
	la $a0, prompt3
	syscall

	li $v0, 1
	lw $a0, even
	syscall

	#exit code
	li $v0, 10
	syscall

#Creates an if condition
main:
	bnez $t0, loop		#loop till n is zero
	j exec			#jump back to program line pointer

#Acts as a while loop
loop:
	lw $t1, x		#t1 has value of x
	la $t3, ($t1)		#temp (t3)  = x
	
	li $v0, 1		#print x in each iteration
	la $a0, ($t1)
	syscall
	
	div $t7, $t1, 2		#t7 = (x / 2), HI = (x % 2)
	mfhi $t7		#t7 <- HI
	beq $t7, 0, adde	#check if even and branch
	
	lw $t5, odd
	addi $t5, $t5, 1	#else odd
	la $a1, odd
	sw $t5, ($a1)		#store in data
	j loop2			#continue to next iteration

loop2:	
	li $v0, 4		#print space between each iteration
	la $a0, space
	syscall
	
	lw $t2, y		#get value of y
	add $t1, $t1, $t2	#x = x + y
	div $t1, $t4		#x = x / 10, HI = x % 10
	mfhi $t1		#t1 <- HI
	la $a0, x		#store x back in data
	sw $t1, ($a0)
		
	move $t2, $t3		#y = temp
	div $t2, $t4		#y = y / 10, HI = y % 10
	mfhi $t2		#t2 <- HI
	la $a0, y		#store y back in data
	sw $t2, ($a0)
	
	subi $t0, $t0, 1	#n = n - 1
	
	j main			#jump to main
	
adde:
	lw $t5, even		#if even
	addi $t5, $t5, 1	#add 1 to even count
	la $a1, even
	sw $t5, ($a1)		#store back to data
	j loop2			#countinue to next iteration
	
