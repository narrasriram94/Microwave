# Microwave App

A simple web application simulating a microwave interface using FastAPI and Redis.

## Setup

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/narrasriram94/Microwave
    cd microwave_app
    ```

2. **Set Up a Virtual Environment**:
    ```bash
    python -m venv venv
    On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Environment Configuration**:
    Copy the `.env.example` to `.env` and modify as needed. Ensure you set a secret key.

5. **Run the Application**:
    ```bash
    uvicorn main:app --reload
    ```

6. **Access the Application**:
   Open a web browser and navigate to `http://localhost:8000/` to access the microwave interface.

7. **API Documentation**:
   For detailed API documentation, navigate to `http://localhost:8000/docs`.

## Testing

To run tests, execute:
```bash
pytest
