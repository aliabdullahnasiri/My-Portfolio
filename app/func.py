import os
import pathlib
import re
import subprocess
import uuid
from datetime import date
from operator import call
from typing import List, Union

import pytesseract
import requests
from flask import render_template
from pdf2image import convert_from_path
from PIL import Image
from pypdf import PdfReader

from app.config import Config
from app.models.file import File


def validate_uid(uid: str) -> bool:
    return bool(re.match(Config.UID_PATTERN, uid))


def get_file(id: int) -> Union[File, None]:
    return File.query.filter_by(id=id).first()


def get_file_url(id: int) -> Union[str, None]:
    file = File.query.filter_by(id=id).first()

    if file:
        return file.file_url


def render_td(col_id: str, obj, max_length: int = 64) -> str:
    dct = obj.to_dict()

    dct.setdefault("obj_{}".format(obj.__class__.__name__.lower()), obj)

    for TEMP in Config.TD_TEMPS:
        if col_id.startswith(let := "temp_"):
            col_id = col_id[len(let) :]

        if col_id == TEMP.name.split(chr(46)).pop(0):
            try:
                return render_template(
                    f"admin/components/tables/td/{TEMP.name}",
                    **{col_id: getattr(obj, col_id)},
                )
            except AttributeError as _:
                pass

            return render_template(f"admin/components/tables/td/{TEMP.name}", **dct)

    if hasattr(obj, attr := f"display_{col_id}"):
        return getattr(obj, attr)

    val = dct.get(col_id, "N/A")

    if hasattr(obj, col_id) and (attr := getattr(obj, col_id)) and type(attr) is date:
        val = call(getattr(obj, "display_date"), col_id, 0)

    if not val:
        val = "N/A"

    if type(val) == str and len(val) > max_length:
        return "{}...".format(val[slice(max_length)])

    return val


def __import_all__(path: str) -> None:
    ext = ".py"
    for module in pathlib.Path(path).glob(f"*{ext}"):
        __import__(
            re.sub(
                re.compile(rf"{ext}$"),
                "",
                f"{path.replace(chr(47), chr(46))}{chr(46)}{module.name}",
            )
        )


def generate_certificate_preview(
    pdf_path, output_path, width: int = 600, height: int = 400
):
    TARGET_SIZE = (width, height)
    pages = convert_from_path(pdf_path, dpi=200)
    img = pages[0]

    # keep aspect ratio
    img.thumbnail(TARGET_SIZE)

    bg_color = img.getpixel((10, 10))

    # create background canvas
    background = Image.new("RGB", TARGET_SIZE, bg_color)

    # center the image
    x = (TARGET_SIZE[0] - img.width) // 2
    y = (TARGET_SIZE[1] - img.height) // 2

    background.paste(img, (x, y))

    background.save(output_path, "JPEG", quality=90)


def extract_credential_urls(pdf: pathlib.Path) -> List[str]:
    """
    Extracts all URLs from a PDF file, including text URLs and clickable annotation URLs.

    Args:
        pdf (pathlib.Path): Path to the PDF file.

    Returns:
        list: A list of URLs found in the PDF.
    """
    urls = []

    try:
        reader = PdfReader(pdf)

        for page in reader.pages:
            text = page.extract_text() or ""
            urls.extend(re.findall(r"https?://\S+", text))

            if "/Annots" in page:
                for annot in page["/Annots"]:
                    obj = annot.get_object()
                    if "/A" in obj and "/URI" in obj["/A"]:
                        urls.append(obj["/A"]["/URI"])

        if not urls:
            images = convert_from_path(pdf)
            for image in images:
                text = pytesseract.image_to_string(image).replace(" ", "")
                urls.extend(re.findall(r"(https?://\S+|[\w.-]+/\S+)", text))

        normalized_urls = []
        for url in urls:
            url = url.strip().replace(" ", "")
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "https://" + url

            normalized_urls.append(url)

        return normalized_urls

    except Exception as e:
        print(f"Error reading {pdf}: {e}")
        return []


def is_url_alive(url, timeout=5):
    """
    Check if a URL returns HTTP status code 200.

    Args:
        url (str): The URL to check.
        timeout (int): Maximum seconds to wait for response (default 5s).

    Returns:
        bool: True if status code is 200, False otherwise.
    """
    try:
        # Make a HEAD request first (faster than GET)
        response = requests.head(url, allow_redirects=True, timeout=timeout)

        # Some servers may not allow HEAD requests, fallback to GET
        if response.status_code != 200:
            response = requests.get(url, allow_redirects=True, timeout=timeout)

        return response.status_code == 200

    except requests.RequestException:
        # Catch all request-related errors (connection error, timeout, etc.)
        return False


def generate_pdf(latex_content: str) -> bytes:
    temp_dir = f"/tmp/{uuid.uuid4()}"
    os.makedirs(temp_dir, exist_ok=True)

    tex_path = os.path.join(temp_dir, "main.tex")

    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(latex_content)

    for _ in range(2):
        subprocess.run(
            ["pdflatex", "main.tex"],
            cwd=temp_dir,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    pdf_path = os.path.join(temp_dir, "main.pdf")

    data = b""

    with open(pdf_path, "rb") as f:
        data = f.read()

    for file in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, file))

    os.rmdir(temp_dir)

    return data
