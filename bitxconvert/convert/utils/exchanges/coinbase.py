import inspect

import xlrd
import xlsxwriter
import datetime

from bitxconvert.convert.tools import create_tmp_file
from bitxconvert.convert.utils.convert_date import get_date_time
from bitxconvert.utils.exceptions import IncorrectExchangeException

COL_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
new_row = 1
buy_orders = 0
sell_orders = 0


def get_coinbase_version(files):
    # Create and open new file
    tmp_file = create_tmp_file()
    new_wb = xlsxwriter.Workbook(tmp_file['file_path'])
    new_sheet = new_wb.add_worksheet()
    bold = new_wb.add_format({'bold': 1})
    new_sheet.set_column(1, 1, 15)
    float_format = new_wb.add_format()

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
        convert_rows(sheet, new_sheet, float_format)

    new_wb.close()

    return tmp_file


def convert_rows(sheet, new_sheet, float_format):
    global buy_orders
    global sell_orders

    header_hit = False

    for row in range(0, sheet.nrows):
        if header_hit:
            if sheet.cell_value(row, 1) == "Sell":
                values = {
                    'date': get_date_time(sheet.cell_value(row, 0)),
                    'type': "SELL",
                    'recv': sheet.cell_value(row, 5),
                    'currency1': sheet.cell_value(row, 2),
                    'sent': sheet.cell_value(row, 3),
                    'currency2': "USD",
                    'price': sheet.cell_value(row, 4),
                    'fee_coin': "USD"
                }
                sell_orders = sell_orders + 1
                write_rows(new_sheet, values, float_format)
            if sheet.cell_value(row, 1) == "Buy":
                values = {
                    'date': get_date_time(sheet.cell_value(row, 0)),
                    'type': "BUY",
                    'recv': sheet.cell_value(row, 3),
                    'currency1': "USD",
                    'sent': sheet.cell_value(row, 5),
                    'currency2': sheet.cell_value(row, 2),
                    'price': sheet.cell_value(row, 4),
                    'fee_coin': "USD"
                }
                buy_orders = buy_orders + 1
                write_rows(new_sheet, values, float_format)
        else:
            header_hit = is_header(row, sheet)


def is_header(row, sheet):
    """
    We Just need to test the first 2 columns to be safe
    :param row:
    :param sheet:
    :return:
    """
    if sheet.cell_value(row, 0) == "Timestamp" and sheet.cell_value(row, 1) == "Transaction Type":
        return True
    return False


def write_rows(new_sheet, values, float_format):
    # start from the first row below the headers
    col = 0
    global new_row
    float_format.set_num_format('0.00000000')

    new_sheet.write_string(new_row, col, values['date'])
    new_sheet.write_string(new_row, col + 1, values['type'])
    new_sheet.write_number(new_row, col + 2, values['recv'], float_format)
    new_sheet.write_string(new_row, col + 3, values['currency1'])
    new_sheet.write_number(new_row, col + 4, values['sent'], float_format)
    new_sheet.write_string(new_row, col + 5, values['currency2'])
    new_sheet.write_number(new_row, col + 6, values['price'], float_format)
    new_sheet.write_string(new_row, col + 7, "")
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


