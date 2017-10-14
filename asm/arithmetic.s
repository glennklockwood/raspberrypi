/*
 * make arithmetic; ./arithmetic; echo $?
 *
 * Relies on the C runtime to wrap this assembly and return the final value
 * as the application's exit code.
 *
 */
.global main
 
main:
    mov r1, #6      /* set register r1 to immediate value of 6 */
    mov r2, #4      /* set register r2 to immediate value of 4 */
    add r0, r1, r2  /* add contents of r1 and r2, store in r3 */
    bx lr           /* branch to link register */
