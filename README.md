# Question Detection Solution

This repository contains a FastAPI application that processes images using the SmolDocling model for document layout analysis. It's containerized with Docker for easy deployment and execution.

## Building the Docker Image

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/akif-caglar/question_detection_vlm.git
    cd question_detection_vlm
    ```

2.  **Build the Docker Image:**
    ```bash
    docker build -t q-detect-api .
    ```

## Running the Docker Container

1.  **Run the Container (GPU):**
    ```bash
    docker run --gpus all -p 8000:8000 q-detect-api
    ```

## Using the API
Once the container is running, you can interact with the API using HTTP requests.

## Endpoints

### `/question-detect/` (POST)

**Description:**

This endpoint accepts an image file as input, processes it to detect question regions, crops those regions, and returns a concatenated image of the cropped questions.

**Request:**

-   **Method:** POST
-   **Headers:**
    -   `Content-Type: multipart/form-data`
-   **Body:**
    -   `file`: The image file to process.

**Response:**

-   **Status Code:** 200 (OK)
-   **Content-Type:** `image/png`
-   **Body:** A PNG image containing the horizontally concatenated cropped question regions.

**Testing:**
```bash
    python test.py
