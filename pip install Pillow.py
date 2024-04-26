import numpy as np
from PIL import Image
import random

# Constants
ALPHA = 4  # Hyperparameter for key generation
ITER_MAX = 3  # Number of iterations for encryption/decryption
BLOCK_SIZE = 16  # Size of each block for Rubik's Cube-like shuffling

# Generate key vectors
def generate_key_vectors(width, height, alpha):
    Kr = [random.randint(0, 2 * alpha - 1) for _ in range(height)]
    Kc = [random.randint(0, 2 * alpha - 1) for _ in range(width)]
    return Kr, Kc

# Shuffling based on Rubik's Cube principle
def shuffle_blocks(image, block_size):
    width, height = image.size
    blocks_x = width // block_size
    blocks_y = height // block_size

    # Create a list of blocks
    blocks = []
    for by in range(blocks_y):
        for bx in range(blocks_x):
            block = image.crop((bx * block_size, by * block_size, (bx + block_size), (by + block_size)))
            blocks.append(block)

    # Shuffle the blocks randomly
    random.shuffle(blocks)

    # Create a new image to hold the shuffled blocks
    shuffled_image = Image.new("RGB", (blocks_x * block_size, blocks_y * block_size))
    index = 0

    for by in range(blocks_y):
        for bx in range(blocks_x):
            shuffled_image.paste(blocks[index], (bx * block_size, by * block_size))
            index += 1

    return shuffled_image

# Rolling operations for rows and columns
def roll_array(array, times, direction):
    if direction == "right":
        return np.roll(array, times, axis=1)
    elif direction == "left":
        return np.roll(array, -times, axis=1)
    elif direction == "down":
        return np.roll(array, times, axis=0)
    elif direction == "up":
        return np.roll(array, -times, axis=0)

# XOR transformation
def xor_transform(pixel, key):
    return pixel ^ key

# Encryption function
def encrypt_image(image_path, Kr, Kc, block_size, iter_max):
    original_image = Image.open(image_path)

    # Shuffle the blocks
    shuffled_image = shuffle_blocks(original_image, block_size)

    # Convert the shuffled image to numpy array for further manipulation
    image_data = np.array(shuffled_image)

    # Iterate the encryption process
    for _ in range(iter_max):
        # Rolling rows
        for i in range(image_data.shape[0]):
            row_sum = np.sum(image_data[i])
            direction = "right" if row_sum % 2 == 0 else "left"
            image_data[i] = roll_array(image_data[i], Kr[i], direction)

        # Rolling columns
        for j in range(image_data.shape[1]):
            col_sum = np.sum(image_data[:, j])
            direction = "down" if col_sum % 2 == 0 else "up"
            image_data[:, j] = roll_array(image_data[:, j], Kc[j], direction)

        # XOR transformation
        for i in range(image_data.shape[0]):
            for j in range(image_data.shape[1]):
                if j % 2 == 0:
                    image_data[i, j] = xor_transform(image_data[i, j], Kr[i])
                else:
                    image_data[i, j] = xor_transform(image_data[i, j], 180)
                
                if i % 2 == 0:
                    image_data[i, j] = xor_transform(image_data[i, j], 180)
                else:
                    image_data[i, j] = xor_transform(image_data[i, j], Kc[j])

    encrypted_image = Image.fromarray(image_data)
    return encrypted_image


# Decrypt image
def decrypt_image(encrypted_image, Kr, Kc, block_size, iter_max):
    image_data = np.array(encrypted_image)

    # Decryption process in reverse order
    for _ in range(iter_max):
        # XOR transformation
        for i in range(image_data.shape[0]):
            for j in range(image_data.shape[1]):
                if i % 2 == 0:
                    image_data[i, j] = xor_transform(image_data[i, j], 180)
                else:
                    image_data[i, j] = xor_transform(image_data[i, j], Kc[j])
                
                if j % 2 == 0:
                    image_data[i, j] = xor_transform(image_data[i, j], Kr[i])
                else:
                    image_data[i, j] = xor_transform(image_data[i, j], 180)

        # Rolling columns in reverse
        for j in range(image_data.shape[1]):
            col_sum = np.sum(image_data[:, j])
            direction = "down" if col_sum % 2 == 0 else "up"
            image_data[:, j] = roll_array(image_data[:, j], -Kc[j], direction)

        # Rolling rows in reverse
        for i in range(image_data.shape[0]):
            row_sum = np.sum(image_data[i])
            direction = "right" if row_sum % 2 == 0 else "left"
            image_data[i] = roll_array(image_data[i], -Kr[i], direction)

    decrypted_image = Image.fromarray(image_data)

    return decrypted_image


# Example usage
image_path = "your_image.jpg"  # Replace with the path to your image
Kr, Kc = generate_key_vectors(50, 50, ALPHA)  # Replace 50 with the dimensions of your image
encrypted_image = encrypt_image(image_path, Kr, Kc, BLOCK_SIZE, ITER_MAX)

# Save the encrypted image
encrypted_image.save("encrypted_image.jpg")

# Decrypt the image
decrypted_image = decrypt_image(encrypted_image, Kr, Kc, BLOCK_SIZE, ITER_MAX)

# Save the decrypted image
decrypted_image.save("decrypted_image.jpg")
