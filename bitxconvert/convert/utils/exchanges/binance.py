import inspect

import xlrd
import xlsxwriter
import datetime
from bitxconvert.convert.tools import create_tmp_file
from bitxconvert.utils.exceptions import IncorrectExchangeException

COL_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
new_row = 1
buy_orders = 0
sell_orders = 0


def get_binance_version(files):
    # Create and open new file
    tmp_file = create_tmp_file()
    new_wb = xlsxwriter.Workbook(tmp_file['file_path'])
    new_sheet = new_wb.add_worksheet()
    bold = new_wb.add_format({'bold': 1})
    new_sheet.set_column(1, 1, 15)

    # Start writing from old file
    for file in files:
        # Open file in memory
        try:
            wb = xlrd.open_workbook(file_contents=file.read())
        except Exception as e:
            print("{} -- Error: {}-->{}".format(datetime.datetime.now(), inspect.stack()[0][3], e))
            raise IncorrectExchangeException("You attempted to upload a file which is not supported for the current "
                                             "exchange. If you think this is a mistake, please contact us.")
        sheet = wb.sheet_by_index(0)

        write_col_names(new_sheet, bold)
        convert_rows(sheet, new_sheet)

    new_wb.close()
    print("Parsed BINANCE FILE")
    return tmp_file


def get_base_currency(market):
    if "USDT" in market[-4:]:
        return "USDT"
    if "BTC" in market[-3:]:
        return "BTC"
    if "ETH" in market[-3:]:
        return "ETH"
    if "BNB" in market[-3:]:
        return "BNB"
    if "TUSD" in market[-4:]:
        return "TUSD"
    if "PAX" in market[-3:]:
        return "PAX"
    if "USDC" in market[-4:]:
        return "USDC"
    if "XRP" in market[-3:]:
        return "XRP"


def get_currency_from_market(market):
    if "USDT" in market[-4:]:
        return market[:-4]
    if "BTC" in market[-3:]:
        return market[:-3]
    if "ETH" in market[-3:]:
        return market[:-3]
    if "BNB" in market[-3:]:
        return market[:-3]
    if "TUSD" in market[-4:]:
        return market[:-4]
    if "PAX" in market[-3:]:
        return market[:-3]
    if "USDC" in market[-4:]:
        return market[:-4]
    if "XRP" in market[-3:]:
        return market[:-3]


def get_currency(market, fee_coin):
    return market.replace(fee_coin, "")


def convert_rows(sheet, new_sheet):
    global buy_orders
    global sell_orders

    for row in range(0, sheet.nrows):
        if sheet.cell_value(row, 2) == "SELL":
            if sheet.cell_value(row, 7) == "BNB":
                coin = sheet.cell_value(row, 7)
            else:
                coin = sheet.cell_value(row, 7)
            values = {
                'date': sheet.cell_value(row, 0),
                'type': sheet.cell_value(row, 2),
                'recv': sheet.cell_value(row, 5),
                'currency1': coin,
                'sent': sheet.cell_value(row, 4),
                'currency2': get_currency(sheet.cell_value(row, 1), sheet.cell_value(row, 7)),
                'price': sheet.cell_value(row, 3),
                'fee': sheet.cell_value(row, 6),
                'fee_coin': sheet.cell_value(row, 7)
            }
            sell_orders = sell_orders + 1
            write_rows(new_sheet, values)
        if sheet.cell_value(row, 2) == "BUY":
            if "BNB" not in str(sheet.cell_value(row, 7)):
                values = {
                    'date': sheet.cell_value(row, 0),
                    'type': sheet.cell_value(row, 2),
                    'recv': sheet.cell_value(row, 5),
                    'currency1': get_currency(sheet.cell_value(row, 1), sheet.cell_value(row, 7)),
                    'sent': sheet.cell_value(row, 4),
                    'currency2': sheet.cell_value(row, 7),
                    'price': sheet.cell_value(row, 3),
                    'fee': sheet.cell_value(row, 6),
                    'fee_coin': sheet.cell_value(row, 7)
                }
                buy_orders = buy_orders + 1
                write_rows(new_sheet, values)
            else:
                coin = get_base_currency(sheet.cell_value(row, 1))
                coin2 = get_currency_from_market(sheet.cell_value(row, 1))
                values = {
                    'date': sheet.cell_value(row, 0),
                    'type': sheet.cell_value(row, 2),
                    'recv': sheet.cell_value(row, 5),
                    'currency1': coin,
                    'sent': sheet.cell_value(row, 4),
                    'currency2': coin2,
                    'price': sheet.cell_value(row, 3),
                    'fee': sheet.cell_value(row, 6),
                    'fee_coin': sheet.cell_value(row, 7)
                }
                buy_orders = buy_orders + 1
                write_rows(new_sheet, values)


def write_rows(new_sheet, values):
    # start from the first row below the headers
    col = 0
    global new_row

    new_sheet.write_string(new_row, col, values['date'])
    new_sheet.write_string(new_row, col + 1, values['type'])
    new_sheet.write_string(new_row, col + 2, values['recv'])
    new_sheet.write_string(new_row, col + 3, values['currency1'])
    new_sheet.write_string(new_row, col + 4, values['sent'])
    new_sheet.write_string(new_row, col + 5, values['currency2'])
    new_sheet.write_string(new_row, col + 6, values['price'])
    new_sheet.write_string(new_row, col + 7, values['fee'])
    new_sheet.write_string(new_row, col + 8, values['fee_coin'])

    new_row = new_row + 1


def write_col_names(new_sheet, bold):
    new_sheet.write("A1", "Date", bold)
    new_sheet.write("B1", "Type", bold)
    new_sheet.write("C1", "Recv", bold)
    new_sheet.write("D1", "Currency", bold)
    new_sheet.write("E1", "Sent", bold)
    new_sheet.write("F1", "Currency", bold)
    new_sheet.write("G1", "Price", bold)
    new_sheet.write("H1", "Fee", bold)
    new_sheet.write("I1", "Fee Coin", bold)
