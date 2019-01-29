import inspect

import xlrd
import xlsxwriter
from django.conf import settings
import datetime

from bitxconvert.convert.tools import create_tmp_file
from bitxconvert.convert.utils.convert_date import get_date_time
from bitxconvert.utils.exceptions import IncorrectExchangeException

COL_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
new_row = 1
buy_orders = 0
sell_orders = 0


def get_bittrex_version(files):
    # Create and open new file
    tmp_file = create_tmp_file()
    new_wb = xlsxwriter.Workbook(tmp_file['file_path'])
    new_sheet = new_wb.add_worksheet()
    bold = new_wb.add_format({'bold': 1})
    float_format = new_wb.add_format()
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
        convert_rows(sheet, new_sheet, float_format)

    new_wb.close()

    return tmp_file


def get_base_currency(markets):
    market = markets.split('-', 1)[0]
    if "USDT" == market:
        return "USDT"
    if "USD" == market:
        return "USD"
    if "BTC" == market:
        return "BTC"
    if "ETH" == market:
        return "ETH"
    if "BNB" == market:
        return "BNB"
    if "TUSD" == market:
        return "TUSD"
    if "PAX" == market:
        return "PAX"
    if "USDC" == market:
        return "USDC"
    if "XRP" == market:
        return "XRP"


def get_currency_from_market(market):
    # market = markets.split('-', 1)[-1]
    if "USDT" in market[:-4]:
        return market.split('-', 1)[-1]
    if "USD" in market[:-3]:
        return market.split('-', 1)[-1]
    if "BTC" in market[:-3]:
        return market.split('-', 1)[-1]
    if "ETH" in market[:-3]:
        return market.split('-', 1)[-1]
    if "BNB" in market[:-3]:
        return market.split('-', 1)[-1]
    if "TUSD" in market[:-4]:
        return market.split('-', 1)[-1]
    if "PAX" in market[:-3]:
        return market.split('-', 1)[-1]
    if "USDC" in market[:-4]:
        return market.split('-', 1)[-1]
    if "XRP" in market[:-3]:
        return market.split('-', 1)[-1]


def get_currency(market, fee_coin):
    return market.replace(fee_coin, "")


def convert_rows(sheet, new_sheet, float_format):
    global buy_orders
    global sell_orders

    for row in range(1, sheet.nrows):
        if sheet.cell_value(row, 2) == "SELL" or "LIMIT_SELL":
            coin = get_base_currency(sheet.cell_value(row, 1))
            coin2 = get_currency_from_market(sheet.cell_value(row, 1))
            if is_btc(coin, sheet.cell_value(row, 3)):
                values = {
                    'date': get_date_time(sheet.cell_value(row, 8)),
                    'type': "SELL",
                    'recv': sheet.cell_value(row, 3),
                    'currency1': coin2,
                    'sent': sheet.cell_value(row, 4),
                    'currency2': coin,
                    'price': sheet.cell_value(row, 6),
                    'fee': sheet.cell_value(row, 5),
                    'fee_coin': coin
                }
            else:
                values = {
                    'date': get_date_time(sheet.cell_value(row, 8)),
                    'type': "SELL",
                    'recv': sheet.cell_value(row, 4),
                    'currency1': coin,
                    'sent': sheet.cell_value(row, 3),
                    'currency2': coin2,
                    'price': sheet.cell_value(row, 6),
                    'fee': sheet.cell_value(row, 5),
                    'fee_coin': coin2
                }
            sell_orders = sell_orders + 1
            write_rows(new_sheet, values, float_format)
        if sheet.cell_value(row, 2) == "BUY" or "LIMIT_BUY":
            coin = get_base_currency(sheet.cell_value(row, 1))
            coin2 = get_currency_from_market(sheet.cell_value(row, 1))
            if is_btc(coin, sheet.cell_value(row, 3)):
                values = {
                    'date': get_date_time(sheet.cell_value(row, 8)),
                    'type': "BUY",
                    'recv': sheet.cell_value(row, 3),
                    'currency1': coin2,
                    'sent': sheet.cell_value(row, 4),
                    'currency2': coin,
                    'price': sheet.cell_value(row, 6),
                    'fee': sheet.cell_value(row, 5),
                    'fee_coin': coin
                }
            else:
                values = {
                    'date': get_date_time(sheet.cell_value(row, 8)),
                    'type': "BUY",
                    'recv': sheet.cell_value(row, 3),
                    'currency1': coin2,
                    'sent': sheet.cell_value(row, 4),
                    'currency2': coin,
                    'price': sheet.cell_value(row, 6),
                    'fee': sheet.cell_value(row, 5),
                    'fee_coin': coin2
                }
            buy_orders = buy_orders + 1
            write_rows(new_sheet, values, float_format)


def write_rows(new_sheet, values, float_format):
    # start from the first row below the headers
    col = 0
    global new_row

    float_format.set_num_format('0.00000000')

    new_sheet.write_string(new_row, col, values['date'])
    new_sheet.write_string(new_row, col + 1, values['type'])
    new_sheet.write_number(new_row, col + 2, values['recv'], cell_format=float_format)
    new_sheet.write_string(new_row, col + 3, values['currency1'])
    new_sheet.write_number(new_row, col + 4, values['sent'], cell_format=float_format)
    new_sheet.write_string(new_row, col + 5, values['currency2'])
    new_sheet.write_number(new_row, col + 6, values['price'], cell_format=float_format)
    new_sheet.write_number(new_row, col + 7, values['fee'], cell_format=float_format)
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


def is_btc(coin, amount):
    if coin == "BTC":
        if settings.CONVERT_BTC_LIMIT < amount:
            return True
        else:
            return False


# def floatHourToTime(fh):
#     h, r = divmod(fh, 1)
#     m, r = divmod(r*60, 1)
#     return (
#         int(h),
#         int(m),
#         int(r*60),
#     )
#
#
# def get_date_time(value):
#     dt = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + int(value) - 2)
#     hour, minute, second = floatHourToTime(value % 1)
#     dt = dt.replace(hour=hour, minute=minute, second=second)
#     dt_str = dt.astimezone(pytz.utc)
#     return dt_str.strftime("%Y-%m-%d %H:%M:%S")
