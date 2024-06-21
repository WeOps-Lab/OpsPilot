import os
import subprocess


def markdown_to_pdf_pandoc(markdown_file_path, output_pdf_path):
    # Call pandoc to convert the markdown to pdf
    result = subprocess.run(
        [
            "pandoc",
            "-s",
            markdown_file_path,
            "-o",
            output_pdf_path,
            "--pdf-engine",
            "xelatex",
            "-V",
            "CJKmainfont=Microsoft YaHei",
            "--template",
            f"{os.path.dirname(os.path.abspath(__file__))}/eisvogel.latex",
            "--listings",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise Exception(f"Error converting markdown to pdf: {result.stderr}")
