import os
import subprocess
import uuid

import pandas as pd


class KScanService:
    def scan(self, targets):
        output_file = f"{uuid.uuid4()}.txt"
        subprocess.run(["./libs/kscan/kscan", "-t", targets, "--scan", "-o", output_file])

        content = ''
        with open(output_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                content += line + '\n'
        os.remove(output_file)
        return content

    def json_to_markdown(self, data):
        df = pd.DataFrame(data)
        return df.to_markdown(index=False)
