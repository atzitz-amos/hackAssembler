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
// pop pointer 1           
@SP
M=M-1
A=M
D=M
@THAT
M=D
// push constant 0         
@0
D=A
@SP
M=M+1
A=M-1
M=D
// pop that 0              
@0
D=A
@THAT
D=D+M
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// push constant 1   
@1
D=A
@SP
M=M+1
A=M-1
M=D
// pop that 1              
@1
D=A
@THAT
D=D+M
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
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
// push constant 2         
@2
D=A
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
// pop argument 0          
@0
D=A
@ARG
D=D+M
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// label LOOP
(LOOP)
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
// if-goto COMPUTE_ELEMENT 
@SP
M=M-1
A=M
D=M
@COMPUTE_ELEMENT
D; JNE
// goto END                
@END
0; JMP
// label COMPUTE_ELEMENT
(COMPUTE_ELEMENT)
// push that 0
@0
D=A
@THAT
A=D+M
D=M
@SP
M=M+1
A=M-1
M=D
// push that 1
@1
D=A
@THAT
A=D+M
D=M
@SP
M=M+1
A=M-1
M=D
// add
@SP
M=M-1
A=M-1
D=M
@SP
M=M-1
A=M+1
D=D+M
@SP
M=M+1
A=M-1
M=D
// pop that 2
@2
D=A
@THAT
D=D+M
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// push pointer 1
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
// push constant 1
@1
D=A
@SP
M=M+1
A=M-1
M=D
// add
@SP
M=M-1
A=M-1
D=M
@SP
M=M-1
A=M+1
D=D+M
@SP
M=M+1
A=M-1
M=D
// pop pointer 1 
@SP
M=M-1
A=M
D=M
@THAT
M=D
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
// push constant 1
@1
D=A
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
// pop argument 0          
@0
D=A
@ARG
D=D+M
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// goto LOOP
@LOOP
0; JMP
// label END
(END)
