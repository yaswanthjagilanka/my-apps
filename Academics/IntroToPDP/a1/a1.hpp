/*  YASWANTH
 *  JAGILANKA
 *  YJAGILAN
 */

#ifndef A1_HPP
#define A1_HPP

#include <vector>


void isort(std::vector<short int>& Xi, MPI_Comm comm) {
    
    int size = -1;
    int rank = -1;
    int i,j;

    MPI_Comm_size(comm, &size);
    MPI_Comm_rank(comm, &rank);

    // Code to be executed inside the processor of Rank 0
    if(rank==0){
        // Initialising Vector which holds the count of each element inside the processor
        std::vector<long long int> vector1(2*size-1, 0);
        int len =2*size-1;

        /* Updating the Count of each element using traversal in whole list
        This runs in a time of O(n) */
        for (i=0;i<Xi.size();i++)
            vector1[Xi[i]+size-1]=vector1[Xi[i]+size-1]+1;
        
        // Initialising Vector to hold the data received from other processors
        std::vector<long long int> vector2(2*size-1, 0);
        
        /* Receive the data from all other ranks using MPI_Recv
        Update the values by appending them to main vector */
        for(i=1;i<size;i++){
            MPI_Recv(&vector2[0], len, MPI_LONG_LONG_INT, i, i, comm,MPI_STATUS_IGNORE);
            for(j=0;j<len;j++)
                vector1[j] = vector2[j] + vector1[j];
        }
        
        // Send the count vector to all the other size-1 processors
        for(i=1;i<size;i++)
            MPI_Send(&vector1[0], len, MPI_LONG_LONG_INT, i, i*2, comm);

        // Replacing the vector Xi with the updated sorted elements
        std::vector<short int> Xi(vector1[0],-size+1);
    }

    // Code to be executed inside the processor other than Rank 0
    else{  
        // Initialising Vector which holds the count of each element inside the processor
        std::vector<long long int> vector1(2*size-1, 0);
        int len =2*size-1;

        /* Updating the Count of each element using traversal in whole list
        This runs in a time of O(n) */
        for (i=0;i<Xi.size();i++)
            vector1[Xi[i]+size-1]=vector1[Xi[i]+size-1]+1;

        //  Send the data in vector1 with count to Rank 0 for final aggregation
        MPI_Send(&vector1[0],len,MPI_LONG_LONG_INT,0,rank,comm);

        // Receive the final count to be populated in each of the Ranks
        MPI_Recv(&vector1[0], len, MPI_LONG_LONG_INT, 0, rank*2, comm,MPI_STATUS_IGNORE);

        // Replacing the vector Xi with the updated sorted elements
        std::vector<short int> Xi(vector1[2*rank-1] + vector1[2*rank],2*rank-size); 
        fill(Xi.begin() + vector1[2*rank-1], Xi.end(), 2*rank-size+1);
    }

} // isort

#endif // A1_HPP
