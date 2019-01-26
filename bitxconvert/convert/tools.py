import uuid
from django.conf import settings
import xlsxwriter
import csv


def create_tmp_name():
    return str(uuid.uuid4())


def create_tmp_file_path(file_name):
    return "{}{}.xlsx".format(settings.TMP_FILE_LOC, file_name)


def create_tmp_file():
    tmp_file_name = create_tmp_name()
    file_path = "{}/{}.xlsx".format(settings.TMP_FILE_LOC, tmp_file_name)
    workbook = xlsxwriter.Workbook(file_path)
    workbook.close()
    return {
        "file": tmp_file_name,
        "file_path": file_path
    }

