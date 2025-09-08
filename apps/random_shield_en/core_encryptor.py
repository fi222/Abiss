import random

ALPHANUMERIC = 'abcdefghijklmnopqrstuvwxyz0123456789 '
POOL_SIZE = 100  # Each character gets 100 randomized values

def generate_pools(key_list):
    pools = {}
    current_value = 0

    for char in ALPHANUMERIC:
        pools[char] = []
        for _ in range(POOL_SIZE):
            for key in key_list:
                current_value += key
                pools[char].append(current_value)
        random.shuffle(pools[char])
    return pools

def encode_message(message, key_list, noise_amount):
    pools = generate_pools(key_list)
    encoded_numbers = []

    for char in message.lower():
        if char not in pools:
            continue  # Skip unsupported characters

        assigned_number = random.choice(pools[char])
        pools[char].remove(assigned_number)  # Avoid reuse

        for _ in range(noise_amount):
            encoded_numbers.append(random.randint(1000, 99999))

        encoded_numbers.append(assigned_number)

    for _ in range(noise_amount):
        encoded_numbers.append(random.randint(1000, 99999))

    return ' '.join(str(num) for num in encoded_numbers)

def decode_message(encoded_text, key_list, use_segmentation=False):
    pools = generate_pools(key_list)
    reverse_lookup = {}

    for char, numbers in pools.items():
        for num in numbers:
            reverse_lookup[num] = char

    decoded_chars = []
    try:
        encoded_numbers = map(int, encoded_text.strip().split())
    except ValueError:
        return "[Error] Encoded text must be numbers separated by spaces."

    for num in encoded_numbers:
        if num in reverse_lookup:
            decoded_chars.append(reverse_lookup[num])

    result = ''.join(decoded_chars)
    if use_segmentation:
        return smart_segment(result)
    return result

# Optional word segmentation (only works if wordsegment is installed)
def smart_segment(text):
    try:
        from wordsegment import load, segment
        load()
        return ' '.join(segment(text))
    except ImportError:
        return "[Segment error] Install with: pip install wordsegment"

# Optional test
if __name__ == "__main__":
    key = [456, 902, 2364, 3476]
    noise = 5
    message = "good morning how are you"

    encoded = encode_message(message, key, noise)
    print("Encoded:", encoded)

    decoded = decode_message(encoded, key)
    print("Decoded:", decoded)

    segmented = decode_message(encoded, key, use_segmentation=True)
    print("Segmented:", segmented)

    input("Press Enter to exit...")
