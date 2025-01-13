#include "circuit_breaker_impl.hpp"

#include <iostream>

CircuitBreakerSMImpl::CircuitBreakerSMImpl() 
    : CircuitBreakerSM() {

    }

CircuitBreakerSMImpl::~CircuitBreakerSMImpl() {
}

void CircuitBreakerSMImpl::ClosedRun() {
    std::cout << "Running State: 'ClosedRun'" << std::endl;
    if (Consume(Input::Open) != TransitionResult::Ok) {
        throw("Invalid Transition!");
    }
}

void CircuitBreakerSMImpl::ClosingRun() {
    std::cout << "Running State: 'ClosingRun'" << std::endl;
    if (Consume(Input::Successful) != TransitionResult::Ok) {
        throw("Invalid Transition!");
    }

}

void CircuitBreakerSMImpl::InitRun() {
    std::cout << "Running State: 'InitRun'" << std::endl;
    if (Consume(Input::IsOpen) != TransitionResult::Ok) {
        throw("Invalid Transition!");
    }
}

void CircuitBreakerSMImpl::OpenRun() {
    std::cout << "Running State: 'OpenRun'" << std::endl;
    if (Consume(Input::Close) != TransitionResult::Ok) {
        throw("Invalid Transition!");
    }
}

void CircuitBreakerSMImpl::OpeningRun() {
    std::cout << "Running State: 'OpeningRun'" << std::endl;
    if (Consume(Input::Successful) != TransitionResult::Ok) {
        throw("Invalid Transition!");
    }
}

void CircuitBreakerSMImpl::FaultRun() {
    std::cout << "Running State: 'FaultRun'" << std::endl;
    if (Consume(Input::Clear) != TransitionResult::Ok) {
        throw("Invalid Transition!");
    }

}