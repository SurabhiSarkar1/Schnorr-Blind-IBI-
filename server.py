# server.py
from flask import Flask, request, jsonify
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.backends import default_backend
import random
import hashlib
import time
import tracemalloc

app = Flask(__name__)

# Start measuring setup phase runtime
setup_start_time = time.time()

# Setup Phase (Key Generation Phase)
parameters = dh.generate_parameters(generator=2, key_size=2048, backend=default_backend())
sk = parameters.generate_private_key()  # Server's private key
parameters_numbers = parameters.parameter_numbers()
g = parameters_numbers.g
p = parameters_numbers.p
q = (p - 1) // 2
sk_value = sk.private_numbers().x
mpk = pow(g, sk_value, p)  # Public key

# End measuring setup phase runtime
setup_end_time = time.time()
setup_runtime = (setup_end_time - setup_start_time) * 1000  # Convert to milliseconds
setup_runtimes = [setup_runtime]

# Runtime and memory statistics
extract_runtimes = []
prove_verify_runtimes = []
overall_runtimes = []

@app.route('/setup', methods=['GET'])
def setup():
    return jsonify({
        'g': g,
        'p': p,
        'q': q,
        'mpk': mpk
    })

@app.route('/extract', methods=['POST'])
def extract():
    overall_start_time = time.time()
    start_time = time.time()
    data = request.get_json()
    R_prime = data['R_prime']
    C_prime = data['C_prime']
    alpha = data['alpha']
    
    # Issuer: Choose r from Z_q^*
    r = random.randint(1, q - 1)
    R = pow(g, r, p)  # R = g^r

    # Compute challenge C and response s
    C = (C_prime * pow(alpha, -1, q)) % q
    s = (r + C * sk_value) % q

    extract_runtime = (time.time() - start_time) * 1000  # Convert to milliseconds
    extract_runtimes.append(extract_runtime)

    overall_end_time = time.time()
    overall_runtime = (overall_end_time - overall_start_time) * 1000  # Convert to milliseconds
    overall_runtimes.append(overall_runtime)

    return jsonify({
        'R': R,
        's': s
    })

@app.route('/prove_verify', methods=['POST'])
def prove_verify():
    overall_start_time = time.time()
    start_time = time.time()
    data = request.get_json()
    y = data['y']
    S_prime = data['S_prime']
    C_prime = data['C_prime']
    u = data['u']
    Y = data['Y']
    V = data['V']

    # Verifier: Check if g^z = Y * (V / mpk^C_prime)^u mod p
    z = (y + u * S_prime) % q
    lhs_verify = pow(g, z, p)
    rhs_verify = (Y * pow(V * pow(mpk, -C_prime, p), u, p)) % p

    prove_verify_runtime = (time.time() - start_time) * 1000  # Convert to milliseconds
    prove_verify_runtimes.append(prove_verify_runtime)

    overall_end_time = time.time()
    overall_runtime = (overall_end_time - overall_start_time) * 1000  # Convert to milliseconds
    overall_runtimes.append(overall_runtime)

    return jsonify({
        'verification': lhs_verify == rhs_verify,
        'lhs': lhs_verify,
        'rhs': rhs_verify
    })

@app.route('/runtime_stats', methods=['GET'])
def runtime_stats():
    avg_setup_runtime = sum(setup_runtimes) / len(setup_runtimes) if setup_runtimes else 0
    avg_extract_runtime = sum(extract_runtimes) / len(extract_runtimes) if extract_runtimes else 0
    avg_prove_verify_runtime = sum(prove_verify_runtimes) / len(prove_verify_runtimes) if prove_verify_runtimes else 0
    avg_overall_runtime = sum(overall_runtimes) / len(overall_runtimes) if overall_runtimes else 0

    current, peak = tracemalloc.get_traced_memory()

    return jsonify({
        'average_setup_runtime_ms': avg_setup_runtime,
        'average_extract_runtime_ms': avg_extract_runtime,
        'average_prove_verify_runtime_ms': avg_prove_verify_runtime,
        'average_overall_runtime_ms': avg_overall_runtime,
        'current_memory_usage_kb': current / 1024,
        'peak_memory_usage_kb': peak / 1024
    })

if __name__ == '__main__':
    tracemalloc.start()
    app.run(debug=True, port=5000)
