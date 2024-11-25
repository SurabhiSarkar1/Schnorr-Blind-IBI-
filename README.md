**Schnorr Identity Based Blind Identification Scheme**

**Overview**
This repository contains the implementation and analysis of Schnorr Identity-Based Blind Identification (IBBI) Scheme, a novel approach to construct a pairing-free, provably secure blind variation of the Schnorr Identification Scheme, designed to ensure user anonymity and strong security under the random oracle model. The study encompasses computational efficiency in resource-constrained environments like IoT systems and compares its efficiency.



**Contents:**

The source code for the implementation in Python Flask.

Client-Server setup for runtime efficiency and memory usage across devices (e.g., Raspberry Pi 3/local machine).




**Installation Dependencies/Libraries:**
- python 3.x
- Libraries/Imports: 
Flask: lightweight web framework for Python used to create web applications. Also the main class to create a Flask application.
request: to provide access to the data sent with the HTTP request.
jsonify: to Convert Python dictionaries or lists into JSON format for HTTP responses.
cryptography: main library to be used to import cryptographic modules.
Diffie-Hellman (DH) cryptographic primitives: The dh module provides methods to generate DH key pairs and perform the key exchange process.
default cryptographic backend: to perform cryptographic operations like key generation and signature verification.
random: to generate random numbers.
hashlib: for secure hashing algorithms like SHA-256 or MD5.
time: for measuring execution time or introducing delays/calculation of run times for each phases.
tracemalloc: to track memory allocations and performance optimization.


### How to run the scheme:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/SurabhiSarkar1/Schnorr-Blind-IBI-.git
   ```


2. **Run the Schemes**:
   ```bash
   python client.py   # to run the scheme and record ouputs
   python server.py # to initiate the server and start keygen process/verification process
   ```
### Results:
   Overall Runtime and Runtimes for Setup, Extract and Identification Protocol Stage
   Overall and phase wise Memory Usage 


   Experiments were conducted on:
IdeaPad 5 15ALC05 (AMD Ryzen 7 5700U)
Alienware m15 (Intel Core i7-8750H)
Raspberry Pi 3 (ARM Cortex-A53)

Use Cases
Electronic Voting: Ensures voter anonymity during authentication.
Secure Banking Transactions: Provides secure, private identity verification.
IoT Access Control: Lightweight and efficient for resource-constrained devices.

References: 
1. Chia, J., Chin, J. J., & Yip, S. C. (2021). A Pairing-Free Identity-Based Identification Scheme with Tight Security Using Modified-Schnorr Signatures. Symmetry, 13(8), 1330.
2. Tan, S.-Y., Heng, S.-H., Phan, R.C.-W. . and Goi, B.-M. (2011). A Variant of Schnorr Identity-Based Identification Scheme with Tight Reduction. Lecture Notes in Computer Science, pp.361–370. 20doi:https://doi.org/10.1007/978-3-642-27142-7_42.

Contact:
www.linkedin.com/in/surabhi-sarkar-172026195