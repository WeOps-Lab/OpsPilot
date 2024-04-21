import json
import os
import subprocess
import uuid

import pandas as pd


class KScanService:
    def scan(self, targets):
        output_file = f"{uuid.uuid4()}.json"
        subprocess.run(["./libs/kscan/kscan", "-t", targets, "--scan", "-oJ", output_file])
        with open(output_file, 'r') as f:
            data = json.load(f)
        os.remove(output_file)
        return data

    def json_to_markdown(self, data):
        df = pd.DataFrame(data)
        return df.to_markdown(index=False)
