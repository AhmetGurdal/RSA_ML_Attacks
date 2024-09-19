#include <gmp.h>
#include <gmpxx.h>
#include <iostream>
#include <random>
#include "../../../usr/include/c++/13/bits/chrono.h"

void generate_prime(mpz_class &prime, int bit_length) {
    gmp_randclass rand(gmp_randinit_default);
    unsigned long seed = std::chrono::system_clock::now().time_since_epoch() / std::chrono::microseconds(1);
    rand.seed(seed);

    while (true) {
        // Generate a random number
        prime = rand.get_z_bits(bit_length);

        // Ensure the number is odd
        mpz_setbit(prime.get_mpz_t(), 0);

        // Use GMP's built-in primality test with 25 rounds of Miller-Rabin
        if (mpz_probab_prime_p(prime.get_mpz_t(), 25) > 0) {
            break;
        }
    }
}

void help() {
    std::cout << "Usage: ./gen <bit_length> <base> <total>\n";
}

int main(int argc, char** argv) {
    FILE *file = fopen("primes.txt", "w");;
    if(argc != 4){
        help();
        return -1;
    }
    
    int total = 0;
    int bit_length = atoi(argv[1]);
    int base = atoi(argv[2]);
    int iteration = atoi(argv[3]);
    if (file != NULL) { 
        while(total != iteration){
            mpz_class prime;
            generate_prime(prime, bit_length);
            std::string bit_version = prime.get_str(2);
            if(size(bit_version) == bit_length){  
                fprintf(file, "%s\n",prime.get_str(base).c_str());
                total += 1;
            }
        }
    }
    else{
        printf("Error opening the file.\n"); 
        return 1;
    }
    fclose(file);
    return 0;
}