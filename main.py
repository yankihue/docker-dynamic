import random
import subprocess

import requests

base_images = ["debian", "ubuntu", "alpine"]
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

build_container = subprocess.run(
    "docker build -q --build-arg base_image={}:{} .".format(
        base_image,
        tag,
    ),
    shell=True,
    capture_output=True,
)
run_container = subprocess.run(
    "docker run --rm -p 80:80 -it {}".format(
        build_container.stdout.decode("utf-8").strip()
    ),
    shell=True,
    capture_output=True,
)
