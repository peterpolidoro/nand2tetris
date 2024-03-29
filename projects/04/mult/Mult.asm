// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
  @R0
  D=M
  @n
  M=D // n = R0

  @R1
  D=M
  @m
  M=D // m = R1

  @R2
  M=0 // R2 = 0

  @i
  M=0 // i = 0

  @mult
  M=0 // mult = 0

(LOOP)
  @i
  D=M
  @m
  D=D-M
  @STOP
  D;JEQ

  @mult
  D=M
  @n
  D=D+M
  @mult
  M=D
  @i
  M=M+1
  @LOOP
  0;JMP

(STOP)
  @mult
  D=M
  @R2
  M=D // RAM[2] = mult

(END)
  @END
  0;JMP
