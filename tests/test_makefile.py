import subprocess
import unittest


class MakefileDockerTests(unittest.TestCase):
    def test_docker_build_defaults_to_amd64_platform(self):
        result = subprocess.run(
            ["make", "-n", "docker"],
            check=True,
            capture_output=True,
            text=True,
        )

        self.assertIn("docker build --platform linux/amd64", result.stdout)

    def test_docker_arm64_build_uses_arm64_platform_and_tags(self):
        result = subprocess.run(
            ["make", "-n", "docker-arm64"],
            check=True,
            capture_output=True,
            text=True,
        )

        self.assertIn("docker build --platform linux/arm64", result.stdout)
        self.assertIn("heifeng/webnut:latest-arm64", result.stdout)
        self.assertIn("-arm64", result.stdout)
