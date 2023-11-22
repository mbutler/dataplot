#!/bin/bash

# Ask the user for the number of iterations
echo -n "Enter the number of key pairs to generate: "
read iterations

for i in $(seq 1 $iterations); do
    # Generate a unique identifier based on date and time
    unique_id=$(date +"%Y%m%d%H%M%S")

    # Create filenames for private and public keys
    private_key_file="${unique_id}_private_charmfarm_key.txt"
    public_key_file="${unique_id}_public_charmfarm_key.txt"

    # Generate the private key
    openssl genpkey -algorithm RSA -out "$private_key_file"
    if [ $? -ne 0 ]; then
        echo "Failed to generate private key"
        exit 1
    fi

    # Generate the public key from the private key
    openssl rsa -pubout -in "$private_key_file" -out "$public_key_file"
    if [ $? -ne 0 ]; then
        echo "Failed to generate public key"
        exit 1
    fi

    echo "Keys generated successfully for iteration $i:"
    echo "Private Key: $private_key_file"
    echo "Public Key: $public_key_file"

    # Sleep for 1 second to avoid duplicate filenames
    sleep 1
done
