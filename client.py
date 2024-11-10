# client.py
import requests
import random
import hashlib
import time

# Number of iterations
iterations = 1

# Start measuring overall runtime
overall_start_time = time.time()

# Fetch setup parameters from server
response = requests.get('http://localhost:5000/setup')
setup_data = response.json()

g = setup_data['g']
p = setup_data['p']
q = setup_data['q']
mpk = setup_data['mpk']

# Run the scheme for 10000 iterations
extract_runtimes = []
prove_verify_runtimes = []

for i in range(iterations):
    print(f"Iteration {i + 1}")
    
    # Extract Phase
    extract_start_time = time.time()
    ID = "Albert Einstein"

    # Issuer: Choose random values for α, β
    alpha = random.randint(1, q - 1)
    beta = random.randint(1, q - 1)

    # Generate R_prime and C_prime
    r = random.randint(1, q - 1)
    R = pow(g, r, p)  # Assume R comes from the server, initially known.
    R_prime = (pow(R, alpha, p) * pow(g, beta, p)) % p
    C_prime_input = f"{R_prime}{ID}".encode()
    C_prime = int(hashlib.sha256(C_prime_input).hexdigest(), 16) % q

    # Send R_prime and C_prime to server
    extract_data = {
        'R_prime': R_prime,
        'C_prime': C_prime,
        'alpha': alpha
    }
    extract_response = requests.post('http://localhost:5000/extract', json=extract_data)
    extract_response_data = extract_response.json()

    R = extract_response_data['R']
    s = extract_response_data['s']

    # End measuring extract phase runtime
    extract_end_time = time.time()
    extract_runtime = (extract_end_time - extract_start_time) * 1000  # Convert to milliseconds
    extract_runtimes.append(extract_runtime)

    # Verify Phase
    # Check if R = g^s * mpk^(-C) mod p
    C = (C_prime * pow(alpha, -1, q)) % q  # Recompute C as done on the server side
    lhs = R
    rhs = (pow(g, s, p) * pow(mpk, -C, p)) % p
    if lhs == rhs:
        print("Verification successful in Extract Phase: LHS equals RHS")
    else:
        print("Verification failed in Extract Phase: LHS does not equal RHS")

    # Prove and Verify Phase
    prove_verify_start_time = time.time()

    # Prover (P): Choose y from Z_q^*
    y = random.randint(1, q - 1)
    Y = pow(g, y, p)  # Y = g^y
    V = (pow(g, s, p) * pow(mpk, C_prime, p)) % p  # V = g^s * X^C'

    # Verifier (V): Choose u from Z_q^*
    u = random.randint(1, q - 1)

    # Send Prove and Verify data to server
    prove_verify_data = {
        'y': y,
        'S_prime': s,
        'C_prime': C_prime,
        'u': u,
        'Y': Y,
        'V': V
    }
    prove_verify_response = requests.post('http://localhost:5000/prove_verify', json=prove_verify_data)
    prove_verify_response_data = prove_verify_response.json()

    # End measuring prove and verify phase runtime
    prove_verify_end_time = time.time()
    prove_verify_runtime = (prove_verify_end_time - prove_verify_start_time) * 1000  # Convert to milliseconds
    prove_verify_runtimes.append(prove_verify_runtime)

    if prove_verify_response_data['verification']:
        print("Verification successful in Prove and Verify Phase: LHS equals RHS")
    else:
        print("Verification failed in Prove and Verify Phase: LHS does not equal RHS")

# End measuring overall runtime
overall_end_time = time.time()
overall_runtime = (overall_end_time - overall_start_time) * 1000  # Convert to milliseconds
average_extract_runtime = sum(extract_runtimes) / len(extract_runtimes) if extract_runtimes else 0
average_prove_verify_runtime = sum(prove_verify_runtimes) / len(prove_verify_runtimes) if prove_verify_runtimes else 0
average_runtime = overall_runtime / iterations  # Calculate average runtime per iteration

# Fetch runtime statistics from server
runtime_response = requests.get('http://localhost:5000/runtime_stats')
runtime_stats = runtime_response.json()

# Print all the statistics
print("\nRuntime Statistics from Server:")
print(f"Average Setup Phase Runtime: {runtime_stats['average_setup_runtime_ms']} ms")
print(f"Average Extract Phase Runtime: {average_extract_runtime:.2f} ms")
print(f"Average Prove and Verify Phase Runtime: {average_prove_verify_runtime:.2f} ms")
print(f"Average Overall Runtime per iteration: {average_runtime:.2f} ms")
print(f"Overall Runtime for {iterations} iterations: {overall_runtime:.2f} ms")
print(f"Current Memory Usage: {runtime_stats['current_memory_usage_kb']:.2f} KB")
print(f"Peak Memory Usage: {runtime_stats['peak_memory_usage_kb']:.2f} KB")
print("All iterations complete.")
