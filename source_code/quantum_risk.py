from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def quantum_risk_score(risks, ai_score):

    score = 0

    for r in risks:

        level = r[1]

        if "High" in level:
            score += 30

        elif "Medium" in level:
            score += 20

        elif "Sensitive" in level:
            score += 25

        else:
            score += 10

    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)

    simulator = AerSimulator()

    job = simulator.run(qc, shots=1)

    result = job.result()

    counts = result.get_counts()

    rule_score = score
    
    llm_score = ai_score

    quantum_factor = int(list(counts.keys())[0])

    final_score = (rule_score * 0.6) + (llm_score * 0.4) + quantum_factor

    final_score = min(int(final_score), 100)
    return final_score