#!/usr/bin/env python3
import uvicorn
from fastapi import FastAPI

from nicegui import app, ui

VALID_USA_CANADA_MEXICO_PHONE_NUMBER_LENGTH = 10

# This example deliberately creates a separate FastAPI app and runs NiceGUI on top of it using `ui.run_with`.
# Please note that the `app` object from NiceGUI is also a FastAPI app.
# Often it is easier to stick to `ui.run` and use the `@app.get` etc. decorators to add normal FastAPI endpoints.
fastApiApp = FastAPI()


@fastApiApp.get('/')
def get_root():
    return {'message': 'Hello, FastAPI! Browse to /gui to see the NiceGUI app.'}

def sanitize_phone_number(text):
    global sanitizedPhoneNumber, invalidPhoneNumberLabel

    sanitizedPhoneNumber = text.replace(" ", "")
    sanitizedPhoneNumber = sanitizedPhoneNumber.replace("(", "")
    sanitizedPhoneNumber = sanitizedPhoneNumber.replace(")", "")
    sanitizedPhoneNumber = sanitizedPhoneNumber.replace(".", "")
    sanitizedPhoneNumber = sanitizedPhoneNumber.replace("-", "")
    sanitizedPhoneNumber = sanitizedPhoneNumber.replace("+", "")

    invalidPhoneNumberLabel.visible = False

    return sanitizedPhoneNumber


@ui.page('/')
def show():

    invalidPhoneNumberLabel = ui.label("ERROR LABEL")
    invalidPhoneNumberLabel.visible = False
    userInputTextBox = ui.input(label='Enter your 10 digit phone number', placeholder='e.g. 719.555.1234', \
                    on_change=lambda e: invalidPhoneNumberLabel.set_text(sanitize_phone_number(e.value)), \
                    validation={'Phone number is too long': lambda value: len(sanitizedPhoneNumber) <= VALID_USA_CANADA_MEXICO_PHONE_NUMBER_LENGTH}).classes('w-1/5')  # Length incluses + symbol at start of phone number

    #userInputButton = ui.button('NEXT', on_click=lambda e: send_otp_password(sanitizedPhoneNumber, invalidPhoneNumberLabel, enterPhoneNumberGrid)))

    # NOTE dark mode will be persistent for each user across tabs and server restarts
    ui.dark_mode().bind_value(app.storage.user, 'dark_mode')
    ui.checkbox('dark mode').bind_value(app.storage.user, 'dark_mode')


ui.run_with(
    fastApiApp,
    dark=True,
    mount_path='/home',  # NOTE this can be omitted if you want the paths passed to @ui.page to be at the root
    storage_secret='Pluto@42',  # NOTE setting a secret is optional but allows for persistent storage per user
)

if __name__ == '__main__':
    uvicorn.run('Server:fastApiApp', log_level='info', reload=True)
