# Steps to set up Chroma

1. Start Docker

2. Pull the image from Chroma
> docker pull chromadb/chroma

3. RUN:
> docker run -d -p 8000:8000 --name chroma chromadb/chroma

References:
- [Chroma AWS Deployment](https://docs.trychroma.com/deployment/aws)