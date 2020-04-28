#include "blas.h"

__global__ static void gradientsAverage(float *gradients, int size, int nRanks)
{
    int index = (blockIdx.x + blockIdx.y * gridDim.x) * blockDim.x + threadIdx.x;
    if (index >= size) return;
    gradients[index] /= (float) nRanks;
}

void gradients_Average(float *gradients, int size, int nRanks, cudaStream_t cudaStream)
{
    gradientsAverage<<<cuda_gridsize(size), BLOCK, 0, cudaStream>>>(gradients, size, nRanks);
}

__global__ static void gradientsReduce(float *gradients, float *buf, int size)
{
    int index = (blockIdx.x + blockIdx.y * gridDim.x) * blockDim.x + threadIdx.x;
    if (index >= size) return;
    gradients[index] += buf[index];
}

void gradients_Reduce(float *gradients, float *buf, int size, cudaStream_t cudaStream)
{
    gradientsReduce<<<cuda_gridsize(size), BLOCK, 0, cudaStream>>>(gradients, buf, size);
}