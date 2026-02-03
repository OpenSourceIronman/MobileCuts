#!/usr/bin/env python3
from nicegui import ui
from datetime import datetime

from Database import Database

VALID_USA_CANADA_MEXICO_PHONE_NUMBER_LENGTH = 10
VALID_PASSWORD_LENGTH = 8

loggedInUsername = None

appDB = Database()
ui.colors(primary='#6A0DAD')
ui.colors(secondary='#D4AF37')

buttons = {}
timeSlots = ['07:00 AM', '07:30 AM', '08:00 AM', '08:30 AM', '09:00 AM', '09:30 AM', '10:00 AM', '10:30 AM', '11:00 AM', '11:30 AM', \
             '12:00 PM', '12:30 PM', '01:00 PM', '01:30 PM', '02:00 PM', '02:30 PM', '03:00 PM', '03:30 PM', '04:00 PM', '04:30 PM', '05:00 PM', '05:30 PM', '06:00 PM', '06:30 PM', '07:00 PM', '07:30 PM', '08:00 PM']

# Inject CSS to make labels gold
ui.add_head_html("""
<style>
/* Label color */
.q-field__label {
    color: #D4AF37 !important;  /* metallic gold */
}

/* Inactive underline */
.q-field__control::before {
    border-bottom: 1px solid #D4AF37 !important;
}

/* Active (focused) underline */
.q-field--focused .q-field__control::after {
    border-bottom: 2px solid #FFD700 !important;  /* bright gold when active */
}

/* Optional: input text color for better contrast */
.q-field__native {
    color: white !important;
}
</style>
""")

def sanitize_phone_number1(text):
    global sanitizedPhoneNumber

    sanitizedPhoneNumber = text.replace(" ", "")
    sanitizedPhoneNumber = sanitizedPhoneNumber.replace("(", "")
    sanitizedPhoneNumber = sanitizedPhoneNumber.replace(")", "")
    sanitizedPhoneNumber = sanitizedPhoneNumber.replace(".", "")
    sanitizedPhoneNumber = sanitizedPhoneNumber.replace("-", "")
    sanitizedPhoneNumber = sanitizedPhoneNumber.replace("+", "")

    return sanitizedPhoneNumber

def sanitize_phone_number(textInput: str):
    """Sanitize a phone number input to only digits and limit to 10 characters."""
    digits_only = ''.join(filter(str.isdigit, textInput))
    return digits_only[:10]

def sanitize_and_update(rawTextInput: str):
    return sanitize_phone_number(rawTextInput)

def gui_login(username: str, password: str, left_drawer):
    global loggedInUsername

    if userLoginButton.text == "Logout":
        userLoginButton.text = "Login"
        userUsernameTextBox.visible = True
        userPasswordTextBox.visible = True

        ui.notify(f"Logged out.", type='positive')
        return

    validLogin, id = appDB.login(username, password)
    if validLogin:
        left_drawer.hide()
        loggedInUsername = username

        userLoginButton.text = "Logout"
        userUsernameTextBox.visible = False
        userUsernameTextBox.value = ''
        userPasswordTextBox.visible = False
        userPasswordTextBox.value = ''

        ui.notify(f"Welcome, {username}!", type='positive')
    else:
        ui.notify(f"Invalid username or password.", type='negative')

def gui_button_click(e):
    global buttons
    #print(buttonclicked)
    print(e.sender.text)
    print(vars(e.sender))
    # highlight the clicked one in gold
    for button in buttons:
        if button.label != e.sender.text:
            button.delete()
    buttons[e.sender.text].update()



def gui_book_appointment(username: int):
    if loggedInUsername:
        ui.notify(f"Booking appointment for {loggedInUsername}...", type='positive')
    else:
        ui.notify(f"Please log in first.", type='negative')

with ui.header().classes(replace='row items-center').style('background-color: #6A0DAD; color: white;') as header:
    ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=white')
    with ui.tabs() as tabs:
        ui.tab('Book Appointment')
        ui.tab('Track Barber Arrival')

with ui.footer(value=False).style('background-color: #6A0DAD; color: white;') as footer:
    ui.label('Footer')

with ui.left_drawer().style('background-color: #9966CC; color: black;') as left_drawer:
    ui.label('Mobile Cuts Account').style('font-size: 24px; font-weight: bold; color: #D4AF37;')
    userUsernameTextBox = ui.input(label='Enter your 10 digit phone number', placeholder='e.g. 719.555.1234', on_change=lambda e: sanitize_and_update(e.value), \
                    validation={'Phone number is too long': lambda value: len(sanitize_phone_number(value)) <= VALID_USA_CANADA_MEXICO_PHONE_NUMBER_LENGTH}).classes('w-full')  # Length incluses + symbol at start of phone number
    userPasswordTextBox = ui.input(label='Enter your password', password=True, password_toggle_button= True, \
                    validation={'Password is too short': lambda value: len(value) >= VALID_PASSWORD_LENGTH}).classes('w-full')
    userLoginButton = ui.button('Login', color='secondary', on_click=lambda: gui_login(userUsernameTextBox.value, userPasswordTextBox.value, left_drawer)).classes('w-full').style('font-size: 24px;')

    # Capture Enter key press
    userPasswordTextBox.on(
        'keydown.enter',
        lambda: gui_login(userUsernameTextBox.value, userPasswordTextBox.value, left_drawer)
    )

with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
    ui.button(color='primaryColor', on_click=footer.toggle, icon='contact_support').props('fab')

with ui.tab_panels(tabs, value='Book Appointment').classes('w-full'):
    with ui.tab_panel('Book Appointment'):
        now = datetime.now().strftime('%Y-%m-%d')
        ui.date(value=now).classes('w-full').style('--q-primary: #9966CC; color: white;')

        with ui.row().style('justify-content: center'):
            for time in timeSlots:
                buttons[time] = ui.button(time, color='#6A0DAD', on_click=gui_button_click).classes('w-1/10').style('font-size: 14px;')

        ui.button('Book Appointment', color='secondary', on_click=lambda: gui_book_appointment(loggedInUsername)).classes('w-full').style('font-size: 24px;')

    with ui.tab_panel('Track Trip'):
        m = ui.leaflet(center=(51.505, -0.09))
        ui.label().bind_text_from(m, 'center', lambda center: f'Center: {center[0]:.3f}, {center[1]:.3f}')
        ui.label().bind_text_from(m, 'zoom', lambda zoom: f'Zoom: {zoom}')


if __name__ in {"__main__", "__mp_main__"}:

    ui.run(title='Mobile Cuts', native=True, dark=True, window_size=(1600, 980))

"""
💈 Top Purple HEX Colors for a Barber

Primary Brand Color
Royal Purple
#6A0DAD
Bold, premium, confident

Accent / Button Color
Amethyst
#9966CC
Softer luxury, pairs well with gold or black

🎨 Recommended Combinations
	1.	Modern Luxury
	•	Background: #0D0D0D (near-black)
	•	Accent: #6A0DAD
	•	Highlight: #BF00FF
	•	Text: #FFFFFF
	2.	Royal & Clean
	•	Background: #FFFFFF
	•	Primary: #7F00FF
	•	Secondary: #9966CC
	•	Accent (for pricing or premium tiers): #D4AF37 (metallic gold)
"""
