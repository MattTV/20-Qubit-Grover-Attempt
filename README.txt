Notes about 20 Qubit Grover's Algorithm Attempt

Normally I would repeat the oracle and diffuser sqrt(N) times where N = 2^n qubits. In this case, that would be 1,024 times.
My computer ran into trouble transpiling any more than a few iterations of the circuit.
The current results given use only one iteration.

The histogram can't be read in its current state, butthe high probability close to the beginning of the graph makes it likely that 0b1010 is the standout option, which is correct.

The next steps I would take with the algorithm are to use a more powerful system to transpile and create at least a dozen iterations.
I would also like to break the oracle and diffuser into their own custom gates to simplify the code.