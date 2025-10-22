# Summary of Extracted Quantum Concepts (Pre-Classification)

This document summarizes the raw quantum concepts automatically extracted from the source code 
of the Qiskit, PennyLane, and Classiq frameworks. 
These concepts were identified by the `src/core_concepts/identify_*.py` scripts and serve as the input for the
manual pattern classification step.

## Pattern Coverage Analysis

This analysis compares the quantum patterns found in the three frameworks against the base list 
of 59 patterns from `quantum_patterns.json`.

**Coverage: 25.4%** (15/59 base patterns found)

### Framework Pattern Distribution

| Framework | Patterns Found |
|-----------|----------------|
| Classiq | 21 |
| PennyLane | 20 |
| Qiskit | 13 |

### Complete List of Patterns Found

#### Classiq Patterns

| Pattern | Concepts |
|---------|----------|
| Amplitude Amplification | `open_library.functions.amplitude_amplification.amplitude_amplification`, `open_library.functions.amplitude_amplification.exact_amplitude_amplification`, `open_library.functions.grover.grover_diffuser` (+2 more) |
| Basis Change | `open_library.functions.discrete_sine_cosine_transform.qct_qst_type1`, `open_library.functions.discrete_sine_cosine_transform.qct_qst_type2`, `open_library.functions.discrete_sine_cosine_transform.qct_type2` (+5 more) |
| Circuit Construction Utility | `open_library.functions.modular_exponentiation.multiswap`, `open_library.functions.utility_functions.apply_to_all` |
| Controlled Linear Rotation | `open_library.functions.linear_pauli_rotation.linear_pauli_rotations` |
| Creating Entanglement | `open_library.functions.state_preparation.prepare_bell_state`, `open_library.functions.state_preparation.prepare_ghz_state` |
| Data Encoding | `open_library.functions.state_preparation.inplace_prepare_complex_amplitudes`, `open_library.functions.state_preparation.prepare_complex_amplitudes`, `open_library.functions.state_preparation.prepare_exponential_state` (+3 more) |
| Dynamic Circuit | `open_library.functions.utility_functions.switch` |
| Function Table | `open_library.functions.lookup_table.span_lookup_table` |
| Grover | `open_library.functions.grover.grover_search` |
| Hamiltonian Simulation | `qmod.builtins.functions.exponentiation.suzuki_trotter` |
| Initialization | `open_library.functions.state_preparation.prepare_basis_state`, `open_library.functions.state_preparation.prepare_dicke_state`, `open_library.functions.state_preparation.prepare_dicke_state_unary_input` (+2 more) |
| Linear Combination of Unitaries | `open_library.functions.lcu.lcu`, `open_library.functions.lcu.lcu_pauli` |
| Oracle | `open_library.functions.grover.phase_oracle` |
| Phase Shift | `open_library.functions.qsvt.projector_controlled_double_phase`, `open_library.functions.qsvt.projector_controlled_phase` |
| Quantum Amplitude Estimation | `open_library.functions.amplitude_estimation.amplitude_estimation` |
| Quantum Approximate Optimization Algorithm (QAOA) | `open_library.functions.qaoa_penalty.qaoa_cost_layer`, `open_library.functions.qaoa_penalty.qaoa_layer`, `open_library.functions.qaoa_penalty.qaoa_mixer_layer` (+1 more) |
| Quantum Arithmetic | `open_library.functions.modular_exponentiation.c_modular_multiply`, `open_library.functions.modular_exponentiation.cc_modular_add`, `open_library.functions.modular_exponentiation.inplace_c_modular_multiply` (+3 more) |
| Quantum Phase Estimation (QPE) | `open_library.functions.qpe.qpe`, `open_library.functions.qpe.qpe_flexible` |
| Quantum Singular Value Transformation | `open_library.functions.qsvt.qsvt`, `open_library.functions.qsvt.qsvt_inversion`, `open_library.functions.qsvt.qsvt_lcu` (+2 more) |
| SWAP Test | `open_library.functions.swap_test.swap_test` |
| Variational Quantum Algorithm (VQA) | `open_library.functions.hea.full_hea` |

#### PennyLane Patterns

| Pattern | Concepts |
|---------|----------|
| Amplitude Amplification | `pennylane.templates.subroutines.amplitude_amplification.AmplitudeAmplification` |
| Basis Change | `pennylane.templates.state_preparations.superposition.Superposition`, `pennylane.templates.subroutines.aqft.AQFT`, `pennylane.templates.subroutines.qft.QFT` |
| Circuit Construction Utility | `pennylane.templates.subroutines.basis_rotation.BasisRotation`, `pennylane.templates.subroutines.permute.Permute`, `pennylane.templates.swapnetworks.ccl2.TwoLocalSwapNetwork` |
| Data Encoding | `pennylane.templates.embeddings.amplitude.AmplitudeEmbedding`, `pennylane.templates.embeddings.angle.AngleEmbedding`, `pennylane.templates.embeddings.basis.BasisEmbedding` (+6 more) |
| Grover | `pennylane.templates.subroutines.grover.GroverOperator`, `pennylane.templates.subroutines.reflection.Reflection` |
| Hamiltonian Simulation | `pennylane.templates.subroutines.approx_time_evolution.ApproxTimeEvolution`, `pennylane.templates.subroutines.commuting_evolution.CommutingEvolution`, `pennylane.templates.subroutines.qdrift.QDrift` (+2 more) |
| Initialization | `pennylane.templates.state_preparations.arbitrary_state_preparation.ArbitraryStatePreparation`, `pennylane.templates.state_preparations.basis_qutrit.QutritBasisStatePreparation`, `pennylane.templates.state_preparations.cosine_window.CosineWindow` (+1 more) |
| Linear Combination of Unitaries (LCU) | `pennylane.templates.subroutines.fable.FABLE` |
| Oracle | `pennylane.templates.subroutines.gqsp.GQSP`, `pennylane.templates.subroutines.qubitization.Qubitization`, `pennylane.templates.subroutines.select.Select` (+1 more) |
| Phase Shift | `pennylane.templates.subroutines.flip_sign.FlipSign` |
| Quantum Amplitude Estimation (QAE) | `pennylane.templates.subroutines.qmc.QuantumMonteCarlo` |
| Quantum Approximate Optimization Algorithm (QAOA) | `pennylane.templates.embeddings.qaoaembedding.QAOAEmbedding` |
| Quantum Arithmetic | `pennylane.templates.subroutines.adder.Adder`, `pennylane.templates.subroutines.mod_exp.ModExp`, `pennylane.templates.subroutines.multiplier.Multiplier` (+6 more) |
| Quantum Neural Network (QNN) | `pennylane.templates.layers.cv_neural_net.CVNeuralNetLayers`, `pennylane.templates.subroutines.interferometer.Interferometer`, `pennylane.templates.tensornetworks.mera.MERA` (+2 more) |
| Quantum Phase Estimation (QPE) | `pennylane.templates.subroutines.controlled_sequence.ControlledSequence`, `pennylane.templates.subroutines.qpe.QuantumPhaseEstimation` |
| Quantum Singular Value Transformation (QSVT) | `pennylane.templates.subroutines.qsvt.QSVT` |
| SWAP Test | `pennylane.templates.subroutines.hilbert_schmidt.HilbertSchmidt`, `pennylane.templates.subroutines.hilbert_schmidt.LocalHilbertSchmidt` |
| Schmidt Decomposition | `pennylane.templates.state_preparations.mottonen.MottonenStatePreparation`, `pennylane.templates.subroutines.arbitrary_unitary.ArbitraryUnitary` |
| Variational Quantum Algorithm (VQA) | `pennylane.templates.layers.basic_entangler.BasicEntanglerLayers`, `pennylane.templates.layers.gate_fabric.GateFabric`, `pennylane.templates.layers.random.RandomLayers` (+2 more) |
| Variational Quantum Eigensolver (VQE) | `pennylane.templates.layers.particle_conserving_u1.ParticleConservingU1`, `pennylane.templates.layers.particle_conserving_u2.ParticleConservingU2`, `pennylane.templates.subroutines.all_singles_doubles.AllSinglesDoubles` (+4 more) |

#### Qiskit Patterns

| Pattern | Concepts |
|---------|----------|
| Basis Change | `basis_change.qft.QFT`, `basis_change.qft.QFTGate`, `data_preparation.state_preparation.UniformSuperpositionGate` |
| Circuit Construction Utility | `blueprintcircuit.BlueprintCircuit`, `generalized_gates.diagonal.Diagonal`, `generalized_gates.diagonal.DiagonalGate` (+23 more) |
| Data Encoding | `data_preparation.pauli_feature_map.PauliFeatureMap`, `data_preparation.pauli_feature_map.z_feature_map`, `data_preparation.pauli_feature_map.zz_feature_map` |
| Grover | `grover_operator.GroverOperator` |
| Hamiltonian Simulation | `hamiltonian_gate.HamiltonianGate`, `pauli_evolution.PauliEvolutionGate` |
| Initialization | `data_preparation.initializer.Initialize`, `data_preparation.state_preparation.StatePreparation`, `graph_state.GraphState` (+1 more) |
| Oracle | `bit_flip_oracle.BitFlipOracleGate`, `fourier_checking.FourierChecking`, `hidden_linear_function.HiddenLinearFunction` (+2 more) |
| Quantum Approximate Optimization Algorithm (QAOA) | `n_local.qaoa_ansatz.QAOAAnsatz` |
| Quantum Arithmetic | `arithmetic.adders.adder.Adder`, `arithmetic.adders.adder.FullAdderGate`, `arithmetic.adders.adder.HalfAdderGate` (+23 more) |
| Quantum Logical Operators | `boolean_logic.quantum_and.AND`, `boolean_logic.quantum_and.AndGate`, `boolean_logic.quantum_or.OR` (+2 more) |
| Quantum Phase Estimation (QPE) | `phase_estimation.PhaseEstimation` |
| Variational Quantum Algorithm (VQA) | `n_local.efficient_su2.EfficientSU2`, `n_local.evolved_operator_ansatz.EvolvedOperatorAnsatz`, `n_local.excitation_preserving.ExcitationPreserving` (+4 more) |
| Variational Quantum Eigensolver (VQE) | `n_local.evolved_operator_ansatz.hamiltonian_variational_ansatz` |

### Missing Patterns

The following 44 patterns from the base list were not found in any of the three frameworks:

- Ad-hoc Hybrid Code Execution
- Alternating Operator Ansatz (AOA)
- Amplitude Encoding
- Angle Encoding
- Basis Encoding
- Biased Initial State
- Chained Optimization
- Circuit Cutting
- Classical-Quantum Interface
- Error Correction
- Gate Cut
- Gate Error Mitigation
- Hadamard Test
- Hybrid Module
- Matrix Encoding
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
- Quantum Fourier Transformation
- Quantum Hardware Selection
- Quantum Kernel Estimator (QKE)
- Quantum Module
- Quantum Module Template
- Quantum Random Access Memory (QRAM) Encoding
- Quantum-Classic Split
- Readout Error Mitigation
- Speedup via Verifying
- Standalone Circuit Execution
- Uncompute
- Unified Execution
- Unified Observability
- Uniform Superposition
- Variational Parameter Transfer
- Warm Start
- Wire Cut

### New Patterns Created

The following 13 patterns were found in the frameworks but are not in the base list:

#### Basis Change

**Observed in:**

- **Classiq**: 8 concepts
  - `open_library.functions.discrete_sine_cosine_transform.qct_qst_type1`
  - `open_library.functions.discrete_sine_cosine_transform.qct_qst_type2`
  - `open_library.functions.discrete_sine_cosine_transform.qct_type2`
  - `open_library.functions.discrete_sine_cosine_transform.qst_type2`
  - `open_library.functions.qaoa_penalty.qaoa_init`
  - `open_library.functions.qft_functions.qft`
  - `open_library.functions.qft_functions.qft_no_swap`
  - `open_library.functions.utility_functions.hadamard_transform`
- **PennyLane**: 3 concepts
  - `pennylane.templates.state_preparations.superposition.Superposition`
  - `pennylane.templates.subroutines.aqft.AQFT`
  - `pennylane.templates.subroutines.qft.QFT`
- **Qiskit**: 3 concepts
  - `basis_change.qft.QFT`
  - `basis_change.qft.QFTGate`
  - `data_preparation.state_preparation.UniformSuperpositionGate`

#### Circuit Construction Utility

**Observed in:**

- **Classiq**: 2 concepts
  - `open_library.functions.modular_exponentiation.multiswap`
  - `open_library.functions.utility_functions.apply_to_all`
- **PennyLane**: 3 concepts
  - `pennylane.templates.subroutines.basis_rotation.BasisRotation`
  - `pennylane.templates.subroutines.permute.Permute`
  - `pennylane.templates.swapnetworks.ccl2.TwoLocalSwapNetwork`
- **Qiskit**: 26 concepts
  - `blueprintcircuit.BlueprintCircuit`
  - `generalized_gates.diagonal.Diagonal`
  - `generalized_gates.diagonal.DiagonalGate`
  - `generalized_gates.gms.GMS`
  - `generalized_gates.gms.MSGate`
  - `generalized_gates.gr.GR`
  - `generalized_gates.gr.GRX`
  - `generalized_gates.gr.GRY`
  - `generalized_gates.gr.GRZ`
  - `generalized_gates.isometry.Isometry`
  - `generalized_gates.linear_function.LinearFunction`
  - `generalized_gates.mcg_up_to_diagonal.MCGupDiag`
  - `generalized_gates.mcmt.MCMTGate`
  - `generalized_gates.mcmt.MCMTVChain`
  - `generalized_gates.pauli.PauliGate`
  - `generalized_gates.permutation.Permutation`
  - `generalized_gates.permutation.PermutationGate`
  - `generalized_gates.rv.RVGate`
  - `generalized_gates.uc.UCGate`
  - `generalized_gates.uc_pauli_rot.UCPauliRotGate`
  - `generalized_gates.ucrz.UCRZGate`
  - `generalized_gates.unitary.UnitaryGate`
  - `iqp.IQP`
  - `iqp.random_iqp`
  - `overlap.UnitaryOverlap`
  - `quantum_volume.QuantumVolume`

#### Controlled Linear Rotation

**Observed in:**

- **Classiq**: 1 concepts
  - `open_library.functions.linear_pauli_rotation.linear_pauli_rotations`

#### Data Encoding

**Observed in:**

- **Classiq**: 6 concepts
  - `open_library.functions.state_preparation.inplace_prepare_complex_amplitudes`
  - `open_library.functions.state_preparation.prepare_complex_amplitudes`
  - `open_library.functions.state_preparation.prepare_exponential_state`
  - `open_library.functions.state_preparation.prepare_linear_amplitudes`
  - `open_library.functions.variational.encode_in_angle`
  - `open_library.functions.variational.encode_on_bloch`
- **PennyLane**: 9 concepts
  - `pennylane.templates.embeddings.amplitude.AmplitudeEmbedding`
  - `pennylane.templates.embeddings.angle.AngleEmbedding`
  - `pennylane.templates.embeddings.basis.BasisEmbedding`
  - `pennylane.templates.embeddings.displacement.DisplacementEmbedding`
  - `pennylane.templates.embeddings.iqp.IQPEmbedding`
  - `pennylane.templates.embeddings.squeezing.SqueezingEmbedding`
  - `pennylane.templates.state_preparations.qrom_state_prep.QROMStatePreparation`
  - `pennylane.templates.subroutines.prepselprep.PrepSelPrep`
  - `pennylane.templates.subroutines.qrom.QROM`
- **Qiskit**: 3 concepts
  - `data_preparation.pauli_feature_map.PauliFeatureMap`
  - `data_preparation.pauli_feature_map.z_feature_map`
  - `data_preparation.pauli_feature_map.zz_feature_map`

#### Hamiltonian Simulation

**Observed in:**

- **Classiq**: 1 concepts
  - `qmod.builtins.functions.exponentiation.suzuki_trotter`
- **PennyLane**: 5 concepts
  - `pennylane.templates.subroutines.approx_time_evolution.ApproxTimeEvolution`
  - `pennylane.templates.subroutines.commuting_evolution.CommutingEvolution`
  - `pennylane.templates.subroutines.qdrift.QDrift`
  - `pennylane.templates.subroutines.trotter.TrotterProduct`
  - `pennylane.templates.subroutines.trotter.TrotterizedQfunc`
- **Qiskit**: 2 concepts
  - `hamiltonian_gate.HamiltonianGate`
  - `pauli_evolution.PauliEvolutionGate`

#### Linear Combination of Unitaries

**Observed in:**

- **Classiq**: 2 concepts
  - `open_library.functions.lcu.lcu`
  - `open_library.functions.lcu.lcu_pauli`

#### Linear Combination of Unitaries (LCU)

**Observed in:**

- **PennyLane**: 1 concepts
  - `pennylane.templates.subroutines.fable.FABLE`

#### Quantum Amplitude Estimation

**Observed in:**

- **Classiq**: 1 concepts
  - `open_library.functions.amplitude_estimation.amplitude_estimation`

#### Quantum Amplitude Estimation (QAE)

**Observed in:**

- **PennyLane**: 1 concepts
  - `pennylane.templates.subroutines.qmc.QuantumMonteCarlo`

#### Quantum Arithmetic

**Observed in:**

- **Classiq**: 6 concepts
  - `open_library.functions.modular_exponentiation.c_modular_multiply`
  - `open_library.functions.modular_exponentiation.cc_modular_add`
  - `open_library.functions.modular_exponentiation.inplace_c_modular_multiply`
  - `open_library.functions.modular_exponentiation.modular_exp`
  - `open_library.functions.modular_exponentiation.qft_space_add_const`
  - `open_library.functions.utility_functions.modular_increment`
- **PennyLane**: 9 concepts
  - `pennylane.templates.subroutines.adder.Adder`
  - `pennylane.templates.subroutines.mod_exp.ModExp`
  - `pennylane.templates.subroutines.multiplier.Multiplier`
  - `pennylane.templates.subroutines.out_adder.OutAdder`
  - `pennylane.templates.subroutines.out_multiplier.OutMultiplier`
  - `pennylane.templates.subroutines.out_poly.OutPoly`
  - `pennylane.templates.subroutines.phase_adder.PhaseAdder`
  - `pennylane.templates.subroutines.semi_adder.SemiAdder`
  - `pennylane.templates.subroutines.temporary_and.TemporaryAND`
- **Qiskit**: 26 concepts
  - `arithmetic.adders.adder.Adder`
  - `arithmetic.adders.adder.FullAdderGate`
  - `arithmetic.adders.adder.HalfAdderGate`
  - `arithmetic.adders.adder.ModularAdderGate`
  - `arithmetic.adders.cdkm_ripple_carry_adder.CDKMRippleCarryAdder`
  - `arithmetic.adders.draper_qft_adder.DraperQFTAdder`
  - `arithmetic.adders.vbe_ripple_carry_adder.VBERippleCarryAdder`
  - `arithmetic.exact_reciprocal.ExactReciprocal`
  - `arithmetic.exact_reciprocal.ExactReciprocalGate`
  - `arithmetic.functional_pauli_rotations.FunctionalPauliRotations`
  - `arithmetic.integer_comparator.IntegerComparator`
  - `arithmetic.integer_comparator.IntegerComparatorGate`
  - `arithmetic.linear_amplitude_function.LinearAmplitudeFunctionGate`
  - `arithmetic.linear_pauli_rotations.LinearPauliRotationsGate`
  - `arithmetic.multipliers.hrs_cumulative_multiplier.HRSCumulativeMultiplier`
  - `arithmetic.multipliers.multiplier.MultiplierGate`
  - `arithmetic.multipliers.rg_qft_multiplier.RGQFTMultiplier`
  - `arithmetic.piecewise_chebyshev.PiecewiseChebyshevGate`
  - `arithmetic.piecewise_linear_pauli_rotations.PiecewiseLinearPauliRotationsGate`
  - `arithmetic.piecewise_polynomial_pauli_rotations.PiecewisePolynomialPauliRotationsGate`
  - `arithmetic.polynomial_pauli_rotations.PolynomialPauliRotations`
  - `arithmetic.polynomial_pauli_rotations.PolynomialPauliRotationsGate`
  - `arithmetic.quadratic_form.QuadraticFormGate`
  - `arithmetic.weighted_adder.WeightedAdder`
  - `arithmetic.weighted_adder.WeightedSumGate`
  - `boolean_logic.inner_product.InnerProductGate`

#### Quantum Logical Operators

**Observed in:**

- **Qiskit**: 5 concepts
  - `boolean_logic.quantum_and.AND`
  - `boolean_logic.quantum_and.AndGate`
  - `boolean_logic.quantum_or.OR`
  - `boolean_logic.quantum_xor.BitwiseXorGate`
  - `boolean_logic.quantum_xor.random_bitwise_xor`

#### Quantum Singular Value Transformation

**Observed in:**

- **Classiq**: 5 concepts
  - `open_library.functions.qsvt.qsvt`
  - `open_library.functions.qsvt.qsvt_inversion`
  - `open_library.functions.qsvt.qsvt_lcu`
  - `open_library.functions.qsvt.qsvt_lcu_step`
  - `open_library.functions.qsvt.qsvt_step`

#### Quantum Singular Value Transformation (QSVT)

**Observed in:**

- **PennyLane**: 1 concepts
  - `pennylane.templates.subroutines.qsvt.QSVT`

## Qiskit Concepts

| Concept Name | Summary |
|--------------|---------|
| `/qiskit/qiskit.circuit.library.arithmetic.adders.adder.Adder` | Compute the sum of two equally sized qubit registers. |
| `/qiskit/qiskit.circuit.library.arithmetic.adders.adder.HalfAdderGate` | Compute the sum of two equally-sized qubit registers, including a carry-out bit. |
| `/qiskit/qiskit.circuit.library.arithmetic.adders.adder.ModularAdderGate` | Compute the sum modulo :math:`2^n` of two :math:`n`-sized qubit registers. |
| `/qiskit/qiskit.circuit.library.arithmetic.adders.adder.FullAdderGate` | Compute the sum of two :math:`n`-sized qubit registers, including carry-in and -out bits. |
| `/qiskit/qiskit.circuit.library.arithmetic.adders.cdkm_ripple_carry_adder.CDKMRippleCarryAdder` | A ripple-carry circuit to perform in-place addition on two qubit registers. |
| `/qiskit/qiskit.circuit.library.arithmetic.adders.draper_qft_adder.DraperQFTAdder` | A circuit that uses QFT to perform in-place addition on two qubit registers. |
| `/qiskit/qiskit.circuit.library.arithmetic.adders.vbe_ripple_carry_adder.VBERippleCarryAdder` | The VBE ripple carry adder [1]. |
| `/qiskit/qiskit.circuit.library.arithmetic.exact_reciprocal.ExactReciprocal` | Exact reciprocal |
| `/qiskit/qiskit.circuit.library.arithmetic.exact_reciprocal.ExactReciprocalGate` | Implements an exact reciprocal function. |
| `/qiskit/qiskit.circuit.library.arithmetic.functional_pauli_rotations.FunctionalPauliRotations` | Base class for functional Pauli rotations. |
| `/qiskit/qiskit.circuit.library.arithmetic.integer_comparator.IntegerComparator` | Integer Comparator. |
| `/qiskit/qiskit.circuit.library.arithmetic.integer_comparator.IntegerComparatorGate` | Perform a :math:`\geq` (or :math:`<`) on a qubit register against a classical integer. |
| `/qiskit/qiskit.circuit.library.arithmetic.linear_amplitude_function.LinearAmplitudeFunctionGate` | A circuit implementing a (piecewise) linear function on qubit amplitudes. |
| `/qiskit/qiskit.circuit.library.arithmetic.linear_pauli_rotations.LinearPauliRotationsGate` | Linearly-controlled X, Y or Z rotation. |
| `/qiskit/qiskit.circuit.library.arithmetic.multipliers.hrs_cumulative_multiplier.HRSCumulativeMultiplier` | A multiplication circuit to store product of two input registers out-of-place. |
| `/qiskit/qiskit.circuit.library.arithmetic.multipliers.multiplier.MultiplierGate` | Compute the product of two equally sized qubit registers into a new register. |
| `/qiskit/qiskit.circuit.library.arithmetic.multipliers.rg_qft_multiplier.RGQFTMultiplier` | A QFT multiplication circuit to store product of two input registers out-of-place. |
| `/qiskit/qiskit.circuit.library.arithmetic.piecewise_chebyshev.PiecewiseChebyshevGate` | Piecewise Chebyshev approximation to an input function. |
| `/qiskit/qiskit.circuit.library.arithmetic.piecewise_linear_pauli_rotations.PiecewiseLinearPauliRotationsGate` | Piecewise-linearly-controlled Pauli rotations. |
| `/qiskit/qiskit.circuit.library.arithmetic.piecewise_polynomial_pauli_rotations.PiecewisePolynomialPauliRotationsGate` | Piecewise-polynomially-controlled Pauli rotations. |
| `/qiskit/qiskit.circuit.library.arithmetic.polynomial_pauli_rotations.PolynomialPauliRotations` | A circuit implementing polynomial Pauli rotations. |
| `/qiskit/qiskit.circuit.library.arithmetic.polynomial_pauli_rotations.PolynomialPauliRotationsGate` | A gate implementing polynomial Pauli rotations. |
| `/qiskit/qiskit.circuit.library.arithmetic.quadratic_form.QuadraticFormGate` | Implements a quadratic form on binary variables encoded in qubit registers. |
| `/qiskit/qiskit.circuit.library.arithmetic.weighted_adder.WeightedAdder` | A circuit to compute the weighted sum of qubit registers. |
| `/qiskit/qiskit.circuit.library.arithmetic.weighted_adder.WeightedSumGate` | A gate to compute the weighted sum of qubit registers. |
| `/qiskit/qiskit.circuit.library.basis_change.qft.QFT` | Quantum Fourier Transform Circuit. |
| `/qiskit/qiskit.circuit.library.basis_change.qft.QFTGate` | Quantum Fourier Transform Gate. |
| `/qiskit/qiskit.circuit.library.bit_flip_oracle.BitFlipOracleGate` | Implements a bit-flip oracle |
| `/qiskit/qiskit.circuit.library.blueprintcircuit.BlueprintCircuit` | Blueprint circuit object. |
| `/qiskit/qiskit.circuit.library.boolean_logic.inner_product.InnerProductGate` | A 2n-qubit Boolean function that computes the inner product of two n-qubit vectors over :math:`F_2`. |
| `/qiskit/qiskit.circuit.library.boolean_logic.quantum_and.AND` | A circuit implementing the logical AND operation on a number of qubits. |
| `/qiskit/qiskit.circuit.library.boolean_logic.quantum_and.AndGate` | A gate representing the logical AND operation on a number of qubits. |
| `/qiskit/qiskit.circuit.library.boolean_logic.quantum_or.OR` | A circuit implementing the logical OR operation on a number of qubits. |
| `/qiskit/qiskit.circuit.library.boolean_logic.quantum_xor.BitwiseXorGate` | An n-qubit gate for bitwise xor-ing the input with some integer ``amount``. |
| `/qiskit/qiskit.circuit.library.boolean_logic.quantum_xor.random_bitwise_xor` | Create a random BitwiseXorGate. |
| `/qiskit/qiskit.circuit.library.data_preparation.pauli_feature_map.z_feature_map` | The first order Pauli Z-evolution circuit. |
| `/qiskit/qiskit.circuit.library.data_preparation.pauli_feature_map.zz_feature_map` | Second-order Pauli-Z evolution circuit. |
| `/qiskit/qiskit.circuit.library.data_preparation.initializer.Initialize` | Complex amplitude initialization. |
| `/qiskit/qiskit.circuit.library.data_preparation.pauli_feature_map.PauliFeatureMap` | The Pauli Expansion circuit. |
| `/qiskit/qiskit.circuit.library.data_preparation.pauli_feature_map.self_product` | Define a function map from R^n to R. |
| `/qiskit/qiskit.circuit.library.data_preparation.state_preparation.StatePreparation` | Complex amplitude state preparation. |
| `/qiskit/qiskit.circuit.library.data_preparation.state_preparation.UniformSuperpositionGate` | Implements a uniform superposition state. |
| `/qiskit/qiskit.circuit.library.fourier_checking.FourierChecking` | Fourier checking circuit. |
| `/qiskit/qiskit.circuit.library.generalized_gates.diagonal.Diagonal` | Circuit implementing a diagonal transformation. |
| `/qiskit/qiskit.circuit.library.generalized_gates.diagonal.DiagonalGate` | A generic diagonal quantum gate. |
| `/qiskit/qiskit.circuit.library.generalized_gates.gms.GMS` | Global Mølmer–Sørensen gate. |
| `/qiskit/qiskit.circuit.library.generalized_gates.gms.MSGate` | The Mølmer–Sørensen gate. |
| `/qiskit/qiskit.circuit.library.generalized_gates.gr.GR` | Global R gate. |
| `/qiskit/qiskit.circuit.library.generalized_gates.gr.GRX` | Global RX gate. |
| `/qiskit/qiskit.circuit.library.generalized_gates.gr.GRY` | Global RY gate. |
| `/qiskit/qiskit.circuit.library.generalized_gates.gr.GRZ` | Global RZ gate. |
| `/qiskit/qiskit.circuit.library.generalized_gates.isometry.Isometry` | Decomposition of arbitrary isometries from :math:`m` to :math:`n` qubits. |
| `/qiskit/qiskit.circuit.library.generalized_gates.linear_function.LinearFunction` | A linear reversible circuit on n qubits. |
| `/qiskit/qiskit.circuit.library.generalized_gates.mcg_up_to_diagonal.MCGupDiag` | Decomposes a multi-controlled gate :math:`U` up to a diagonal :math:`D` acting on the control and target qubit (but not on the ancilla qubits), i.e., it implements a circuit corresponding to a unitary :math:`U'`, such that :math:`U = D U'`. |
| `/qiskit/qiskit.circuit.library.generalized_gates.mcmt.MCMTGate` | The multi-controlled multi-target gate, for an arbitrary singly controlled target gate. |
| `/qiskit/qiskit.circuit.library.generalized_gates.mcmt.MCMTVChain` | The MCMT implementation using the CCX V-chain. |
| `/qiskit/qiskit.circuit.library.generalized_gates.pauli.PauliGate` | A multi-qubit Pauli gate. |
| `/qiskit/qiskit.circuit.library.generalized_gates.permutation.Permutation` | An n_qubit circuit that permutes qubits. |
| `/qiskit/qiskit.circuit.library.generalized_gates.permutation.PermutationGate` | A gate that permutes qubits. |
| `/qiskit/qiskit.circuit.library.generalized_gates.rv.RVGate` | Rotation around arbitrary rotation axis :math:`\vec{v}` where :math:`\\|\vec{v}\\|_2` is angle of rotation in radians. |
| `/qiskit/qiskit.circuit.library.generalized_gates.uc.UCGate` | Uniformly controlled gate (also called multiplexed gate). |
| `/qiskit/qiskit.circuit.library.generalized_gates.uc_pauli_rot.UCPauliRotGate` | Uniformly controlled Pauli rotations. |
| `/qiskit/qiskit.circuit.library.generalized_gates.ucrz.UCRZGate` | Uniformly controlled Pauli-Z rotations. |
| `/qiskit/qiskit.circuit.library.generalized_gates.unitary.UnitaryGate` | Class quantum gates specified by a unitary matrix. |
| `/qiskit/qiskit.circuit.library.graph_state.GraphState` | Circuit to prepare a graph state. |
| `/qiskit/qiskit.circuit.library.graph_state.GraphStateGate` | A gate representing a graph state. |
| `/qiskit/qiskit.circuit.library.grover_operator.GroverOperator` | The Grover operator. |
| `/qiskit/qiskit.circuit.library.hamiltonian_gate.HamiltonianGate` | Class for representing evolution by a Hamiltonian operator as a gate. |
| `/qiskit/qiskit.circuit.library.hidden_linear_function.HiddenLinearFunction` | Circuit to solve the hidden linear function problem. |
| `/qiskit/qiskit.circuit.library.iqp.IQP` | Instantaneous quantum polynomial (IQP) circuit. |
| `/qiskit/qiskit.circuit.library.iqp.random_iqp` | A random instantaneous quantum polynomial time (IQP) circuit. |
| `/qiskit/qiskit.circuit.library.n_local.efficient_su2.EfficientSU2` | The hardware efficient SU(2) 2-local circuit. |
| `/qiskit/qiskit.circuit.library.n_local.evolved_operator_ansatz.hamiltonian_variational_ansatz` | Construct a Hamiltonian variational ansatz. |
| `/qiskit/qiskit.circuit.library.n_local.evolved_operator_ansatz.EvolvedOperatorAnsatz` | The evolved operator ansatz. |
| `/qiskit/qiskit.circuit.library.n_local.excitation_preserving.ExcitationPreserving` | The heuristic excitation-preserving wave function ansatz. |
| `/qiskit/qiskit.circuit.library.n_local.n_local.NLocal` | The n-local circuit class. |
| `/qiskit/qiskit.circuit.library.n_local.pauli_two_design.PauliTwoDesign` | The Pauli Two-Design ansatz. |
| `/qiskit/qiskit.circuit.library.n_local.qaoa_ansatz.QAOAAnsatz` | A generalized QAOA quantum circuit with a support of custom initial states and mixers. |
| `/qiskit/qiskit.circuit.library.n_local.real_amplitudes.RealAmplitudes` | The real-amplitudes 2-local circuit. |
| `/qiskit/qiskit.circuit.library.n_local.two_local.TwoLocal` | The two-local circuit. |
| `/qiskit/qiskit.circuit.library.overlap.UnitaryOverlap` | Circuit that returns the overlap between two unitaries :math:`U_2^{\dag} U_1`. |
| `/qiskit/qiskit.circuit.library.pauli_evolution.PauliEvolutionGate` | Time-evolution of an operator consisting of Paulis. |
| `/qiskit/qiskit.circuit.library.phase_estimation.PhaseEstimation` | Phase Estimation circuit. |
| `/qiskit/qiskit.circuit.library.phase_oracle.PhaseOracle` | Phase Oracle. |
| `/qiskit/qiskit.circuit.library.phase_oracle.PhaseOracleGate` | Implements a phase oracle. |
| `/qiskit/qiskit.circuit.library.quantum_volume.QuantumVolume` | A quantum volume model circuit. |

## PennyLane Concepts

| Concept Name | Summary |
|--------------|---------|
| `/pennylane/pennylane.templates.embeddings.amplitude.AmplitudeEmbedding` | Encodes :math:`2^n` features into the amplitude vector of :math:`n` qubits. |
| `/pennylane/pennylane.templates.embeddings.angle.AngleEmbedding` | Encodes :math:`N` features into the rotation angles of :math:`n` qubits, where :math:`N \leq n`. |
| `/pennylane/pennylane.templates.embeddings.basis.BasisEmbedding` | Encodes :math:`n` binary features into a basis state of :math:`n` qubits. |
| `/pennylane/pennylane.templates.embeddings.displacement.DisplacementEmbedding` | Encodes :math:`N` features into the displacement amplitudes :math:`r` or phases :math:`\phi` of :math:`M` modes, where :math:`N\leq M`. |
| `/pennylane/pennylane.templates.embeddings.iqp.IQPEmbedding` | Encodes :math:`n` features into :math:`n` qubits using diagonal gates of an IQP circuit. |
| `/pennylane/pennylane.templates.embeddings.qaoaembedding.QAOAEmbedding` | Encodes :math:`N` features into :math:`n>N` qubits, using a layered, trainable quantum circuit that is inspired by the QAOA ansatz proposed by `Killoran et al. (2020) <https://arxiv.org/abs/2001.03622>`_. |
| `/pennylane/pennylane.templates.embeddings.squeezing.SqueezingEmbedding` | Encodes :math:`N` features into the squeezing amplitudes :math:`r \geq 0` or phases :math:`\phi \in [0, 2\pi)` of :math:`M` modes, where :math:`N\leq M`. |
| `/pennylane/pennylane.templates.layers.basic_entangler.BasicEntanglerLayers` | Layers consisting of one-parameter single-qubit rotations on each qubit, followed by a closed chain or *ring* of CNOT gates. |
| `/pennylane/pennylane.templates.layers.cv_neural_net.CVNeuralNetLayers` | A sequence of layers of a continuous-variable quantum neural network, as specified in `Killoran et al. (2019) <https://doi.org/10.1103/PhysRevResearch.1.033063>`_. |
| `/pennylane/pennylane.templates.layers.gate_fabric.GateFabric` | Implements a local, expressive, and quantum-number-preserving ansatz proposed by `Anselmetti et al. (2021) <https://doi.org/10.1088/1367-2630/ac2cb3>`_. |
| `/pennylane/pennylane.templates.layers.particle_conserving_u1.ParticleConservingU1` | Implements the heuristic VQE ansatz for quantum chemistry simulations using the particle-conserving gate :math:`U_{1,\mathrm{ex}}` proposed by Barkoutsos *et al.* in `arXiv:1805.04340 <https://arxiv.org/abs/1805.04340>`_. |
| `/pennylane/pennylane.templates.layers.particle_conserving_u2.ParticleConservingU2` | Implements the heuristic VQE ansatz for Quantum Chemistry simulations using the particle-conserving entangler :math:`U_\mathrm{ent}(\vec{\theta}, \vec{\phi})` proposed in `arXiv:1805.04340 <https://arxiv.org/abs/1805.04340>`__. |
| `/pennylane/pennylane.templates.layers.random.RandomLayers` | Layers of randomly chosen single qubit rotations and 2-qubit entangling gates, acting on randomly chosen qubits. |
| `/pennylane/pennylane.templates.layers.simplified_two_design.SimplifiedTwoDesign` | Layers consisting of a simplified 2-design architecture of Pauli-Y rotations and controlled-Z entanglers proposed in `Cerezo et al. (2021) <https://doi.org/10.1038/s41467-021-21728-w>`_. |
| `/pennylane/pennylane.templates.layers.strongly_entangling.StronglyEntanglingLayers` | Layers consisting of single qubit rotations and entanglers, inspired by the circuit-centric classifier design `arXiv:1804.00633 <https://arxiv.org/abs/1804.00633>`_. |
| `/pennylane/pennylane.templates.state_preparations.arbitrary_state_preparation.ArbitraryStatePreparation` | Implements an arbitrary state preparation on the specified wires. |
| `/pennylane/pennylane.templates.state_preparations.basis_qutrit.QutritBasisStatePreparation` | Prepares a basis state on the given wires using a sequence of TShift gates. |
| `/pennylane/pennylane.templates.state_preparations.cosine_window.CosineWindow` | CosineWindow(wires) Prepares an initial state with a cosine wave function. |
| `/pennylane/pennylane.templates.state_preparations.mottonen.MottonenStatePreparation` | Prepares an arbitrary state on the given wires using a decomposition into gates developed by `Möttönen et al. (2004) <https://arxiv.org/abs/quant-ph/0407010>`_. |
| `/pennylane/pennylane.templates.state_preparations.qrom_state_prep.QROMStatePreparation` | Prepares a quantum state using Quantum Read-Only Memory (QROM). |
| `/pennylane/pennylane.templates.state_preparations.state_prep_mps.MPSPrep` | Prepares an initial state from a matrix product state (MPS) representation. |
| `/pennylane/pennylane.templates.state_preparations.superposition.Superposition` | Prepare a superposition of computational basis states. |
| `/pennylane/pennylane.templates.subroutines.amplitude_amplification.AmplitudeAmplification` | Applies amplitude amplification. |
| `/pennylane/pennylane.templates.subroutines.aqft.AQFT` | AQFT(order, wires) Apply an approximate quantum Fourier transform (AQFT). |
| `/pennylane/pennylane.templates.subroutines.arbitrary_unitary.ArbitraryUnitary` | Implements an arbitrary unitary on the specified wires. |
| `/pennylane/pennylane.templates.subroutines.arithmetic.adder.Adder` | Performs the in-place modular addition operation. |
| `/pennylane/pennylane.templates.subroutines.arithmetic.mod_exp.ModExp` | Performs the out-place modular exponentiation operation. |
| `/pennylane/pennylane.templates.subroutines.arithmetic.multiplier.Multiplier` | Performs the in-place modular multiplication operation. |
| `/pennylane/pennylane.templates.subroutines.arithmetic.out_adder.OutAdder` | Performs the out-place modular addition operation. |
| `/pennylane/pennylane.templates.subroutines.arithmetic.out_multiplier.OutMultiplier` | Performs the out-place modular multiplication operation. |
| `/pennylane/pennylane.templates.subroutines.arithmetic.out_poly.OutPoly` | Performs the out-of-place polynomial operation. |
| `/pennylane/pennylane.templates.subroutines.arithmetic.phase_adder.PhaseAdder` | Performs the in-place modular phase addition operation. |
| `/pennylane/pennylane.templates.subroutines.arithmetic.semi_adder.SemiAdder` | This operator performs the plain addition of two integers :math:`x` and :math:`y` in the computational basis: |
| `/pennylane/pennylane.templates.subroutines.arithmetic.temporary_and.TemporaryAND` | TemporaryAND(wires, control_values) |
| `/pennylane/pennylane.templates.subroutines.controlled_sequence.ControlledSequence` | Creates a sequence of controlled gates raised to decreasing powers of 2. Can be used as a sub-block in building a `quantum phase estimation <https://en.wikipedia.org/wiki/Quantum_phase_estimation_algorithm>`__ circuit. |
| `/pennylane/pennylane.templates.subroutines.fable.FABLE` | Construct a unitary with the fast approximate block encoding method. |
| `/pennylane/pennylane.templates.subroutines.flip_sign.FlipSign` | Flips the sign of a given basis state. |
| `/pennylane/pennylane.templates.subroutines.gqsp.GQSP` | Implements the generalized quantum signal processing (GQSP) circuit. |
| `/pennylane/pennylane.templates.subroutines.grover.GroverOperator` | Performs the Grover Diffusion Operator. |
| `/pennylane/pennylane.templates.subroutines.hilbert_schmidt.HilbertSchmidt` | Create a Hilbert-Schmidt template that can be used to compute the Hilbert-Schmidt Test (HST). |
| `/pennylane/pennylane.templates.subroutines.hilbert_schmidt.LocalHilbertSchmidt` | Create a Local Hilbert-Schmidt template that can be used to compute the Local Hilbert-Schmidt Test (LHST). |
| `/pennylane/pennylane.templates.subroutines.interferometer.Interferometer` | General linear interferometer, an array of beamsplitters and phase shifters. |
| `/pennylane/pennylane.templates.subroutines.permute.Permute` | Applies a permutation to a set of wires. |
| `/pennylane/pennylane.templates.subroutines.prepselprep.PrepSelPrep` | Implements a block-encoding of a linear combination of unitaries. |
| `/pennylane/pennylane.templates.subroutines.qchem.all_singles_doubles.AllSinglesDoubles` | Builds a quantum circuit to prepare correlated states of molecules by applying all :class:`~.pennylane.SingleExcitation` and :class:`~.pennylane.DoubleExcitation` operations to the initial Hartree-Fock state. |
| `/pennylane/pennylane.templates.subroutines.qchem.basis_rotation.BasisRotation` | Implements a circuit that performs an exact single-body basis rotation using Givens rotations and phase shifts. |
| `/pennylane/pennylane.templates.subroutines.qchem.fermionic_double_excitation.FermionicDoubleExcitation` | Circuit to exponentiate the tensor product of Pauli matrices representing the double-excitation operator entering the Unitary Coupled-Cluster Singles and Doubles (UCCSD) ansatz. UCCSD is a VQE ansatz commonly used to run quantum chemistry simulations. |
| `/pennylane/pennylane.templates.subroutines.qchem.fermionic_single_excitation.FermionicSingleExcitation` | Circuit to exponentiate the tensor product of Pauli matrices representing the single-excitation operator entering the Unitary Coupled-Cluster Singles and Doubles (UCCSD) ansatz. UCCSD is a VQE ansatz commonly used to run quantum chemistry simulations. |
| `/pennylane/pennylane.templates.subroutines.qchem.kupccgsd.kUpCCGSD` | Implements the k-Unitary Pair Coupled-Cluster Generalized Singles and Doubles (k-UpCCGSD) ansatz. |
| `/pennylane/pennylane.templates.subroutines.qchem.uccsd.UCCSD` | Implements the Unitary Coupled-Cluster Singles and Doubles (UCCSD) ansatz. |
| `/pennylane/pennylane.templates.subroutines.qft.QFT` | QFT(wires) Apply a quantum Fourier transform (QFT). |
| `/pennylane/pennylane.templates.subroutines.qmc.QuantumMonteCarlo` | Performs the `quantum Monte Carlo estimation <https://arxiv.org/abs/1805.00109>`__ algorithm. |
| `/pennylane/pennylane.templates.subroutines.qpe.QuantumPhaseEstimation` | Performs the `quantum phase estimation <https://en.wikipedia.org/wiki/Quantum_phase_estimation_algorithm>`__ circuit. |
| `/pennylane/pennylane.templates.subroutines.qrom.QROM` | Applies the QROM operator. |
| `/pennylane/pennylane.templates.subroutines.qsvt.QSVT` | QSVT(UA,projectors) Implements the `quantum singular value transformation <https://arxiv.org/abs/1806.01838>`__ (QSVT) circuit. |
| `/pennylane/pennylane.templates.subroutines.qubitization.Qubitization` | Applies the `Qubitization <https://arxiv.org/abs/2204.11890>`__ operator. |
| `/pennylane/pennylane.templates.subroutines.reflection.Reflection` | Apply a reflection about a state :math:`\|\Psi\rangle`. |
| `/pennylane/pennylane.templates.subroutines.select.Select` | The ``Select`` operator, also known as multiplexer or multiplexed operation, applies different operations depending on the state of designated control wires. |
| `/pennylane/pennylane.templates.subroutines.select_pauli_rot.SelectPauliRot` | Applies individual single-qubit Pauli rotations depending on the state of designated control qubits. |
| `/pennylane/pennylane.templates.subroutines.time_evolution.approx_time_evolution.ApproxTimeEvolution` | Applies the Trotterized time-evolution operator for an arbitrary Hamiltonian, expressed in terms of Pauli gates. |
| `/pennylane/pennylane.templates.subroutines.time_evolution.commuting_evolution.CommutingEvolution` | Applies the time-evolution operator for a Hamiltonian expressed as a linear combination of mutually commuting Pauli words. |
| `/pennylane/pennylane.templates.subroutines.time_evolution.qdrift.QDrift` | An operation representing the QDrift approximation for the complex matrix exponential of a given Hamiltonian. |
| `/pennylane/pennylane.templates.subroutines.time_evolution.trotter.TrotterProduct` | An operation representing the Suzuki-Trotter product approximation for the complex matrix exponential of a given Hamiltonian. |
| `/pennylane/pennylane.templates.subroutines.time_evolution.trotter.TrotterizedQfunc` | An operation representing the Suzuki-Trotter product approximation applied to a set of operations defined in a function. |
| `/pennylane/pennylane.templates.swapnetworks.ccl2.TwoLocalSwapNetwork` | Apply two-local gate operations using a canonical 2-complete linear (2-CCL) swap network. |
| `/pennylane/pennylane.templates.tensornetworks.mera.MERA` | The MERA template broadcasts an input circuit across many wires following the architecture of a multi-scale entanglement renormalization ansatz tensor network. This architecture can be found in `arXiv:quant-ph/0610099 <https://arxiv.org/abs/quant-ph/0610099>`_ and closely resembles `quantum convolutional neural networks <https://arxiv.org/abs/1810.03787>`_. |
| `/pennylane/pennylane.templates.tensornetworks.mps.MPS` | The MPS template broadcasts an input circuit across many wires following the architecture of a Matrix Product State tensor network. The result is similar to the architecture in `arXiv:1803.11537 <https://arxiv.org/abs/1803.11537>`_. |
| `/pennylane/pennylane.templates.tensornetworks.ttn.TTN` | The TTN template broadcasts an input circuit across many wires following the architecture of a tree tensor network. The result is similar to the architecture in `arXiv:1803.11537 <https://arxiv.org/abs/1803.11537>`_. |

## Classiq Concepts

| Concept Name | Summary |
|--------------|---------|
| `/classiq/open_library.functions.amplitude_amplification.amplitude_amplification` | Applies the Amplitude Amplification algorithm; Prepares a state using the given `space_transform` function, and applies `reps` repetititions of the grover operator, using the given `oracle` functions which marks the "good" states. |
| `/classiq/open_library.functions.amplitude_amplification.exact_amplitude_amplification` | Applies an exact version of the Amplitude Amplification algorithm, assuming knowledge of the amplitude of the marked state. The function should be applied on the zero state, and it takes care for preparing the initial state before amplification using the `space_transform`. |
| `/classiq/open_library.functions.amplitude_estimation.amplitude_estimation` | Estimate the probability of a state being marked by the operand `oracle` as a "good state. ". |
| `/classiq/open_library.functions.discrete_sine_cosine_transform.qct_qst_type1` | Applies the quantum discrete cosine (DCT) and sine (DST) transform of type 1 to the qubit array `x`. Corresponds to the matrix (with $n\equiv$`x. |
| `/classiq/open_library.functions.discrete_sine_cosine_transform.qct_qst_type2` | Applies the quantum discrete cosine (DCT) and sine (DST) transform of type 2 to the qubit array `x` concatenated with `q`, with `q` being the MSB. Corresponds to the matrix (with $n\equiv$`x. |
| `/classiq/open_library.functions.discrete_sine_cosine_transform.qct_type2` | Applies the quantum discrete cosine (DCT) transform of type 2, ${ m DCT}^{(2)}$, to the qubit array `x`. |
| `/classiq/open_library.functions.discrete_sine_cosine_transform.qst_type2` | Applies the quantum discrete sine (DST) transform of type 2, ${ m DST}^{(2)}$, to the qubit array `x`. |
| `/classiq/open_library.functions.grover.phase_oracle` | Creates a phase oracle operator based on a predicate function. |
| `/classiq/open_library.functions.grover.reflect_about_zero` | Reflects the state about the \|0> state (i. e. |
| `/classiq/open_library.functions.grover.grover_diffuser` | Reflects the given state about the A\|0> state, where A is the `space_transform` parameter. It is defined as:. |
| `/classiq/open_library.functions.grover.grover_operator` | Applies the grover operator, defined by:. |
| `/classiq/open_library.functions.grover.grover_search` | Applies Grover search algorithm. |
| `/classiq/open_library.functions.hea.full_hea` | Implements an ansatz on a qubit array `x` with the given 1-qubit and 2-qubit operations. |
| `/classiq/open_library.functions.lcu.lcu` | Implements a general linear combination of unitaries (LCU) procedure. The algorithm prepares a superposition over the `unitaries` according to `magnitudes`, and then conditionally applies each unitary controlled by the `block`. |
| `/classiq/open_library.functions.lcu.lcu_pauli` | Applies a linear combination of unitaries (LCU) where each unitary is a Pauli term, represented as a tensor product of Pauli operators. The function prepares a superposition over the unitaries according to the given magnitudes and phases, and applies the corresponding Pauli operators conditionally. |
| `/classiq/open_library.functions.linear_pauli_rotation.linear_pauli_rotations` | Performs a rotation on a series of $m$ target qubits, where the rotation angle is a linear function of an $n$-qubit control register. |
| `/classiq/open_library.functions.lookup_table.span_lookup_table` | Applies a classical function to quantum numbers. |
| `/classiq/open_library.functions.modular_exponentiation.qft_space_add_const` | Adds a constant to a quantum number (in the Fourier space) using the Quantum Fourier Transform (QFT) Adder algorithm. Assuming that the input `phi_b` has `n` qubits, the result will be $\phi_b+=value \mod 2^n$. |
| `/classiq/open_library.functions.modular_exponentiation.cc_modular_add` | Adds a constant `a` to a quantum number `phi_b` modulo the constant `n`, controlled by 2 qubits. The quantum number `phi_b` and the constant `a` are assumed to be in the QFT space. |
| `/classiq/open_library.functions.modular_exponentiation.c_modular_multiply` | Performs out-of-place multiplication of a quantum number `x` by a classical number `a` modulo classical number `n`, controlled by a quantum bit `ctrl` and adds the result to a quantum array `b`. Applies $b += xa \mod n$ if `ctrl=1`, and the identity otherwise. |
| `/classiq/open_library.functions.modular_exponentiation.multiswap` | Swaps the qubit states between two arrays. Qubits of respective indices are swapped, and additional qubits in the longer array are left unchanged. |
| `/classiq/open_library.functions.modular_exponentiation.inplace_c_modular_multiply` | Performs multiplication of a quantum number `x` by a classical number `a` modulo classical number `n`, controlled by a quantum bit `ctrl`. Applies $x=xa \mod n$ if `ctrl=1`, and the identity otherwise. |
| `/classiq/open_library.functions.modular_exponentiation.modular_add_qft_space` | Adds a constant `a` to a quantum number `phi_b` modulo the constant `n`. The quantum number `phi_b` is assumed to be in the QFT space. |
| `/classiq/open_library.functions.modular_exponentiation.modular_multiply` | Performs out-of-place multiplication of a quantum number `x` by a classical number `a` modulo classical number `n`, and adds the result to a quantum array `b` (Applies $b += xa \mod n$). |
| `/classiq/open_library.functions.modular_exponentiation.inplace_modular_multiply` | Performs multiplication of a quantum number `x` by a classical number `a` modulo classical number `n` (Applies $x=xa \mod n$). |
| `/classiq/open_library.functions.modular_exponentiation.modular_exp` | Raises a classical integer `a` to the power of a quantum number `power` modulo classical integer `n` times a quantum number `x`. Performs $x=(a^{power} \mod n)*x$ in-place. |
| `/classiq/open_library.functions.qaoa_penalty.qaoa_mixer_layer` | Applies the mixer layer for the QAOA algorithm. The mixer layer is a sequence of `X` gates applied to each qubit in the target quantum array variable. |
| `/classiq/open_library.functions.qaoa_penalty.qaoa_cost_layer` | Applies the cost layer to the QAOA model. |
| `/classiq/open_library.functions.qaoa_penalty.qaoa_layer` | Applies the QAOA layer, which concatenates the cost layer and the mixer layer. |
| `/classiq/open_library.functions.qaoa_penalty.qaoa_init` | Initializes the QAOA circuit by applying the Hadamard gate to all qubits. |
| `/classiq/open_library.functions.qaoa_penalty.qaoa_penalty` | Applies the penalty layer to the QAOA model. |
| `/classiq/open_library.functions.qft_functions.qft_no_swap` | Applies the Quantum Fourier Transform (QFT) without the swap gates. |
| `/classiq/open_library.functions.qft_functions.qft` | Performs the Quantum Fourier Transform (QFT) on `target` in-place. Implements the following transformation:. |
| `/classiq/open_library.functions.qpe.qpe_flexible` | Implements the Quantum Phase Estimation (QPE) algorithm, which estimates the phase (eigenvalue) associated with an eigenstate of a given unitary operator $U$. This is a flexible version that allows the user to provide a callable that generates the unitary operator $U^k$ for a given integer $k$, offering greater flexibility in handling different quantum circuits using some powering rule. |
| `/classiq/open_library.functions.qpe.qpe` | Implements the standard Quantum Phase Estimation (QPE) algorithm, which estimates the phase (eigenvalue) associated with an eigenstate of a given unitary operator $U$. |
| `/classiq/open_library.functions.qsvt.qsvt_step` | Applies a single QSVT step, composed of 2 projector-controlled-phase rotations, and applications of the block encoding unitary `u` and its inverse:. |
| `/classiq/open_library.functions.qsvt.qsvt` | Implements the Quantum Singular Value Transformation (QSVT) - an algorithmic framework, used to apply polynomial transformations of degree `d` on the singular values of a block encoded matrix, given as the unitary `u`. Given a unitary $U$, a list of phase angles $\phi_1, \phi_2,. |
| `/classiq/open_library.functions.qsvt.projector_controlled_phase` | Assigns a phase to the entire subspace determined by the given projector. Corresponds to the operation:. |
| `/classiq/open_library.functions.qsvt.qsvt_inversion` | Implements matrix inversion on a given block-encoding of a square matrix, using the QSVT framework. Applies a polynomial approximation of the inverse of the singular values of the matrix encoded in `u`. |
| `/classiq/open_library.functions.qsvt.projector_controlled_double_phase` | Assigns 2 phases to the entire subspace determined by the given projector, each one is controlled differentely on a given `lcu` qvar. Used in the context of the `qsvt_lcu` function. |
| `/classiq/open_library.functions.qsvt.qsvt_lcu_step` | Applies a single QSVT-lcu step, composed of 2 double phase projector-controlled-phase rotations, and applications of the block encoding unitary `u` and its inverse:. |
| `/classiq/open_library.functions.qsvt.qsvt_lcu` | Implements the Quantum Singular Value Transformation (QSVT) for a linear combination of odd and even polynomials, so that it is possible to encode a polynomial of indefinite parity, such as approximation to exp(i*A) or exp(A). Should work for Hermitian block encodings. |
| `/classiq/open_library.functions.qsvt.gqsp` | Implements Generalized Quantum Signal Processing (GQSP), which realizes a (Laurent) polynomial transformation of degree d on the eigenvalues of the given signal unitary `u`. The protocol is according to https://arxiv. |
| `/classiq/open_library.functions.state_preparation.prepare_uniform_trimmed_state` | Initializes a quantum variable in a uniform superposition of the first `m` computational basis states:. |
| `/classiq/open_library.functions.state_preparation.prepare_uniform_interval_state` | Initializes a quantum variable in a uniform superposition of the specified interval in the computational basis states:. |
| `/classiq/open_library.functions.state_preparation.prepare_ghz_state` | Initializes a quantum variable in a Greenberger-Horne-Zeilinger (GHZ) state. i. |
| `/classiq/open_library.functions.state_preparation.prepare_exponential_state` | Prepares a quantum state with exponentially decreasing amplitudes. The state is prepared in the computational basis, with the amplitudes of the states decreasing exponentially with the index of the state:. |
| `/classiq/open_library.functions.state_preparation.prepare_bell_state` | Initializes a quantum array of size 2 in one of the four Bell states. |
| `/classiq/open_library.functions.state_preparation.inplace_prepare_int` | This function is **deprecated**. Use in-place-xor assignment statement in the form _target-var_ **^=** _quantum-expression_ or **inplace_xor(**_quantum-expression_**,** _target-var_**)** instead. |
| `/classiq/open_library.functions.state_preparation.prepare_int` | This function is **deprecated**. Use assignment statement in the form _target-var_ **\|=** _quantum-expression_ or **assign(**_quantum-expression_**,** _target-var_**)** instead. |
| `/classiq/open_library.functions.state_preparation.inplace_prepare_complex_amplitudes` | Prepares a quantum state with amplitudes and phases for each state according to the given parameters, in polar representation. Expects to act on an initialized zero state $\|0\rangle$. |
| `/classiq/open_library.functions.state_preparation.prepare_complex_amplitudes` | Initializes and prepares a quantum state with amplitudes and phases for each state according to the given parameters, in polar representation. |
| `/classiq/open_library.functions.state_preparation.prepare_dicke_state_unary_input` | Prepares a Dicke state with a variable number of excitations based on an unary-encoded input. |
| `/classiq/open_library.functions.state_preparation.prepare_dicke_state` | Prepares a Dicke state with k excitations over the provided quantum register. |
| `/classiq/open_library.functions.state_preparation.prepare_basis_state` | Initializes a quantum array in the specified basis state. |
| `/classiq/open_library.functions.state_preparation.prepare_linear_amplitudes` | Initializes a quantum variable in a state with linear amplitudes: $$\|\psi angle = rac{1}{Z}\sum_{x=0}^{2^n-1}{x\|x angle}$$ Where $Z$ is a normalization constant. |
| `/classiq/open_library.functions.state_preparation.inplace_prepare_sparse_amplitudes` | Prepares a quantum state with the given (complex) amplitudes. The input is given sparse format, as a list of non-zero states and their corresponding amplitudes. |
| `/classiq/open_library.functions.state_preparation.prepare_sparse_amplitudes` | Initializes and prepares a quantum state with the given (complex) amplitudes. The input is given sparse format, as a list of non-zero states and their corresponding amplitudes. |
| `/classiq/open_library.functions.swap_test.swap_test` | Tests the overlap (in terms of fidelity) of two quantum states. The fidelity of `state1` and `state2` is calculated from the probability of measuring `test` qubit in the state 0 as follows:. |
| `/classiq/open_library.functions.utility_functions.apply_to_all` | Applies the single-qubit operand `gate_operand` to each qubit in the qubit array `target`. |
| `/classiq/open_library.functions.utility_functions.hadamard_transform` | Applies Hadamard transform to the target qubits. |
| `/classiq/open_library.functions.utility_functions.modular_increment` | Adds $a$ to $x$ modulo the range of $x$, assumed that $x$ is a non-negative integer and $a$ is an integer. Mathematically it is described as:. |
| `/classiq/open_library.functions.variational.encode_in_angle` | Creates an angle encoding of n data points on n qubits. |
| `/classiq/open_library.functions.variational.encode_on_bloch` | Creates a dense angle encoding of n data points on n//2 qubits. |
| `/classiq/qmod.builtins.functions.exponentiation.suzuki_trotter` | Applies the Suzuki-Trotter decomposition to a Pauli operator. |
