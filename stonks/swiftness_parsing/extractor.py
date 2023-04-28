import datetime
import re
import zipfile
from typing import Optional

import xlrd
from io import BytesIO

from stonks.swiftness_parsing.normalizer import normalize_swiftness_dict


def xls_to_dict(zip_data: BytesIO, password: Optional[bytes]):
    archive = zipfile.ZipFile(zip_data)
    xls_name = [f for f in archive.filelist if f.filename.endswith(".xls")][0]
    worksheet_data = archive.open(xls_name, pwd=password).read()
    worksheet = xlrd.open_workbook_xls(file_contents=worksheet_data)
    data = {}

    for sheet_name in worksheet.sheet_names():
        sheet = worksheet.sheet_by_name(sheet_name)
        sheet_data = []

        # Get headers
        headers = []
        for i in range(sheet.ncols):
            val: str = sheet.cell_value(0, i)
            if val.strip() == "":
                break
            headers.append(val)

        # Get data
        for i in range(1, sheet.nrows):
            row_data = {}
            for j, header in enumerate(headers):
                row_data[header] = sheet.cell_value(i, j)

            sheet_data.append(row_data)

        data[sheet_name] = sheet_data

    return data, xls_name.filename


def extract_swiftness_zip(zip_data, zip_pass=None):
    data, filename = xls_to_dict(BytesIO(zip_data), zip_pass)
    normalized = normalize_swiftness_dict(data)

    # Example: 111222333_202302091340.xls
    # Outputs: 2023,02,09,13,40
    xls_date = re.match(r".*_(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})\.xls", filename).groups()
    for row in normalized["insurances"]:
        row["date_of_validity"] = datetime.date(int(xls_date[0]), int(xls_date[1]), int(xls_date[2]))

    return normalized
