"""
Infrastructure Layer

External adapters and implementations:
- Database repositories (MongoDB, Redis, S3)
- External services (Clerk Auth, APIs)
- Framework configurations (FastAPI)

Clean Architecture Dependency Rule:
- Infrastructure Layer implements Application Layer interfaces
- Infrastructure Layer can depend on Domain and Application Layers
"""
