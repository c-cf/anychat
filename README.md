# AnyChat

Welcome to AnyChat! This is a FastAPI-based chat application that combines document management and role assignment features, utilizing the latest language model technology to provide intelligent responses.

## Features

- **Authentication and Authorization**: Secure authentication and authorization using OAuth2 and JWT.
- **Chat Functionality**: Real-time message handling with intelligent responses.
- **Document Management**: Support for adding, updating, deleting, and listing documents with permission control.
- **Role Assignment**: Flexible role and permission management system, supporting custom roles and permissions.

## TODO List
### Infrastructure
- [x] Design and implement complete database models (using SQLAlchemy ORM)
- [x] Establish database migration system (Alembic)
- [x] Implement containerized deployment (Docker & Docker Compose)
- [ ] Set up CI/CD pipeline
- [x] Create configurations for development, testing, and production environments

### User Management & Authentication

- [ ] Complete user registration and login system
- [ ] Password reset functionality
- [ ] Email verification
- [ ] OAuth third-party login integration (Google, GitHub, etc.)
- [ ] JWT token refresh mechanism
- [ ] Multi-factor authentication (optional)

### Permission Management

- [ ]  Convert in-memory permission storage to database storage
- [ ]  Implement role-based access control (RBAC)
- [ ]  Fine-grained permission management (for documents and features)
- [ ]  Permission audit logging
- [ ]  User groups and team management

### Document Management

- [ ] Document version control
- [ ] Document classification and tagging system
- [ ] Multi-format document support (PDF, DOCX, Markdown, etc.)
- [ ] Batch import/export functionality
- [ ] Document sharing and collaboration features
- [ ] Document permission management

### RAG Engine Enhancements

- [ ] Query preprocessing and rewriting
- [ ] Hybrid retrieval (keywords + semantic)
- [ ] Relevance ranking algorithm optimization
- [ ] Dynamic context length adjustment
- [ ] LLM prompt optimization
- [ ] Citation accuracy verification
- [ ] Enhanced multilingual support

### Chat Functionality

- [ ] Chat history persistence
- [ ] Conversation context management
- [ ] Message grouping and search
- [ ] Conversation export functionality
- [ ] Inline citations and annotations
- [ ] File upload/sharing within chat

### Monitoring & Analytics

- [ ] User query logging system
- [ ] Performance metrics dashboard
- [ ] Usage statistics and reporting
- [ ] User feedback collection mechanism
- [ ] Answer quality evaluation
- [ ] API usage monitoring

### Frontend Interface

- [ ] Responsive chat UI
- [ ] Document management dashboard
- [ ] Admin control panel
- [ ] User settings page
- [ ] Multi-theme support
- [ ] Mobile-friendly design

### Security Enhancements

- [ ] API rate limiting
- [ ] Input validation and sanitization
- [ ] SQL injection protection
- [ ] CSRF protection
- [ ] Data encryption
- [ ] Secure dependency management and auditing

### Advanced Features

- [ ] Multi-model support (switching between different LLMs)
- [ ] Knowledge base auto-updates
- [ ] Custom plugin system
- [ ] API integration interface
- [ ] Scheduled tasks and automation
- [ ] Asynchronous processing for long-running tasks

### Performance Optimization

- [ ] Implement caching layer
- [ ] Database index optimization
- [ ] Vector retrieval performance tuning
- [ ] Horizontal scaling support
- [ ] Non-blocking processing for large documents
- [ ] Batch processing for vector operations

### Documentation & Support

- [ ] API documentation (using Swagger/OpenAPI)
- [ ] User manual
- [ ] Developer documentation
- [ ] Contribution guidelines
- [ ] Examples and tutorials
- [ ] Frequently asked questions

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
