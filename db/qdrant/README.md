# Qdrant - Vector DB

Singleton class implementation for Qdrant DB Client

## Getting started

1. Install and setup docker

2. Pull the qdrant image: <br>
> docker pull qdrant/qdrant

3. Run: <br>
> docker run -p 6333:6333 -p 6334:6334 -v $(pwd)/qdrant_storage:/qdrant/storage:z qdrant/qdrant
