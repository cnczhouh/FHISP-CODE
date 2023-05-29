.file       "udelay_asm.S"

/*
 * void _wait(int n);
 * dual instruction loop
 * total instruction count = 2*n + 4
 */
.global _wait
_wait:
    mov		lp_count, r0
    lp      wait_loop_end
wait_loop_in:
    nop_s
    nop_s
wait_loop_end:
    j_s [blink]
    nop_s
