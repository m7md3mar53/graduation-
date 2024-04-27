async function encryptImage() {
    const fileInput = document.getElementById("file");
    const keyInput = document.getElementById("key");
    const file = fileInput.files[0];
    const key = keyInput.value;

    if (file && key) {
        const formData = new FormData();
        formData.append("file", file);
        formData.append("key", key);

        const response = await fetch("/encrypt", {
            method: "POST",
            body: formData,
        });

        if (response.ok) {
            const encryptedBlob = await response.blob();
            const encryptedURL = URL.createObjectURL(encryptedBlob);

            const link = document.createElement("a");
            link.href = encryptedURL;
            link.download = "encrypted_image.bin";
            link.textContent = "Download Encrypted Image";

            const result = document.getElementById("result");
            result.innerHTML = "";
            result.appendChild(link);
        }
    }
}

async function decryptImage() {
    const fileInput = document.getElementById("file");
    const keyInput = document.getElementById("key");
    const file = fileInput.files[0];
    const key = keyInput.value;

    if (file && key) {
        const formData = new FormData();
        formData.append("file", file);
        formData.append("key", key);

        const response = await fetch("/decrypt", {
            method: "POST",
            body: formData,
        });

        if (response.ok) {
            const decryptedBlob = await response.blob();
            const decryptedURL = URL.createObjectURL(decryptedBlob);

            const image = document.createElement("img");
            image.src = decryptedURL;

            const result = document.getElementById("result");
            result.innerHTML = "";
            result.appendChild(image);
        }
    }
}
