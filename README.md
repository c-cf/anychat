# AnyChat

Welcome to AnyChat! This is a FastAPI-based chat application that combines document management and role assignment features, utilizing the latest language model technology to provide intelligent responses.

## Features

- **Authentication and Authorization**: Secure authentication and authorization using OAuth2 and JWT.
- **Chat Functionality**: Real-time message handling with intelligent responses.
- **Document Management**: Support for adding, updating, deleting, and listing documents with permission control.
- **Role Assignment**: Flexible role and permission management system, supporting custom roles and permissions.

## Getting Started

### Environment Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/anychat.git
    cd anychat
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # For Windows use `venv\Scripts\activate`
    ```

3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Configure environment variables:
    Create a `.env` file and add the following content:
    ```env
    SECRET_KEY=your_secret_key
    ALGORITHM=HS256
    DB_TYPE=sqlite
    DB_CONNECTION=sqlite:///./app.db
    VECTOR_DB_TYPE=qdrant
    VECTOR_DB_URL=http://localhost:6333
    LLM_TYPE=ollama
    LLM_MODEL=llama2
    ```

### Running the Application

1. Start the application:
    ```sh
    uvicorn main:app --reload
    ```

2. Open your browser and visit `http://127.0.0.1:8000/docs` to view the API documentation.

## Testing

We provide detailed testing documentation. Please refer to [TESTING.md](https://github.com/c-cf/anychat/blob/main/TESTING.md) for information on how to run and write test cases.

## Contributing

We welcome contributions of any kind! Please read CONTRIBUTING.md for more information.

## License

This project is open-sourced under the Apache 2.0 License.

## Contact Us

If you have any questions or suggestions, please reach out to us via [issues](https://github.com/yourusername/anychat/issues).

---

Let's make chatting smarter and more fun together! 🚀
