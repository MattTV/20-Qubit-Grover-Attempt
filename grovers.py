from math import sqrt
from qiskit import QuantumCircuit
from qiskit.circuit.library import MCXGate
from qiskit.compiler import transpile
from qiskit.visualization import plot_histogram
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

# YOU CHANGE
# YOU CHANGE: Entry to search for
# YOU CHANGE
find_decimal = 10

# Store and print find goals
find_binary = '{0:020b}'.format(find_decimal)
print('Search for ' + str(find_decimal) + ' (0b' + find_binary + ')')

#
# Data for use in program
#
num_data_qubits = 20
num_ctrl_qubits = 1
num_db_entries = 2**num_data_qubits
data_qubit_indices = list(range(num_data_qubits))
ctrl_qubit_indices = len(data_qubit_indices)
all_qubit_indices = list(range(num_data_qubits + num_ctrl_qubits))
all_zeroes = ""
for x in range(num_data_qubits):
    all_zeroes = all_zeroes + "0"

#
# Circuit Start
#

# Create circuit with 20 data and 1 control qubits
qc = QuantumCircuit(21)

# Put control qubit into |-> state
qc.h(ctrl_qubit_indices)
qc.z(ctrl_qubit_indices)

# Put all data qubits into |+> state
for i in range(num_data_qubits):
    qc.h(i)

#
# Create gates to repeat sqrt(N) times where N = number of entries to search through
# HOWEVER, the circuit image generator is limited to 2^16 pixels wide, which can fit less than 72 repititions
# 50 will be arbitrarily chosen for now
# Nevermind, my computer wants to explode when transpiling this. 10.
#
#for x in range(int(sqrt(num_db_entries))):
for x in range(1):

    # Oracle Begin
    qc.append(MCXGate(ctrl_qubit_indices, ctrl_state=find_binary), all_qubit_indices)
    # Oracle End

    # Diffuser Begin
    for i in range(num_data_qubits):
        qc.h(i)

    qc.append(MCXGate(ctrl_qubit_indices, ctrl_state=all_zeroes), all_qubit_indices)

    for i in range(num_data_qubits):
        qc.h(i)
    # Diffuser End

#
# End of repeating circuit
#

# Add Measurement
qc.measure_all()

#
# Circuit End
#

# Output the MatPlotLib drawing as a PNG
# I suggest opening the image in a VSCode tab
# It will update when the program runs
qc.draw('mpl', filename='qc.png')

print("Drawing output successful")

#
# Run on Quantum Hardware
#

# Login to IBM and choose a backend
# You'll need to specify the credentials when initializing QiskitRuntimeService, if they were not previously saved.
service = QiskitRuntimeService()
backend = service.least_busy(operational=True, simulator=False)

print("Choosing backend successful")

# Transpile to work with gates available on the chosen backend
tqc = transpile(qc, backend=backend, optimization_level=0)

print("Transpiling successfl")

# Submit the job and wait for the result
sampler = Sampler(backend)
job = sampler.run([tqc])
print(f"job id: {job.job_id()}")
result = job.result()[0]
print(result)

#
# Process Results
#

# Get the number of counts for each result (including the control bit differentiating them)
counts = result.data.meas.get_counts()

# Create a new dictionary of results combining both control bit states
new_counts = { }
for i in range(int(len(counts) / 2)):
    if ('0' + '{0:020b}'.format(i)) in counts and ('1' + '{0:020b}'.format(i)) in counts:
        new_counts['X' + '{0:020b}'.format(i)] = counts['0' + '{0:020b}'.format(i)] + counts['1' + '{0:020b}'.format(i)]
    elif ('0' + '{0:020b}'.format(i)) in counts:
        new_counts['X' + '{0:020b}'.format(i)] = counts['0' + '{0:020b}'.format(i)]
    elif ('1' + '{0:020b}'.format(i)) in counts:
        new_counts['X' + '{0:020b}'.format(i)] = counts['1' + '{0:020b}'.format(i)]
    else:
        new_counts['X' + '{0:020b}'.format(i)] = 0

# Output the results as a PNG
# I suggest opening the image in a VSCode tab
# It will update when the program runs
plot_histogram(new_counts, filename='result.png')