# Steps to set up Chroma

1. Start Docker

2. Pull the image from Chroma
> docker pull chromadb/chroma

3. Create a password file
> htpasswd -Bbn `user` `password` > chroma.htpasswd

> export CHROMA_SERVER_AUTH_CREDENTIALS_FILE="chroma.htpasswd" <br>
> export CHROMA_SERVER_AUTH_CREDENTIALS_PROVIDER="chromadb.auth.providers.HtpasswdFileServerAuthCredentialsProvider" <br>
> export CHROMA_SERVER_AUTH_PROVIDER="chromadb.auth.basic.BasicAuthServerProvider"

4. RUN:
> docker run -d -p 8000:8000 \
--name chroma \
-e CHROMA_SERVER_AUTH_CREDENTIALS_FILE="/config/chroma.htpasswd" \
-e CHROMA_SERVER_AUTH_CREDENTIALS_PROVIDER="chromadb.auth.providers.HtpasswdFileServerAuthCredentialsProvider" \
-e CHROMA_SERVER_AUTH_PROVIDER="chromadb.auth.basic.BasicAuthServerProvider" \
-v "$(pwd):/config" \
chromadb/chroma

References:
- [Chroma AWS Deployment](https://docs.trychroma.com/deployment/aws)
- [Chroma Auth](https://docs.trychroma.com/deployment/auth)