from prefect import task
import docker
import os

def is_qdrant_running():
    client = docker.from_env()
    containers = client.containers.list(filters={"name": "qdrant"})
    return any(container.status == "running" for container in containers)

@task
def start_qdrant():
    client = docker.from_env()
    if not is_qdrant_running():
        client.images.pull("qdrant/qdrant")
        storage_path = os.path.join(os.getcwd(), "qdrant_storage")
        os.makedirs(storage_path, exist_ok=True)
        try:
            client.containers.run(
                "qdrant/qdrant",
                detach=True,
                ports={'6333/tcp': 6333, '6334/tcp': 6334},
                volumes={storage_path: {'bind': '/qdrant/storage', 'mode': 'z'}},
                name="qdrant",
                remove=True,
            )
            print("Qdrant container started.")
        except docker.errors.APIError as e:
            if "Conflict" in str(e):
                print("Container already exists, skipping creation.")
            else:
                raise e
    else:
        print("Qdrant is already running.")
