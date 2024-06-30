/*  YASWANTH
 *  JAGILANKA
 *  YJAGILAN
 */

#ifndef A3_HPP
#define A3_HPP
#include <cuda_runtime_api.h>
#include <iostream>
#include <vector>
#include <math.h>
# define M_PI           3.14159265358979323846  /* pi */

__global__ void compute(int n,float h,float* d_x, float* d_y, int num_blocks,int block_size){

    // Intra Block buffer for threads
    __shared__ float buf[1024];

    // #read your respective element into variables
    int tid = threadIdx.x;
    int ti = blockIdx.x * blockDim.x + threadIdx.x;
    float x_val = d_x[tid];
    float m = n*h*pow(2*M_PI,0.5);
    float k = 0;


    int index;
    // start your for loop iteration

    // Iterate to get data from all blocks possible
    for (int s = 0; s < num_blocks;++s){
    index = (blockIdx.x + s)%num_blocks;
    index = index*blockDim.x + tid;
    buf[tid] = d_x[index];
    // Sync threads for data fetching
    __syncthreads();

    // Calculating the value with the slot of data in current block avaialable
    for (int b = 0; b < blockDim.x; ++b) {
            float t = (x_val - buf[b])/h;
            k += expf(-powf(t,2));
        }
    // Sync threads for data calculation
    __syncthreads();
    }
    d_y[ti] = k/m;


}


void gaussian_kde(int n, float h, const std::vector<float>& x, std::vector<float>& y) {

    int size = n*sizeof(float);

    float* d_x;
    float* d_y;

    cudaMalloc(&d_x, size);
    cudaMalloc(&d_y, size);

    cudaMemcpy(d_x, x.data(), size, cudaMemcpyHostToDevice);
    cudaMemcpy(d_y, y.data(), size, cudaMemcpyHostToDevice);

    const int block_size = 1024;
    int num_blocks = (n+block_size - 1)/block_size;
    compute<<<num_blocks,block_size>>>(n,h, d_x, d_y,num_blocks,block_size);

    cudaMemcpy(y.data(), d_y, size, cudaMemcpyDeviceToHost);

    cudaFree(d_x);
    cudaFree(d_y);
    cudaError_t err = cudaGetLastError();
    if (err != cudaSuccess) 
        printf("Error: %s\n", cudaGetErrorString(err));



} // gaussian_kde

#endif // A3_HPP
