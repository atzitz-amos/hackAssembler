@256
D=A
@SP
M=D
	// push retAddr
	@main$ret.0
	D=A
	@SP
	M=M+1
	A=M-1
	M=D
	// push LCL
	@LCL
	D=M
	@SP
	M=M+1
	A=M-1
	M=D
	// push ARG
	@ARG
	D=M
	@SP
	M=M+1
	A=M-1
	M=D
	// push THIS
	@THIS
	D=M
	@SP
	M=M+1
	A=M-1
	M=D
	// push THAT
	@THAT
	D=M
	@SP
	M=M+1
	A=M-1
	M=D
	// GOTO
	@Sys.init
	0; JMP
	(main$ret.0)
// function Class1.set 0
(Class1.set)
// push argument 0
@0
D=A
@ARG
A=D+M
D=M
@SP
M=M+1
A=M-1
M=D
// pop static 0
@SP
M=M-1
A=M
D=M
@Class1.0
M=D
// push argument 1
@1
D=A
@ARG
A=D+M
D=M
@SP
M=M+1
A=M-1
M=D
// pop static 1
@SP
M=M-1
A=M
D=M
@Class1.1
M=D
// push constant 0
@0
D=A
@SP
M=M+1
A=M-1
M=D
// return
	// store endFrame
	@LCL
	D=M
	@R15
	M=D
	// store returnAddress
	@5
	D=D-A
	A=D
	D=M
	@R14
	M=D
	// push return value
	@SP
	M=M-1
	A=M
	D=M
	@ARG
	A=M
	M=D
	// set SP
	@ARG
	D=M+1
	@SP
	M=D
	// restore THAT
	@R15
	M=M-1
	A=M
	D=M
	@THAT
	M=D
	// restore THIS
	@R15
	M=M-1
	A=M
	D=M
	@THIS
	M=D
	// restore ARG
	@R15
	M=M-1
	A=M
	D=M
	@ARG
	M=D
	// restore LCL
	@R15
	M=M-1
	A=M
	D=M
	@LCL
	M=D
	// goto retAddr
	@R14
	A=M
	0; JMP
// function Class1.get 0
(Class1.get)
// push static 0
@Class1.0
D=M
@SP
M=M+1
A=M-1
M=D
// push static 1
@Class1.1
D=M
@SP
M=M+1
A=M-1
M=D
// sub
@SP
M=M-1
A=M-1
D=M
@SP
M=M-1
A=M+1
D=D-M
@SP
M=M+1
A=M-1
M=D
// return
	// store endFrame
	@LCL
	D=M
	@R15
	M=D
	// store returnAddress
	@5
	D=D-A
	A=D
	D=M
	@R14
	M=D
	// push return value
	@SP
	M=M-1
	A=M
	D=M
	@ARG
	A=M
	M=D
	// set SP
	@ARG
	D=M+1
	@SP
	M=D
	// restore THAT
	@R15
	M=M-1
	A=M
	D=M
	@THAT
	M=D
	// restore THIS
	@R15
	M=M-1
	A=M
	D=M
	@THIS
	M=D
	// restore ARG
	@R15
	M=M-1
	A=M
	D=M
	@ARG
	M=D
	// restore LCL
	@R15
	M=M-1
	A=M
	D=M
	@LCL
	M=D
	// goto retAddr
	@R14
	A=M
	0; JMP
// function Class2.set 0
(Class2.set)
// push argument 0
@0
D=A
@ARG
A=D+M
D=M
@SP
M=M+1
A=M-1
M=D
// pop static 0
@SP
M=M-1
A=M
D=M
@Class2.0
M=D
// push argument 1
@1
D=A
@ARG
A=D+M
D=M
@SP
M=M+1
A=M-1
M=D
// pop static 1
@SP
M=M-1
A=M
D=M
@Class2.1
M=D
// push constant 0
@0
D=A
@SP
M=M+1
A=M-1
M=D
// return
	// store endFrame
	@LCL
	D=M
	@R15
	M=D
	// store returnAddress
	@5
	D=D-A
	A=D
	D=M
	@R14
	M=D
	// push return value
	@SP
	M=M-1
	A=M
	D=M
	@ARG
	A=M
	M=D
	// set SP
	@ARG
	D=M+1
	@SP
	M=D
	// restore THAT
	@R15
	M=M-1
	A=M
	D=M
	@THAT
	M=D
	// restore THIS
	@R15
	M=M-1
	A=M
	D=M
	@THIS
	M=D
	// restore ARG
	@R15
	M=M-1
	A=M
	D=M
	@ARG
	M=D
	// restore LCL
	@R15
	M=M-1
	A=M
	D=M
	@LCL
	M=D
	// goto retAddr
	@R14
	A=M
	0; JMP
// function Class2.get 0
(Class2.get)
// push static 0
@Class2.0
D=M
@SP
M=M+1
A=M-1
M=D
// push static 1
@Class2.1
D=M
@SP
M=M+1
A=M-1
M=D
// sub
@SP
M=M-1
A=M-1
D=M
@SP
M=M-1
A=M+1
D=D-M
@SP
M=M+1
A=M-1
M=D
// return
	// store endFrame
	@LCL
	D=M
	@R15
	M=D
	// store returnAddress
	@5
	D=D-A
	A=D
	D=M
	@R14
	M=D
	// push return value
	@SP
	M=M-1
	A=M
	D=M
	@ARG
	A=M
	M=D
	// set SP
	@ARG
	D=M+1
	@SP
	M=D
	// restore THAT
	@R15
	M=M-1
	A=M
	D=M
	@THAT
	M=D
	// restore THIS
	@R15
	M=M-1
	A=M
	D=M
	@THIS
	M=D
	// restore ARG
	@R15
	M=M-1
	A=M
	D=M
	@ARG
	M=D
	// restore LCL
	@R15
	M=M-1
	A=M
	D=M
	@LCL
	M=D
	// goto retAddr
	@R14
	A=M
	0; JMP
// function Sys.init 0
(Sys.init)
// push constant 6
@6
D=A
@SP
M=M+1
A=M-1
M=D
// push constant 8
@8
D=A
@SP
M=M+1
A=M-1
M=D
// call Class1.set 2
	// push retAddr
	@Sys.init$ret.11
	D=A
	@SP
	M=M+1
	A=M-1
	M=D
	// push LCL
	@LCL
	D=M
	@SP
	M=M+1
	A=M-1
	M=D
	// push ARG
	@ARG
	D=M
	@SP
	M=M+1
	A=M-1
	M=D
	// push THIS
	@THIS
	D=M
	@SP
	M=M+1
	A=M-1
	M=D
	// push THAT
	@THAT
	D=M
	@SP
	M=M+1
	A=M-1
	M=D
	// set ARG
	@SP
	D=M
	@7
	D=D-A
	@ARG
	M=D
	// set LCL
	@SP
	D=M
	@LCL
	M=D
	// GOTO
	@Class1.set
	0; JMP
	(Sys.init$ret.11)
// pop temp 0 
@SP
M=M-1
A=M
D=M
@R5
M=D
// push constant 23
@23
D=A
@SP
M=M+1
A=M-1
M=D
// push constant 15
@15
D=A
@SP
M=M+1
A=M-1
M=D
// call Class2.set 2
	// push retAddr
	@Sys.init$ret.15
	D=A
	@SP
	M=M+1
	A=M-1
	M=D
	// push LCL
	@LCL
	D=M
	@SP
	M=M+1
	A=M-1
	M=D
	// push ARG
	@ARG
	D=M
	@SP
	M=M+1
	A=M-1
	M=D
	// push THIS
	@THIS
	D=M
	@SP
	M=M+1
	A=M-1
	M=D
	// push THAT
	@THAT
	D=M
	@SP
	M=M+1
	A=M-1
	M=D
	// set ARG
	@SP
	D=M
	@7
	D=D-A
	@ARG
	M=D
	// set LCL
	@SP
	D=M
	@LCL
	M=D
	// GOTO
	@Class2.set
	0; JMP
	(Sys.init$ret.15)
// pop temp 0 
@SP
M=M-1
A=M
D=M
@R5
M=D
// call Class1.get 0
	// push retAddr
	@Sys.init$ret.17
	D=A
	@SP
	M=M+1
	A=M-1
	M=D
	// push LCL
	@LCL
	D=M
	@SP
	M=M+1
	A=M-1
	M=D
	// push ARG
	@ARG
	D=M
	@SP
	M=M+1
	A=M-1
	M=D
	// push THIS
	@THIS
	D=M
	@SP
	M=M+1
	A=M-1
	M=D
	// push THAT
	@THAT
	D=M
	@SP
	M=M+1
	A=M-1
	M=D
	// set ARG
	@SP
	D=M
	@5
	D=D-A
	@ARG
	M=D
	// set LCL
	@SP
	D=M
	@LCL
	M=D
	// GOTO
	@Class1.get
	0; JMP
	(Sys.init$ret.17)
// call Class2.get 0
	// push retAddr
	@Sys.init$ret.18
	D=A
	@SP
	M=M+1
	A=M-1
	M=D
	// push LCL
	@LCL
	D=M
	@SP
	M=M+1
	A=M-1
	M=D
	// push ARG
	@ARG
	D=M
	@SP
	M=M+1
	A=M-1
	M=D
	// push THIS
	@THIS
	D=M
	@SP
	M=M+1
	A=M-1
	M=D
	// push THAT
	@THAT
	D=M
	@SP
	M=M+1
	A=M-1
	M=D
	// set ARG
	@SP
	D=M
	@5
	D=D-A
	@ARG
	M=D
	// set LCL
	@SP
	D=M
	@LCL
	M=D
	// GOTO
	@Class2.get
	0; JMP
	(Sys.init$ret.18)
// label END
(END)
// goto END
@END
0; JMP
