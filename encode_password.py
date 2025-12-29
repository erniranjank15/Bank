"""
URL encode MongoDB password for connection string
"""

import urllib.parse

def encode_password(password):
    """Encode password for MongoDB URI"""
    encoded = urllib.parse.quote(password, safe='')
    return encoded

def create_mongodb_uri(username, password, cluster):
    """Create properly formatted MongoDB URI"""
    encoded_password = encode_password(password)
    uri = f"mongodb+srv://{username}:{encoded_password}@{cluster}/?retryWrites=true&w=majority"
    return uri

# Your MongoDB credentials
username = "kasoteniranjan23_db_user"
password = "Niranjan23"
cluster = "cluster0.mejihk9.mongodb.net"

print("🔐 MongoDB Password Encoding")
print("=" * 50)
print(f"Original password: {password}")

encoded_password = encode_password(password)
print(f"Encoded password:  {encoded_password}")

print("\n🔗 MongoDB Connection Strings:")
print("=" * 50)

# Original URI
original_uri = f"mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority"
print(f"Original URI:\n{original_uri}")

# Encoded URI
encoded_uri = create_mongodb_uri(username, password, cluster)
print(f"\nEncoded URI:\n{encoded_uri}")

print("\n📋 Special Characters Encoding:")
print("=" * 50)
special_chars = {
    '@': '%40',
    '#': '%23', 
    '$': '%24',
    '%': '%25',
    '^': '%5E',
    '&': '%26',
    '*': '%2A',
    '(': '%28',
    ')': '%29',
    '+': '%2B',
    '=': '%3D',
    '[': '%5B',
    ']': '%5D',
    '{': '%7B',
    '}': '%7D',
    '|': '%7C',
    '\\': '%5C',
    ':': '%3A',
    ';': '%3B',
    '"': '%22',
    "'": '%27',
    '<': '%3C',
    '>': '%3E',
    ',': '%2C',
    '?': '%3F',
    '/': '%2F',
    ' ': '%20'
}

print("If your password contains these characters, they need encoding:")
for char, encoded in special_chars.items():
    print(f"  {char} → {encoded}")

print(f"\n✅ Your password '{password}' analysis:")
needs_encoding = False
for char in password:
    if char in special_chars:
        print(f"  ⚠️  Contains '{char}' - needs encoding to '{special_chars[char]}'")
        needs_encoding = True

if not needs_encoding:
    print("  ✅ No special characters found - no encoding needed!")

print(f"\n🎯 FINAL CONNECTION STRING FOR RENDER:")
print("=" * 50)
print(encoded_uri)