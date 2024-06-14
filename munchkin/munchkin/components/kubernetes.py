import os

from dotenv import load_dotenv

load_dotenv()

KUBE_CONFIG_FILE = os.getenv("KUBE_CONFIG_FILE")
