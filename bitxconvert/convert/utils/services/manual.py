"""
cryptoXconvert custom format

Date
Exchange
Order Type
Currency Received
Received Amount
Currency Sent
Sent Amount
Price
Fee
Fee Coin

"""

import xlrd
import csv
import os

from django.conf import settings
from bitxconvert.convert.tools import create_tmp_name


def get_manual_version(file_info, exchange):
    # create a new file
    download_file_info = create_download_file()

    # Open the tmp file
    wb = xlrd.open_workbook(filename=file_info['file_path'])
    sheet = wb.sheet_by_index(0)

    # write data to new csv and get information of the writes
    new_file_info = write_csv(sheet, download_file_info, exchange)

    os.remove(file_info['file_path'])
    return new_file_info


def write_csv(sheet, file_info, exchange):
    buy_orders = 0
    sell_orders = 0
    total_orders = 0

    csv.register_dialect("dialect", delimiter=',', quoting=csv.QUOTE_NONE)
    with open(file_info['file_path'], 'w', encoding="utf-8") as csvfile:
        filewriter = csv.writer(csvfile, dialect="dialect")
        filewriter.writerow(['Date (UTC)', 'Exchange', 'Order Type', 'Currency Received', 'Received Amount',
                             "Currency Sent", "Sent Amount", "Price", "Fee", "Fee Coin"])

        # with open(file_info['file_path'], 'wb') as csvfile:
        for row in range(1, sheet.nrows):
            if sheet.cell_value(row, 0) is not "":
                if sheet.cell_value(row, 1) == "SELL":
                    filewriter.writerow([
                        sheet.cell_value(row, 0), # Date
                        exchange,                 # Exchange
                        sheet.cell_value(row, 1), # Order Type
                        sheet.cell_value(row, 5), # Currency Received
                        sheet.cell_value(row, 4), # Received Amount
                        sheet.cell_value(row, 3), # Currency Sent
                        sheet.cell_value(row, 2), # Sent Amount
                        sheet.cell_value(row, 6), # Price
                        sheet.cell_value(row, 7), # Fee
                        sheet.cell_value(row, 8), # Fee Coin
                    ])
                    sell_orders += 1
                    total_orders += 1
                else:
                    filewriter.writerow([
                        sheet.cell_value(row, 0), # Date
                        exchange,                 # Exchange
                        sheet.cell_value(row, 1), # Order Type
                        sheet.cell_value(row, 3), # Currency Received
                        sheet.cell_value(row, 2), # Received Amount
                        sheet.cell_value(row, 5), # Currency Sent
                        sheet.cell_value(row, 4), # Sent Amount
                        sheet.cell_value(row, 6), # Price
                        sheet.cell_value(row, 7), # Fee
                        sheet.cell_value(row, 8), # Fee Coin
                    ])
                    sell_orders += 1
                    total_orders += 1

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
    file_path = "{}/{}".format(settings.DOWNLOAD_FILE_LOC, file_name)
    return {
        "file": file_name,
        "file_path": file_path
    }
