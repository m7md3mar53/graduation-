// Function to preview an image from a file input
function previewImage() {
    const input = document.getElementById("imageInput");
    const file = input.files[0];

    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const img = document.getElementById("previewImage");
            img.src = e.target.result; // Set the source to the loaded file data
        };

        reader.readAsDataURL(file); // Read the file as a data URL
    }
}

// Function to download the current image
function downloadImage() {
    const img = document.getElementById("previewImage");
    if (img.src) {
        const link = document.createElement("a");
        link.href = img.src;
        link.download = "downloaded_image.jpg"; // Default download name
        link.click(); // Trigger the download
    }
}

// Function to download a key (text file)
function downloadKey(keyContent) {
    const blob = new Blob([keyContent], { type: "text/plain" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "encryption_key.txt"; // Default key file name
    link.click(); // Trigger the download
}

// Function to toggle the visibility of an element
function toggleState(elementId) {
    const element = document.getElementById(elementId);
    element.style.display = element.style.display === "none" ? "block" : "none";
}

// Function to apply Rubik's Cube-based encryption
function rubiksEncrypt(image, blockSize) {
    const canvas = document.createElement("canvas");
    const context = canvas.getContext("2d");

    canvas.width = image.width;
    canvas.height = image.height;

    context.drawImage(image, 0, 0);

    const blocksX = Math.ceil(canvas.width / blockSize);
    const blocksY = Math.ceil(canvas.height / blockSize);

    // Create blocks and shuffle them
    const blocks = [];
    for (let by = 0; by < blocksY; by++) {
        for (let bx = 0; bx < blocksX; bx++) {
            const block = context.getImageData(bx * blockSize, by * blockSize, blockSize, blockSize);
            blocks.push({ data: block, x: bx, y: by });
        }
    }

    // Shuffle the blocks
    blocks.sort(() => Math.random() - 0.5);

    // Create a new canvas to reassemble shuffled blocks
    const shuffledCanvas = document.createElement("canvas");
    shuffledCanvas.width = canvas.width;
    shuffledCanvas.height = canvas.height;
    const shuffledContext = shuffledCanvas.getContext("2d");

    blocks.forEach((block, index) => {
        const x = (index % blocksX) * blockSize;
        const y = Math.floor(index / blocksX) * blockSize;
        shuffledContext.putImageData(block.data, x, y);
    });

    // Return the encrypted image as a Data URL
    return shuffledCanvas.toDataURL("image/jpeg");
}

// Function to apply Rubik's Cube-based decryption
function rubiksDecrypt(shuffledImage, blockSize) {
    const canvas = document.createElement("canvas");
    const context = canvas.getContext("2d");

    canvas.width = shuffledImage.width;
    canvas.height = shuffledImage.height;

    context.drawImage(shuffledImage, 0, 0);

    const blocksX = Math.ceil(canvas.width / blockSize);
    const blocksY = Math.ceil(canvas.height / blockSize);

    // Create blocks from the image
    const blocks = [];
    for (let by = 0; by < blocksY; by++) {
        for (let bx = 0; bx < blocksX; bx++) {
            const block = context.getImageData(bx * blockSize, by * blockSize, blockSize, blockSize);
            blocks.push({ data: block, x: bx, y: by });
        }
    }

    // Sort blocks to reassemble them in the original order
    blocks.sort((a, b) => a.x - b.x || a.y - b.y);

    // Create a new canvas to reassemble unscrambled blocks
    const decryptedCanvas = document.createElement("canvas");
    decryptedCanvas.width = canvas.width;
    decryptedCanvas.height = canvas.height;
    const decryptedContext = decryptedCanvas.getContext("2d");

    blocks.forEach((block, index) => {
        const x = (index % blocksX) * blockSize;
        const y = Math.floor(index / blocksX) * blockSize;
        decryptedContext.putImageData(block.data, x, y);
    });

    // Return the decrypted image as a Data URL
    return decryptedCanvas.toDataURL("image/jpeg");
}

// Function to send data to a backend for encryption
function encryptImageBackend() {
    const data = {
        param1: 'some value', // Modify this with your specific data
    };

    fetch('/encrypt', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Backend encrypted result:', data.result);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Call the encryption function to send data to the backend
encryptImageBackend();
