import random
import subprocess

import requests

base_images = [
    "alpine",
]  # only leave alpine here to quickly test script
base_image = random.choice(base_images)
# Get all tags for randomly selected base image from docker hub API
url = f"https://hub.docker.com/v2/namespaces/library/repositories/{base_image}/tags?page_size=100"
# TODO: Iterate through all pages for all tags
tags_response = requests.get(url).json()
all_tags = []
for result in tags_response["results"]:
    all_tags.append(result["name"])
tag = random.choice(all_tags)
# Container name, ex. test-alpine-3.12.0
container_name = f"test-{base_image}-{tag}"
print(f"Building image with base image: {base_image} and tag: {tag}")
build_command = f"docker build -q --build-arg base_image={base_image}:{tag} ."
build_container = subprocess.run(build_command, shell=True, stdout=subprocess.PIPE)
print(f"Running container {container_name}...")

run_command = f"docker run --rm -p 80:80 -it -d --name {container_name} { build_container.stdout.decode('utf-8').strip()}"
# Run container
container_process = subprocess.run(
    run_command,
    shell=True,
)
# Copy entrypoint script into container
subprocess.run(
    f"docker cp ./entrypoint.sh {container_name}:/entrypoint.sh",
    stdout=subprocess.PIPE,
    shell=True,
)

# Make entrypoint script executable and run it
subprocess.run(
    f'docker exec -it {container_name} sh -c "chmod +x ./entrypoint.sh && ./entrypoint.sh"',
    stdout=subprocess.PIPE,
    shell=True,
)
# Open shell in container
res = subprocess.run(f"docker exec -it {container_name} sh", shell=True)
