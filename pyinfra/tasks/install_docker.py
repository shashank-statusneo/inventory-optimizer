from pyinfra import server


server.shell(
    name="Install Docker",
    commands=[
        "sudo dpkg --remove docker docker-engine docker.io containerd runc",
        "apt-get update -y",
        "curl -fsSL https://download.docker.com/linux/ubuntu/gpg > gpgkey",
    ],
    sudo=True,
)
