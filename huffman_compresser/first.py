import heapq
import pickle

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def calculate_frequency(text):
    frequency = {}
    for char in text:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1
    return frequency

def build_huffman_tree(frequency):
    heap = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged = HuffmanNode(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2
        heapq.heappush(heap, merged)

    return heap[0]

def generate_huffman_codes(root):
    codes = {}
    def _generate_codes(node, current_code):
        if node is None:
            return
        if node.char is not None:
            codes[node.char] = current_code
        _generate_codes(node.left, current_code + "0")
        _generate_codes(node.right, current_code + "1")

    _generate_codes(root, "")
    return codes

def encode_text(text, huffman_codes):
    encoded_text = "".join(huffman_codes[char] for char in text)
    return encoded_text

def text_to_binary(encoded_text):
    byte_array = bytearray()
    for i in range(0, len(encoded_text), 8):
        byte = encoded_text[i:i+8]
        byte_array.append(int(byte, 2))
    return bytes(byte_array)

def binary_to_text(binary_data):
    bits = ""
    for byte in binary_data:
        bits += f"{byte:08b}"
    return bits

def decode_text(encoded_text, huffman_tree):
    decoded_text = ""
    current_node = huffman_tree
    for bit in encoded_text:
        if bit == "0":
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.left is None and current_node.right is None:
            decoded_text += current_node.char
            current_node = huffman_tree

    return decoded_text

def save_compressed_file(encoded_text, huffman_codes, file_path):
    binary_data = text_to_binary(encoded_text)
    with open(file_path, 'wb') as file:
        pickle.dump((binary_data, huffman_codes), file)

def load_compressed_file(file_path):
    with open(file_path, 'rb') as file:
        binary_data, huffman_codes = pickle.load(file)
    return binary_data, huffman_codes

# Example usage
file_path = r'C:/Users/india/Desktop/DSA projects/huffman_compresser/input.txt'
text = read_file(file_path)
frequency = calculate_frequency(text)
huffman_tree = build_huffman_tree(frequency)
huffman_codes = generate_huffman_codes(huffman_tree)
encoded_text = encode_text(text, huffman_codes)

compressed_file_path = r'C:/Users/india/Desktop/DSA projects/huffman_compresser/compressed.bin'
save_compressed_file(encoded_text, huffman_codes, compressed_file_path)
binary_data, loaded_huffman_codes = load_compressed_file(compressed_file_path)
decoded_text = decode_text(binary_to_text(binary_data), huffman_tree)

print("Done")


