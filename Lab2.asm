        .ORIG   x3000
        LEA     R0,ENTER
        PUTS    ;TRAP        x22
        LD      R1,INPUT    ;r1=first char of input
        LD      R2,START    ;r2=location of first node
        AND     R4,R4,#0
        ADD     R4,R4,#1
        ST      R4,SUC      ;if not success, SUC!=0

PUTIN   GETC                ;TRAP        x20         
        STR     R0,R1,#0    
        OUT                 ;TRAP        x21         ;input save in R0
        ADD     R1,R1,#1    
        AND     R6,R6,#0
        ADD     R6,R0,#-10
        BRnp    PUTIN       ;if not end, branch to loop head
        
        ADD     R1,R1,#-1
        AND     R0,R0,#0
        STR     R0,R1,#0    ;the last char of input = /0

NEXTNO  LDR     R2,R2,#0
        
LOOP    AND     R1,R1,#0
        ADD     R1,R2,#2    ;r1=first char of first name
        LDR     R6,R1,#0    ;read r6 as the current char(r1)
        LD      R5,INPUT    ;r5=input location
        AND     R3,R3,#0

;if the storage has a space/newline, will output this
     
MATCH1  LDR     R7,R6,#0    
        AND     R1,R1,#0    
        NOT     R1,R7       ;r1
        ADD     R1,R1,#1    ;r1=-r1.data
        LDR     R7,R5,#0    ;r7=r5.data
        ADD     R6,R6,#1    ;r6=next char of database
        ADD     R5,R5,#1    ;r5=next char of input
        ADD     R7,R7,#0
        BRz     NOT11       ;r7==line feed, continue
        ADD     R1,R1,#0
        BRz     NOT12       ;r1==line feed, continue: line feed should be: /0
        ADD     R0,R1,R7    ;if match, R0=0
        BRz     MATCH1
        ADD     R0,R0,#0    ;if not match, R3++
        BRnp    NO1

NOT11   ;if input =0, but the r7 != 0, should make R3!=0, and continue
        
        ADD     R1,R1,#0
        BRz     CONT1
        ADD     R3,R3,#1
        
        
NOT12   
        ADD     R7,R7,#0
        BRz     CONT1
        ADD     R3,R3,#1
        
        
CONT1   ADD     R3,R3,#0    ;r3==0,print
        BRz     PRINT
        ADD     R1,R2,#3    ;r1=first char of last name
        LDR     R6,R1,#0    ;read r6 as the current char(r1)
        LD      R5,INPUT    ;r5=input location
        AND     R4,R4,#0
        
MATCH2  LDR     R7,R6,#0
        AND     R1,R1,#0
        NOT     R1,R7       ;r1
        ADD     R1,R1,#1    ;r1=-r1.data
        LDR     R7,R5,#0    ;r7=r5.data
        ADD     R6,R6,#1    ;r1=next char of database
        ADD     R5,R5,#1    ;r5=next char of input
        ADD     R7,R7,#0
        BRz     NOT21       ;r7==\0, continue
        ADD     R1,R1,#0
        BRz     NOT22       ;r4==\0, continue
        ADD     R0,R1,R7    ;if match, R0=0
        BRz     MATCH2
        ADD     R0,R0,#0    ;if not match, R3++
        BRnp    NO2
        
NOT21   
        ADD     R1,R1,#0   
        BRz     CONT2
        ADD     R4,R4,#1
        
        
NOT22   
        ADD     R7,R7,#0
        BRz     CONT2
        ADD     R4,R4,#1
        
CONT2   ADD     R4,R4,#0    ;r3==0,print
        BRz     PRINT
        LDR     R0,R2,#0    ;read r0 as the current r2, if == 0, not found
        BRz     END         ;if current node starts x0000, halt
        ADD     R4,R4,#0    ;r3
        BRnp    NEXTNO      ;not macth, next node
        
PRINT   LD      R0,NEWLINE
        OUT
        LDR     R0,R2,#2    ;address of first name
        PUTS
        LD      R0,SPACE
        OUT
        LDR     R0,R2,#3    ;address of last name
        PUTS
        LD      R0,SPACE
        OUT
        LDR     R0,R2,#1    ;address of room number
        PUTS
        AND     R4,R4,#0
        ST      R4,SUC      ;if success, SUC=0
        BRnzp   NEXTNO      
        

NO1     ADD     R3,R3,#1
        BRnzp   MATCH1
    
NO2     ADD     R4,R4,#1
        BRnzp   MATCH2
        
END     LD      R4,SUC
        BRnp    FAIL
        LD      R4,SUC
        BRz     SUCCESS
        
FAIL    LEA     R0,NF
        TRAP    x22
        
SUCCESS HALT

SUC     .FILL       x0000   ;if success, SUC = 0, else = 1. = current r4
INPUT   .FILL       x3200
ENTER	.STRINGZ    "Enter a Name: "
NF      .STRINGZ    "Not Found"
SPACE   .FILL       x0020
NEWLINE .FILL       x000A
START   .FILL       x4000
        .END
