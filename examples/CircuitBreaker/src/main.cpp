
#include "circuit_breaker_impl.hpp"
#include <unistd.h>

int main() {

    CircuitBreakerSMImpl sm = CircuitBreakerSMImpl();

    for (size_t i = 0; i < 100; i++) {
        CircuitBreakerSM_Run(sm);
        usleep(1000);
    }
   
    return 0;
}