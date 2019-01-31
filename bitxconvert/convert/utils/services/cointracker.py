import xlrd
import csv
import os

from django.conf import settings
from bitxconvert.convert.tools import create_tmp_name


def get_cointracker_version(file_info):
    # create a new file
    download_file_info = create_download_file()

    # Open the tmp file
    wb = xlrd.open_workbook(filename=file_info['file_path'])
    sheet = wb.sheet_by_index(0)

    # write data to new csv and get information of the writes
    new_file_info = write_csv(sheet, download_file_info)

    os.remove(file_info['file_path'])
    return new_file_info


def write_csv(sheet, file_info):
    buy_orders = 0
    sell_orders = 0
    total_orders = 0

    csv.register_dialect("dialect", delimiter=',', quoting=csv.QUOTE_NONE)
    with open(file_info['file_path'], 'w', encoding="utf-8") as csvfile:
        filewriter = csv.writer(csvfile, dialect="dialect")
        filewriter.writerow(['Date', 'Received Quantity', 'Currency', 'Sent Quantity', 'Currency'])

        # with open(file_info['file_path'], 'wb') as csvfile:
        for row in range(1, sheet.nrows):
            if sheet.cell_value(row, 0) is not "":
                filewriter.writerow([
                    sheet.cell_value(row, 0),
                    sheet.cell_value(row, 2),
                    sheet.cell_value(row, 3),
                    sheet.cell_value(row, 4),
                    sheet.cell_value(row, 5)
                ])
                total_orders += 1
                if "BUY" in sheet.cell_value(row, 1):
                    buy_orders += 1
                else:
                    sell_orders += 1

    return {
        'buy_orders': buy_orders,
        'sell_orders': sell_orders,
        'total_orders': total_orders,
        'file_name': file_info['file'],
        'file_path': file_info['file_path'],
        'file': csvfile
    }


def create_download_file():
    file_name = "{}.csv".format(create_tmp_name())
    file_path = "{}/{}".format(settings.TMP_FINAL_FILE_LOC, file_name)
    return {
        "file": file_name,
        "file_path": file_path
    }
