import datetime

import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from asgiref.sync import sync_to_async


@sync_to_async
def create_record(user_id: int, price: int, full_name: str, gmail: str, phone="",
                  date=str(datetime.datetime.now().date())):
    sheet_id = '1HNvvkxLjMyP0INCSqwwKeOLEWW5mPodjAHaxhWYa284'
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    creds_json = 'google_api/credentials.json'
    values = [
        [user_id, date, price, full_name, gmail,
         phone]]
    creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(
        httplib2.Http())
    sheets = build('sheets', 'v4', http=creds_service)
    sheet = sheets.spreadsheets()
    sheet.values().append(
        spreadsheetId=sheet_id,
        range="Лист1!A1",
        valueInputOption="RAW",
        body={'values': values}).execute()
    return
