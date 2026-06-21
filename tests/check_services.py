import redis
from qdrant_client import QdrantClient


def main() -> None:
    qdrant = QdrantClient(host="localhost", port=6333)
    collections = qdrant.get_collections()

    cache = redis.Redis(host="localhost", port=6379, decode_responses=True)
    cache.set("vidsearch_setup_check", "ok")

    print("Qdrant OK:", collections)
    print("Redis OK:", cache.get("vidsearch_setup_check"))


if __name__ == "__main__":
    main()
