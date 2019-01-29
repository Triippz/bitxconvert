"""
Standard format for Bitcoin.tax CSV files


Date (date and time as YYYY-MM-DD HH:mm:ss Z)
Source (optional, such as an exchange name like MtGox or gift, donation, etc)
Action (BUY, SELL or FEE)
Symbol (BTC, LTC, DASH, etc)
Volume (number of coins traded - ignore if FEE)
Currency (specify currency such as USD, GBP, EUR or coins, BTC or LTC)
Price (price per coin in Currency or blank for lookup - ignore if FEE)
Fee (any additional costs of the trade)
FeeCurrency (currency of fee if different than Currency)


Date,Action,Source,Symbol,Volume,Price,Currency,Fee
2014-01-01 13:00:00 -0800,BUY,Online,BTC,1,500,USD,5.50
"""
import xlrd
import csv
import os

from django.conf import settings
from bitxconvert.convert.tools import create_tmp_name


def get_bitcointax_version(file_info, exchange):
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
        filewriter.writerow(["Date", "Source", "Action", "Symbol", "Volume", "Currency", "Price", "Fee", "Fee Currency"])

        for row in range(1, sheet.nrows):
            if sheet.cell_value(row, 0) is not "":
                if sheet.cell_value(row, 1) == "SELL":
                    date = sheet.cell_value(row, 0)  # date
                    action = sheet.cell_value(row, 1)  # action
                    symbol = sheet.cell_value(row, 5)  # symbol
                    volume = sheet.cell_value(row, 4)  # volume
                    price = sheet.cell_value(row, 6)  # price
                    currency = sheet.cell_value(row, 3)  # currency
                    fee = sheet.cell_value(row, 7)  # fee
                    fee_coin = sheet.cell_value(row, 8) # fee coin

                    filewriter.writerow([date, exchange, action, symbol, volume, price, currency, fee, fee_coin])
                    sell_orders += 1
                    total_orders += 1
                else:
                    output = [
                        sheet.cell_value(row, 0),  # date
                        exchange,                  # source
                        sheet.cell_value(row, 1),  # action
                        sheet.cell_value(row, 3),  # symbol
                        sheet.cell_value(row, 2),  # volume
                        sheet.cell_value(row, 6),  # price
                        sheet.cell_value(row, 5),  # currency
                        sheet.cell_value(row, 7),  # fee
                        sheet.cell_value(row, 8)  # fee coin
                    ]
                    filewriter.writerow(output)
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
