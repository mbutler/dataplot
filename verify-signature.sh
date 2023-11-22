#!/bin/bash

# Path to your private and public key files
private_key_file="fake_private.txt"
public_key_file="fake_public.txt"

# article hash
text="891da86b2c7c7aaacbea4cad9abbae4b0214b01bc4d7a85dbbf68fa9811bda84"

# File names for temporary text and signature files
text_file="text.txt"
signature_file="signature.txt"

# Save the text string to a file
echo "$text" > "$text_file"

# Sign the text file
openssl dgst -sha256 -sign "$private_key_file" -out "$signature_file" "$text_file"

# Verify the signature
openssl dgst -sha256 -verify "$public_key_file" -signature "$signature_file" "$text_file"

# Clean up temporary files (optional)
#rm "$text_file" "$signature_file"
