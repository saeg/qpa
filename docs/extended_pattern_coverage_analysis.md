# Extended Pattern Coverage Analysis

This report analyzes the coverage of 61 extended patterns across:
- Three sourcing frameworks (Classiq, PennyLane, Qiskit)
- Broader target list of projects

## Summary Statistics

### Framework Coverage
| Framework | Patterns Found | Coverage % |
|-----------|----------------|------------|
| Classiq | 17 | 27.9% |
| PennyLane | 20 | 32.8% |
| Qiskit | 13 | 21.3% |

### Target Project Coverage
**Patterns found in target projects: 21 (34.4%)**

## Detailed Framework Analysis

### Classiq
**Found: 17 patterns**

**Patterns found:**
- Amplitude Amplification
- Basis Change
- Circuit Construction Utility
- Creating Entanglement
- Data Encoding
- Dynamic Circuit
- Function Table
- Grover
- Hamiltonian Simulation
- Initialization
- Oracle
- Phase Shift
- Quantum Approximate Optimization Algorithm (QAOA)
- Quantum Arithmetic
- Quantum Phase Estimation (QPE)
- SWAP Test
- Variational Quantum Algorithm (VQA)

**Missing patterns (44):**
- Ad-hoc Hybrid Code Execution
- Alternating Operator Ansatz (AOA)
- Biased Initial State
- Chained Optimization
- Circuit Cutting
- Classical-Quantum Interface
- Error Correction
- Gate Cut
- Gate Error Mitigation
- Hadamard Test
- Hybrid Module
- Linear Combination of Unitaries (LCU)
- Mid-Circuit Measurement
- Orchestrated Execution
- Post-Selective Measurement
- Pre-Trained Feature Extractor
- Pre-deployed Execution
- Prioritized Execution
- Quantum Amplitude Estimation (QAE)
- Quantum Application Archive
- Quantum Application Testing
- Quantum Associative Memory (QuAM)
- Quantum Circuit Translator
- Quantum Classification
- Quantum Clustering
- Quantum Hardware Selection
- Quantum Kernel Estimator (QKE)
- Quantum Logical Operators
- Quantum Module
- Quantum Module Template
- Quantum Neural Network (QNN)
- Quantum Singular Value Transformation (QSVT)
- Quantum-Classic Split
- Readout Error Mitigation
- Schmidt Decomposition
- Speedup via Verifying
- Standalone Circuit Execution
- Uncompute
- Unified Execution
- Unified Observability
- Variational Parameter Transfer
- Variational Quantum Eigensolver (VQE)
- Warm Start
- Wire Cut

### PennyLane
**Found: 20 patterns**

**Patterns found:**
- Amplitude Amplification
- Basis Change
- Circuit Construction Utility
- Data Encoding
- Grover
- Hamiltonian Simulation
- Initialization
- Linear Combination of Unitaries (LCU)
- Oracle
- Phase Shift
- Quantum Amplitude Estimation (QAE)
- Quantum Approximate Optimization Algorithm (QAOA)
- Quantum Arithmetic
- Quantum Neural Network (QNN)
- Quantum Phase Estimation (QPE)
- Quantum Singular Value Transformation (QSVT)
- SWAP Test
- Schmidt Decomposition
- Variational Quantum Algorithm (VQA)
- Variational Quantum Eigensolver (VQE)

**Missing patterns (41):**
- Ad-hoc Hybrid Code Execution
- Alternating Operator Ansatz (AOA)
- Biased Initial State
- Chained Optimization
- Circuit Cutting
- Classical-Quantum Interface
- Creating Entanglement
- Dynamic Circuit
- Error Correction
- Function Table
- Gate Cut
- Gate Error Mitigation
- Hadamard Test
- Hybrid Module
- Mid-Circuit Measurement
- Orchestrated Execution
- Post-Selective Measurement
- Pre-Trained Feature Extractor
- Pre-deployed Execution
- Prioritized Execution
- Quantum Application Archive
- Quantum Application Testing
- Quantum Associative Memory (QuAM)
- Quantum Circuit Translator
- Quantum Classification
- Quantum Clustering
- Quantum Hardware Selection
- Quantum Kernel Estimator (QKE)
- Quantum Logical Operators
- Quantum Module
- Quantum Module Template
- Quantum-Classic Split
- Readout Error Mitigation
- Speedup via Verifying
- Standalone Circuit Execution
- Uncompute
- Unified Execution
- Unified Observability
- Variational Parameter Transfer
- Warm Start
- Wire Cut

### Qiskit
**Found: 13 patterns**

**Patterns found:**
- Basis Change
- Circuit Construction Utility
- Data Encoding
- Grover
- Hamiltonian Simulation
- Initialization
- Oracle
- Quantum Approximate Optimization Algorithm (QAOA)
- Quantum Arithmetic
- Quantum Logical Operators
- Quantum Phase Estimation (QPE)
- Variational Quantum Algorithm (VQA)
- Variational Quantum Eigensolver (VQE)

**Missing patterns (48):**
- Ad-hoc Hybrid Code Execution
- Alternating Operator Ansatz (AOA)
- Amplitude Amplification
- Biased Initial State
- Chained Optimization
- Circuit Cutting
- Classical-Quantum Interface
- Creating Entanglement
- Dynamic Circuit
- Error Correction
- Function Table
- Gate Cut
- Gate Error Mitigation
- Hadamard Test
- Hybrid Module
- Linear Combination of Unitaries (LCU)
- Mid-Circuit Measurement
- Orchestrated Execution
- Phase Shift
- Post-Selective Measurement
- Pre-Trained Feature Extractor
- Pre-deployed Execution
- Prioritized Execution
- Quantum Amplitude Estimation (QAE)
- Quantum Application Archive
- Quantum Application Testing
- Quantum Associative Memory (QuAM)
- Quantum Circuit Translator
- Quantum Classification
- Quantum Clustering
- Quantum Hardware Selection
- Quantum Kernel Estimator (QKE)
- Quantum Module
- Quantum Module Template
- Quantum Neural Network (QNN)
- Quantum Singular Value Transformation (QSVT)
- Quantum-Classic Split
- Readout Error Mitigation
- SWAP Test
- Schmidt Decomposition
- Speedup via Verifying
- Standalone Circuit Execution
- Uncompute
- Unified Execution
- Unified Observability
- Variational Parameter Transfer
- Warm Start
- Wire Cut

## Target Project Analysis

**Patterns found in target projects: 21**

**Patterns found:**
- Amplitude Amplification
- Basis Change
- Circuit Construction Utility
- Creating Entanglement
- Data Encoding
- Grover
- Hamiltonian Simulation
- Initialization
- Linear Combination of Unitaries (LCU)
- Oracle
- Phase Shift
- Quantum Amplitude Estimation (QAE)
- Quantum Approximate Optimization Algorithm (QAOA)
- Quantum Arithmetic
- Quantum Logical Operators
- Quantum Neural Network (QNN)
- Quantum Phase Estimation (QPE)
- Quantum Singular Value Transformation (QSVT)
- SWAP Test
- Variational Quantum Algorithm (VQA)
- Variational Quantum Eigensolver (VQE)

**Missing patterns (40):**
- Ad-hoc Hybrid Code Execution
- Alternating Operator Ansatz (AOA)
- Biased Initial State
- Chained Optimization
- Circuit Cutting
- Classical-Quantum Interface
- Dynamic Circuit
- Error Correction
- Function Table
- Gate Cut
- Gate Error Mitigation
- Hadamard Test
- Hybrid Module
- Mid-Circuit Measurement
- Orchestrated Execution
- Post-Selective Measurement
- Pre-Trained Feature Extractor
- Pre-deployed Execution
- Prioritized Execution
- Quantum Application Archive
- Quantum Application Testing
- Quantum Associative Memory (QuAM)
- Quantum Circuit Translator
- Quantum Classification
- Quantum Clustering
- Quantum Hardware Selection
- Quantum Kernel Estimator (QKE)
- Quantum Module
- Quantum Module Template
- Quantum-Classic Split
- Readout Error Mitigation
- Schmidt Decomposition
- Speedup via Verifying
- Standalone Circuit Execution
- Uncompute
- Unified Execution
- Unified Observability
- Variational Parameter Transfer
- Warm Start
- Wire Cut

## Patterns Found Only in Frameworks (Not in Target Projects)

**3 patterns found in frameworks but not in target projects:**
- Dynamic Circuit
- Function Table
- Schmidt Decomposition

## Cross-Framework Analysis

**Common patterns between Classiq and PennyLane (14):**
- Amplitude Amplification
- Basis Change
- Circuit Construction Utility
- Data Encoding
- Grover
- Hamiltonian Simulation
- Initialization
- Oracle
- Phase Shift
- Quantum Approximate Optimization Algorithm (QAOA)
- Quantum Arithmetic
- Quantum Phase Estimation (QPE)
- SWAP Test
- Variational Quantum Algorithm (VQA)

**Common patterns between Classiq and Qiskit (11):**
- Basis Change
- Circuit Construction Utility
- Data Encoding
- Grover
- Hamiltonian Simulation
- Initialization
- Oracle
- Quantum Approximate Optimization Algorithm (QAOA)
- Quantum Arithmetic
- Quantum Phase Estimation (QPE)
- Variational Quantum Algorithm (VQA)

**Common patterns between PennyLane and Qiskit (12):**
- Basis Change
- Circuit Construction Utility
- Data Encoding
- Grover
- Hamiltonian Simulation
- Initialization
- Oracle
- Quantum Approximate Optimization Algorithm (QAOA)
- Quantum Arithmetic
- Quantum Phase Estimation (QPE)
- Variational Quantum Algorithm (VQA)
- Variational Quantum Eigensolver (VQE)

**Patterns found in all three frameworks (11):**
- Basis Change
- Circuit Construction Utility
- Data Encoding
- Grover
- Hamiltonian Simulation
- Initialization
- Oracle
- Quantum Approximate Optimization Algorithm (QAOA)
- Quantum Arithmetic
- Quantum Phase Estimation (QPE)
- Variational Quantum Algorithm (VQA)
