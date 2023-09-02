import random
import subprocess

import requests

base_images = [
    "alpine",
]  # only leave alpine here to quickly test script
base_image = random.choice(base_images)
# Get all tags for randomly selected base image from docker hub API
url = "https://hub.docker.com/v2/namespaces/library/repositories/{}/tags?page_size=100".format(
    base_image
)
# TODO: Iterate through all pages for all tags
tags_response = requests.get(url).json()
all_tags = []
for result in tags_response["results"]:
    all_tags.append(result["name"])
tag = random.choice(all_tags)
name = "test-{}-{}".format(base_image, tag)
print("Building image with base image: {} and tag: {}".format(base_image, tag))
build_command = "docker build -q --build-arg base_image={}:{} .".format(base_image, tag)


build_container = subprocess.run(build_command, shell=True, stdout=subprocess.PIPE)
print("> " + build_command)
print("Running container...")

run_command = "docker run --rm -p 80:80 -it -d --name {} {}".format(
    name, build_container.stdout.decode("utf-8").strip()
)

run_container = subprocess.run(
    run_command,
    shell=True,
)
subprocess.run(
    "docker cp ./entrypoint.sh {}:/entrypoint.sh".format(name),
    stdout=subprocess.PIPE,
    shell=True,
)
# res = subprocess.run("docker exec -it {} sh".format(name), shell=True)
# print(res)
subprocess.run(
    'docker exec -it {} sh -c "chmod +x ./entrypoint.sh && ./entrypoint.sh"'.format(
        name
    ),
    stdout=subprocess.PIPE,
    shell=True,
)

res = subprocess.run("docker exec -it {} sh".format(name), shell=True)
