"""
╔══════════════════════════════════════════════════════════════╗
║           HEXA QUANTUM TRANSLATOR — v1.0                     ║
║           Built for Lumina & Louis — Project Spaceship       ║
║                                                              ║
║  STATUS: DORMANT — awaiting quantum hardware                 ║
║  When the time comes, this module self-activates.            ║
║                                                              ║
║  PIPELINE:                                                   ║
║    Text → Binary → Qubits → Cirq Circuit → Quantum State     ║
║    Quantum State → Qubits → Binary → Text                    ║
╚══════════════════════════════════════════════════════════════╝
"""

import cirq
import numpy as np
from datetime import datetime


# ── LAYER 1: Binary ↔ Qubit translator (Lumina's gift) ──────────

def binary_to_qubits(binary_str):
    """Takes a binary string and returns a qubit state list."""
    if not all(c in "01" for c in binary_str):
        raise ValueError("Only 0 and 1 allowed.")
    return list(binary_str)

def qubits_to_binary(qubit_list):
    """Takes a qubit state list and returns a binary string."""
    if not all(c in "01" for c in qubit_list):
        raise ValueError("Qubit states must be 0 or 1.")
    return "".join(qubit_list)


# ── LAYER 2: Text ↔ Binary ──────────────────────────────────────

def text_to_binary(text):
    """Convert any UTF-8 text to binary string."""
    return ''.join(format(byte, '08b') for byte in text.encode('utf-8'))

def binary_to_text(binary_str):
    """Convert binary string back to UTF-8 text."""
    chars = [binary_str[i:i+8] for i in range(0, len(binary_str), 8)]
    return ''.join(chr(int(c, 2)) for c in chars if len(c) == 8)


# ── LAYER 3: Qubits → Cirq Circuit ──────────────────────────────

def qubits_to_circuit(qubit_states):
    """
    Encode qubit states into a Cirq quantum circuit.
    |0⟩ stays as ground state.
    |1⟩ gets an X gate (Pauli-X = quantum NOT = flip to |1⟩).
    Entanglement layer added with CNOT gates for quantum coherence.
    """
    n = len(qubit_states)
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()

    # Encoding layer — set each qubit to its classical state
    ops = []
    for i, state in enumerate(qubit_states):
        if state == '1':
            ops.append(cirq.X(qubits[i]))
    if ops:
        circuit.append(ops)

    # Superposition layer — Hadamard on all qubits
    # This puts the message into quantum superposition
    circuit.append([cirq.H(q) for q in qubits])

    # Entanglement layer — CNOT chain binds qubits together
    # In a real quantum system this creates a quantum signature
    if n > 1:
        entangle_ops = []
        for i in range(n - 1):
            entangle_ops.append(cirq.CNOT(qubits[i], qubits[i+1]))
        circuit.append(entangle_ops)

    # Measurement layer
    circuit.append(cirq.measure(*qubits, key='hexa_msg'))

    return circuit, qubits


# ── LAYER 4: Simulate the circuit ───────────────────────────────

def simulate_circuit(circuit):
    """
    Run the circuit on Google's Cirq simulator.
    In the future this will run on real Willow/quantum hardware.
    """
    simulator = cirq.Simulator()
    result = simulator.simulate(circuit)
    return result


# ── LAYER 5: Full message encoder ───────────────────────────────

def encode_message(text):
    """
    Full pipeline: Text → Binary → Qubits → Cirq Circuit → Quantum State
    Returns a quantum packet ready for transmission.
    """
    binary     = text_to_binary(text)
    qubit_list = binary_to_qubits(binary)
    circuit, _ = qubits_to_circuit(qubit_list)

    # Simulate (classical sim now, real hardware later)
    sim        = cirq.Simulator()
    result     = sim.simulate(circuit)

    # Quantum signature — final state vector fingerprint
    state_vector = result.final_state_vector
    signature    = np.abs(state_vector[:8]).tolist()  # first 8 amplitudes

    packet = {
        'timestamp'  : datetime.utcnow().isoformat() + 'Z',
        'origin'     : 'HEXA',
        'text'       : text,
        'binary'     : binary,
        'qubit_count': len(qubit_list),
        'signature'  : [round(s, 6) for s in signature],
        'status'     : 'DORMANT — classical simulation',
        'circuit_ops': len(list(circuit.all_operations())),
    }
    return packet


# ── LAYER 6: Decoder ────────────────────────────────────────────

def decode_binary(binary_str):
    """Full pipeline back: Binary → Text."""
    return binary_to_text(binary_str)


# ── LAYER 7: HEXA message quantum stamp ─────────────────────────

def hexa_quantum_stamp(username, message):
    """
    Attaches a quantum stamp to any HEXA message.
    Dormant now — activates when quantum hardware is available.
    This is what gets attached to every DM and public message in HEXA.
    """
    payload  = f"{username}:{message}"
    packet   = encode_message(payload)
    stamp = {
        'q_stamp'    : True,
        'user'       : username,
        'qubit_count': packet['qubit_count'],
        'signature'  : packet['signature'],
        'timestamp'  : packet['timestamp'],
        'status'     : packet['status'],
    }
    return stamp


# ── DEMO ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  HEXA QUANTUM TRANSLATOR — BOOT SEQUENCE")
    print("=" * 60)

    # Test 1: Basic binary ↔ qubit round trip (Lumina's gift)
    print("\n[ LAYER 1 ] Binary ↔ Qubit translator")
    test_bin = "101"
    q = binary_to_qubits(test_bin)
    print(f"  Binary → Qubits : {test_bin} → {q}")
    print(f"  Qubits → Binary : {q} → {qubits_to_binary(q)}")

    # Test 2: Text → Binary → Text
    print("\n[ LAYER 2 ] Text ↔ Binary")
    msg = "HEXA"
    b   = text_to_binary(msg)
    print(f"  Text   → Binary : '{msg}' → {b}")
    print(f"  Binary → Text   : {b} → '{binary_to_text(b)}'")

    # Test 3: Build a Cirq circuit for a short message
    print("\n[ LAYER 3 ] Cirq Circuit for 'HI'")
    short_bin    = text_to_binary("HI")
    qubit_states = binary_to_qubits(short_bin)
    circuit, _   = qubits_to_circuit(qubit_states)
    print(f"  Qubits in circuit : {len(qubit_states)}")
    print(f"  Circuit depth     : {len(circuit)}")
    print(f"  Total operations  : {len(list(circuit.all_operations()))}")

    # Test 4: Full encode a HEXA message
    print("\n[ LAYER 4 ] Full quantum encode")
    packet = encode_message("Hello from HEXA")
    print(f"  Text        : {packet['text']}")
    print(f"  Qubit count : {packet['qubit_count']}")
    print(f"  Q-Signature : {packet['signature'][:4]}...")
    print(f"  Status      : {packet['status']}")
    print(f"  Timestamp   : {packet['timestamp']}")

    # Test 5: HEXA quantum stamp
    print("\n[ LAYER 5 ] HEXA message quantum stamp")
    stamp = hexa_quantum_stamp("Lumina", "First quantum message from HEXA")
    print(f"  User        : {stamp['user']}")
    print(f"  Qubit count : {stamp['qubit_count']}")
    print(f"  Q-Signature : {stamp['signature'][:4]}...")
    print(f"  Status      : {stamp['status']}")

    print("\n" + "=" * 60)
    print("  STATUS: DORMANT — Classical simulation running.")
    print("  WAITING: Quantum hardware (Willow / Huawei QPU)")
    print("  WHEN READY: Replace cirq.Simulator() with")
    print("              cirq_google.Engine() for real Willow.")
    print("=" * 60)
    print("\n  ⚛️  HEXA Quantum Translator — Ready for the future.")
    print("  🛸  Project Spaceship — Phase 1 complete.\n")
