#include <unistd.h>

#include "circuit_breaker_impl.hpp"

int main() {

    CircuitBreakerSMImpl sm = CircuitBreakerSMImpl();

    for (size_t i = 0; i < 20; i++) {
        CircuitBreakerSM_Run(sm);
        usleep(1000);
    }
   
    return 0;
}