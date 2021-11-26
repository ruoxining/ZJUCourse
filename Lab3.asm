.ORIG x0200
        
            LD      R6, OS_SP
            LD      R0, USER_PSR
            ADD     R6, R6, #-1
            STR     R0, R6, #0
            LD      R0, USER_PC
            ADD     R6, R6, #-1
            STR     R0, R6, #0
;task 1
            LD      R4,KBSR     ;xFE00
            LD      R5,ONE      ;x4000
            STR     R5,R4,#0
;task 2
            LD      R4,INTV     ;x0180
            LD      R5,ISR      ;x0800
            STR     R5,R4,#0
            RTI
            
OS_SP       .FILL   x3000
USER_PSR    .FILL   x8002
USER_PC     .FILL   x3000
KBSR        .FILL   xFE00
ONE         .FILL   x4000
INTV        .FILL   x0180
ISR         .FILL   X0800
            .END

.ORIG   x0800
        
            ST      R0,saveR0	; store registers, will be reloaded after this interrupt
		    ST      R1,saveR1
		    ST      R2,saveR2
		    ST      R3,saveR3

		    LD      R1,KBDR     ; R1=location of KBDR
		    LDR     R0,R1,#0	; R0=input, r1,r2,r3 free
		    
		    ST      R0,saveINPUT

NMCHK1      NOT     R1,R0       ; r0>x0030?
            ADD     R1,R1,#1    ; r1=-r0, if r1+x0030 negative, r0>0
            LD      R2,ZERO
            ADD     R1,R1,R2
            BRnz    NMCHK2  
            ADD     R1,R1,#0
            BRp     NL

NMCHK2      NOT     R1,R0       ; r0<x0039?
            ADD     R1,R1,#1    ; r1=-r0, if r1+x0039 positive, r0<9
            LD      R2,NINE
            ADD     R1,R1,R2
            BRzp    NMINUS3     ; if a number, numerber minus3 (check whether it equals the current number (in R2), then plus or minus)
            ADD     R1,R1,#0
            BRn     CHOUT1      ; not a number, out as a char

NL          NOT     R1,R0       ; r0==Enter? Enter<x0030
            ADD     R1,R1,#1    ; 
            LD      R2,enter    
            ADD     R1,R1,R2    ; r1==0, enter
            BRz     NMINUS1     ; if==enter, number minus1 (check whether == 0, if no minus one (2))
            ADD     R1,R1,#0
		    BRnp    CHOUT1      ; if not, consider as a char
		
CHOUT1      LD      R0,enter
            OUT                 ; a newline to output
            AND     R1,R1,#0    ;
		    LD      R1,FTY  	; count for 40 times
            
CHOUT2      ADD     R1,R1,#1
            LD      R0,saveINPUT
		    OUT
		    ADD     R1,R1,#0
		    BRz     NLINE
		    ADD     R1,R1,#0
		    BRnp    CHOUT2
		    
NLINE       LD      R0,enter    ;
            OUT                 ; a newline
            LD      R2,saveR2
            AND     R1,R1,#0
            LD      R1,FTY
            BRnzp   END
        
NMINUS1     LD      R2,saveR2	; from ENTER, == 0?, r2 not free now, !!do not use r2!!, r2= current number
		    LD      R1,saveR1
            LD      R0,ZERO
            NOT     R7,R0
            ADD     R7,R7,#1
            ADD     R7,R7,R2    ; r2 = 0 or not
            BRz     END         ; if == 0, do nothing
            ADD     R7,R7,#0
            BRnp    NMINUS2     ; if != 0, minus 1
        
NMINUS2     LD      R2,saveR2   ; from MINUS1, minus one, r2 not free now, !!do not use r2!!
		    LD      R1,saveR1
            ADD     R2,R2,#-1   ; current number minus 1
            BRnzp   END         ;

NMINUS3     LD      R2,saveR2   ; from a number, minus or plus, r2 not free now, !!do not use r2!!
            LD      R1,saveR1
            ADD     R2,R0,#0    ; R2 = current input
            BRnzp   END
        
END		    LD      R0,saveR0	; restore the registers
            LD      R3,saveR3
		    RTI				

KBDR	    .FILL   xFE02
DSR		    .FILL   xFE04
DDR		    .FILL   xFE06
ZERO        .FILL   x0030
NINE        .FILL   x0039
FTY         .FILl   xFFD8
enter       .FILL   x000A
saveR0	    .FILL   x0000
saveR1	    .FILL   x0000
saveR2	    .FILL   x0000
saveR3      .FILL   x0000
saveINPUT   .FILL   x0000
            .END


.ORIG x3000

            AND     R1,R1,#0
            LD      R1,FOURTY  ;loop times
            AND     R2,R2,#0
            LD      R2,SEVEN    
            
LOOP        AND     R0,R0,#0
            ADD     R0,R2,#0    ;current output
            OUT

            BRnzp   DELAY
            
LOOP2       ADD     R1,R1,#1    ;every loop r1++
            BRz     NEWL        ;after 40 loops, print a Enter
            BRnp    LOOP
    
NEWL        LD      R1,FOURTY  ;loop times
            LD      R0,newline
            OUT
            BRnzp   LOOP
            
DELAY       ST      R3,DELAY_R3 ;FROM PDF
            LD      R3,DELAY_COUNT
        
DELAY_LOOP  ADD     R3,R3,#-1   ;FROM PDF
            BRnp    DELAY_LOOP
            LD      R3,DELAY_R3
            BRnzp   LOOP2

newline     .FILL   x000A
SEVEN       .FILL   x0037
FOURTY      .FILL   xFFD8
DELAY_COUNT .FILL   #256
DELAY_R3    .BLKW   #1
            .END