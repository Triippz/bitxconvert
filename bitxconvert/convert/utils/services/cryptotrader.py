"""
Timestamp (UTC) - The UTC timestamp of your trade (VERY IMPORTANT to ensure your dates are in UTC!!)
- Make sure to convert your exchange's local time to UTC.
- This should be in the format of: mm/dd/yyyy hh:mm:ss
Exchange - The exchange name of your trade
BUY/SELL - The type of trade (can be either "BUY" or "SELL")
- Not critical to calculation accuracy.
Coin Traded/Given - The symbol of the coin/currency "traded away"
- Given a trade with product, "BTC-USD" (BASE-QUOTE)
- For BUY trades, this will be the "QUOTE currency" (USD).
- For SELL trades, this will be the "BASE currency" (BTC).
Amount Traded/Given - The amount of currency that was traded away
- Include fees in this number.
Coin Received - The symbol of the coin/currency "received" for this trade
- Given a trade with product, BTC-USD (BASE-QUOTE)
- For BUY trades, this will be the "BASE currency" (BTC).
- For SELL trades, this will be the "QUOTE currency" (USD).
Amount Received - The amount of currency that was received (including fees)
"""

import xlrd
import csv
import os

from django.conf import settings
from bitxconvert.convert.tools import create_tmp_name


def get_cryptotrader_version(file_info, exchange):
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
        filewriter.writerow(['Timestamp (UTC)', 'Exchange', 'BUY/SELL', 'Coin Traded/Given', 'Amount Traded/Given',
                             "Coin Received", "Amount Received"])

        # with open(file_info['file_path'], 'wb') as csvfile:
        for row in range(1, sheet.nrows):
            if sheet.cell_value(row, 0) is not "":
                if sheet.cell_value(row, 1) == "SELL":
                    filewriter.writerow([
                        sheet.cell_value(row, 0), # Date
                        exchange,                 # Exchange
                        sheet.cell_value(row, 1), # BUY/SELL
                        sheet.cell_value(row, 5), # Coin Traded/Given
                        sheet.cell_value(row, 4), # Amount Traded/Given
                        sheet.cell_value(row, 3), # Coin Received
                        sheet.cell_value(row, 2)  # Amount Received
                    ])
                    sell_orders += 1
                    total_orders += 1
                else:
                    filewriter.writerow([
                        sheet.cell_value(row, 0),  # Date
                        exchange,  # Exchange
                        sheet.cell_value(row, 1),  # BUY/SELL
                        sheet.cell_value(row, 5),  # Coin Traded/Given
                        sheet.cell_value(row, 4),  # Amount Traded/Given
                        sheet.cell_value(row, 3),  # Coin Received
                        sheet.cell_value(row, 2)   # Amount Received
                    ])
                    buy_orders += 1
                    total_orders += 1

    csvfile.close()

    return {
        'buy_orders': buy_orders,
        'sell_orders': sell_orders,
        'total_orders': total_orders,
        'file_name': file_info['file'],
        'file_path': file_info['file_path']
    }


def create_download_file():
    file_name = "{}.csv".format(create_tmp_name())
    file_path = "{}/{}".format(settings.DOWNLOAD_FILE_LOC, file_name)
    return {
        "file": file_name,
        "file_path": file_path
    }
