import paramiko
from multiprocessing import Process
import requests
from PIL import Image
from io import BytesIO

username = "user"
password = "mdp"


def update_image():
    with open("memoire.txt", "r") as f:
        ip = f.readlines()[0][0:12]
    response = requests.get(f"http://{ip}:5000/capture")
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    return img


def _reboot():
    with open("memoire.txt", "r") as f:
        ip = f.readlines()[0][0:12]
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=username, password=password)
    stdin, stdout, stderr = client.exec_command("sudo reboot")
    stdout.channel.recv_exit_status()
    client.close()


def _shutdown():
    with open("memoire.txt", "r") as f:
        ip = f.readlines()[0][0:12]
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=username, password=password)
    stdin, stdout, stderr = client.exec_command("sudo shutdown -h now")
    stdout.channel.recv_exit_status()
    client.close()


def _lanceserveur():
    with open("memoire.txt", "r") as f:
        ip = f.readlines()[0][0:12]
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=username, password=password)

    stdin, stdout, stderr = client.exec_command(
        "export DISPLAY=:0 && /bin/python /home/tadoti/Desktop/cam/test.py"
    )
    stdout.channel.recv_exit_status()
    client.close()


def lanceserveur():
    process = Process(target=_lanceserveur)
    process.start()


def shutdown():
    process = Process(target=_shutdown)
    process.start()


def reboot():
    process = Process(target=_reboot)
    process.start()


def _commanderp5(string):
    with open("memoire.txt", "r") as f:
        ip = f.readlines()[0][0:12]
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=username, password=password)
    stdin, stdout, stderr = client.exec_command(string)
    stdout.channel.recv_exit_status()
    client.close()


def commanderp5(string):
    process = Process(target=lambda: _commanderp5(string))
    process.start()
