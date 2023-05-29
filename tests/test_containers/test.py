from pathlib import Path

import requests

from wiremock.testing.testcontainer import WireMockContainer


def test_start_container():

    wm = (
        WireMockContainer()
        .with_exposed_ports(8080)
        .with_mapping(
            "hello-world.json",
            {
                "request": {"method": "GET", "url": "/hello"},
                "response": {"status": 200, "body": "hello"},
            },
        )
        .with_mapping(
            "hello-world-file.json",
            {
                "request": {"method": "GET", "url": "/hello2"},
                "response": {"status": 200, "bodyFileName": "hello.json"},
            },
        )
        .with_mapping(
            "hello-world-transformer.json",
            {
                "request": {"method": "POST", "url": "/hello3"},
                "response": {
                    "status": 201,
                    "headers": {"content-type": "application/json"},
                    "jsonBody": {"message": "Hello, $(name)!"},
                    "transformers": ["json-body-transformer"],
                },
            },
        )
        .with_file("hello.json", {"message": "Hello World !"})
        .with_cli_arg("--verbose", "")
        .with_cli_arg("--root-dir", "/home/wiremock")
        .with_extension(
            "com.ninecookies.wiremock.extensions.JsonBodyTransformer",
            Path("extensions/wiremock-body-transformer-1.1.3.jar"),
        )
        .with_env("JAVA_OPTS", "-Djava.net.preferIPv4Stack=true")
    )
    with wm:
        resp1 = requests.get(wm.get_url("/hello"))
        resp2 = requests.get(wm.get_url("/hello2"))
        resp3 = requests.post(wm.get_url("/hello3"), json={"name": "John Doe"})
        assert resp1.status_code == 200
        assert resp1.content == b"hello"
        assert resp2.status_code == 200
        assert resp2.content == b'{"message": "Hello World !"}'
        assert resp3.status_code == 201
        assert resp3.content == b'{"message": "Hello, John Doe"}'
