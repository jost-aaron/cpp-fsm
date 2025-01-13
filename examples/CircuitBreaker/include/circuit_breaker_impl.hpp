#include "cpp-fsm/circuit_breaker.hpp"

/**
 * @class CircuitBreakerSMImpl
 * @brief Implementation of the Circuit Breaker State Machine.
 * 
 * This class provides the implementation for the different states of a circuit breaker.
 */
class CircuitBreakerSMImpl : public CircuitBreakerSM {
private:
    /* data */
public:
    /**
     * @brief Construct a new Circuit Breaker SMImpl object.
     */
    CircuitBreakerSMImpl();

    /**
     * @brief Destroy the Circuit Breaker SMImpl object.
     */
    ~CircuitBreakerSMImpl();

    /**
     * @brief Run the logic for the Closed state.
     */
    void ClosedRun();

    /**
     * @brief Run the logic for the Closing state.
     */
    void ClosingRun();

    /**
     * @brief Run the logic for the Init state.
     */
    void InitRun();

    /**
     * @brief Run the logic for the Open state.
     */
    void OpenRun();

    /**
     * @brief Run the logic for the Opening state.
     */
    void OpeningRun();

    /**
     * @brief Run the logic for the Fault state.
     */
    void FaultRun();
};

