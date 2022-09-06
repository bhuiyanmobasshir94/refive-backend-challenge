import tempfile
from io import BytesIO
from pathlib import Path

import fitz
import requests
from django.core.files.base import File


def convert_plain_txt_to_pdf_page(text):
    third_part_url = (
        "https://api.products.aspose.com/words/conversion/runcode/?outputType=pdf"
    )
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    }
    response = requests.post(
        third_part_url, headers=headers, files={"0": ("receipt.txt", text)}
    )
    with tempfile.TemporaryDirectory() as tmpdirname:
        temp_dir = Path(tmpdirname)
        file_name = temp_dir / "pdf.pdf"

        with open(file_name, "wb") as pdf:
            pdf.write(response.content)

        doc = fitz.open(file_name)
        page = doc[0]
        return page, doc


def get_list(page, separators=["---"]):
    blocks = page.get_text("dict", flags=11)["blocks"]
    bbox_list = []
    text_list = []
    for b in blocks:
        for l in b["lines"]:
            for s in l["spans"]:
                separator_found = False
                for separator in separators:
                    if separator in s["text"]:
                        separator_found = True
                        continue
                if separator_found:
                    continue
                r = fitz.Rect(s["bbox"])
                page.add_underline_annot(r)
                bbox_list.append(s["bbox"])
                text_list.append(s["text"])
    return bbox_list, text_list


def get_cluster(bbox_list, text_list):
    bbox_cluster = []
    bbox_sub_cluster = []
    text_cluster = []
    text_sub_cluster = []
    for index, bbox in enumerate(bbox_list):
        if index == (len(bbox_list) - 1):
            bbox_cluster.append(bbox_sub_cluster)
            text_cluster.append(text_sub_cluster)
            continue

        if index + 1 < len(bbox_list):
            dist = abs(bbox_list[index][3] - bbox_list[index + 1][1])
            if dist < 5:
                if bbox_list[index] not in bbox_sub_cluster:
                    bbox_sub_cluster.append(bbox_list[index])
                    text_sub_cluster.append(text_list[index])
                if bbox_list[index + 1] not in bbox_sub_cluster:
                    bbox_sub_cluster.append(bbox_list[index + 1])
                    text_sub_cluster.append(text_list[index + 1])
            else:
                bbox_cluster.append(bbox_sub_cluster)
                bbox_sub_cluster = []
                bbox_sub_cluster.append(bbox_list[index + 1])

                text_cluster.append(text_sub_cluster)
                text_sub_cluster = []
                text_sub_cluster.append(text_list[index + 1])
    return bbox_cluster, text_cluster


def get_coords(instance, separators=["---"]):
    text = instance.receipt
    page, doc = convert_plain_txt_to_pdf_page(text)
    bbox_list, text_list = get_list(page, separators=["---"])
    bbox_cluster, text_cluster = get_cluster(bbox_list, text_list)
    block_list = []
    for val in bbox_cluster:
        y0 = val[0][1]
        y1 = val[-1][3]
        x0, x1 = 0, 0
        higest_dist = 0
        for v in val:
            dist = abs(v[0] - v[2])
            if dist > higest_dist:
                higest_dist = dist
                x0 = v[0]
                x1 = v[2]
        cluster = (x0, y0, x1, y1)
        bbox = {
            "begin_row": cluster[0],
            "begin_col": cluster[1],
            "end_row": cluster[2],
            "end_col": cluster[3],
        }

        block_list.append(bbox)
        r = fitz.Rect(cluster)
        page.add_rect_annot(r)

    with tempfile.TemporaryDirectory() as tmpdirname:
        temp_dir = Path(tmpdirname)
        name = instance.receipt.name.split("/")[-1].replace(".txt", ".pdf")
        file_name = temp_dir / name

        doc.save(file_name)
        pdf = open(file_name, "rb")
        instance.marked_pdf.save(name, File(BytesIO(pdf.read())), save=True)

    instance.text_clusters = text_cluster
    instance.bbox_clusters = bbox_cluster
    instance.blocks = block_list
    instance.save()

    return {"blocks": block_list}
