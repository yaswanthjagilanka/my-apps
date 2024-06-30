#include <cuda_runtime_api.h>
#include <iostream>
#include <vector>

_global_ void compute(int n,float* d_x, float* d_y){
    int ti = blockIdx.x * blockDim.x + threadIdx.x;
    d_y[ti] = d_x[ti];
}

void test_cuda() {
    int n = 1000;
    int size = n*sizeof(float);

    std::vector<float> x(n);
    std::vector<float> y(n, 0);

    for(int i=0;i<n;i++){
        x[i] = i;
    }

    float* d_x;
    float* d_y;

    cudaMalloc(&d_x, size);
    cudaMalloc(&d_y, size);

    cudaMemcpy(d_x, x.data(), size, cudaMemcpyHostToDevice);
    cudaMemcpy(d_y, y.data(), size, cudaMemcpyHostToDevice);

    const int block_size = 100;
    int num_blocks = (n+block_size - 1)/block_size;
    compute<<<num_blocks,block_size>>>(n, d_x, d_y);

    cudaMemcpy(y.data(), d_y, size, cudaMemcpyDeviceToHost);

    for(int i=0;i<n;i++){
        std::cout << "y["<< i <<"]  : " << y[i] << std::endl;
    }

    cudaFree(d_x);
    cudaFree(d_y);
}

int main(int argc, char* argv[]) {
    test_cuda();
    return 0;
}