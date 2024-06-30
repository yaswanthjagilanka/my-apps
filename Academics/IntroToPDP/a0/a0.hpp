/*  YASWANTH
 *  JAGILANKA
 *  yjagilan
 */

#ifndef A0_HPP
#define A0_HPP

#include <vector>
#include <omp.h>

void filter_2d(int n, int m, const std::vector<float> &K, std::vector<float> &A)
{
    int i, j, t;
    std::vector<float> R(n * m);
    std::vector<float> KL(3);

    for (t = 0; t < 3; ++t)
        KL[t] = K[3 * t] + K[3 * t + 1] + K[3 * t + 2];

#pragma omp parallel shared(KL,m,n,R,A)
    {
#pragma omp for
        for (i = 0; i < n; ++i)
        {
            for (j = i * m; j < i * m + m; ++j)
            {
                if (i == 0 || i == n - 1 || j % (i * m) == 0 || (j + 1) % m == 0)
                    R[j] = A[j];
                else
                    R[j] = (A[j - m - 1] * KL[0] + A[j - m] * KL[1] + A[j - m + 1] * KL[2]) + (A[j - 1] * KL[0] + A[j] * KL[1] + A[j + 1] * KL[2]) + (A[j + m - 1] * KL[0] + A[j + m] * KL[1] + A[j + m + 1] * KL[2]);
            }
        }
    }

#pragma omp parallel shared(R, A)
        {
#pragma omp for
            for (i = 0; i < n; ++i)
            {
                for (j = i * m; j < i * m + m; ++j)
                {
            A[j] = R[j];
                }
            }
        }
    
} // filter_2d

#endif // A0_HPP
