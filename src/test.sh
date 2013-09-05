#!/bin/sh
#PJM -j
#PJM -L "rscgrp=large"
#PJM -L "elapse=24:00:00"
#PJM -L "node=2x5"
#PJM --mpi "proc=4"
export OMP_NUM_THREADS=4
export PARALLEL=4
mpiexec ~/a.out 1
