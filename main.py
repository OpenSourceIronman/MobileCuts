#!/usr/bin/env python3
from nicegui import ui

VALID_USA_CANADA_MEXICO_PHONE_NUMBER_LENGTH = 10
ui.colors(primaryColor='#6A0DAD')

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

def sanitize_phone_number(text):
    global sanitizedPhoneNumber

    sanitizedPhoneNumber = text.replace(" ", "")
    sanitizedPhoneNumber = sanitizedPhoneNumber.replace("(", "")
    sanitizedPhoneNumber = sanitizedPhoneNumber.replace(")", "")
    sanitizedPhoneNumber = sanitizedPhoneNumber.replace(".", "")
    sanitizedPhoneNumber = sanitizedPhoneNumber.replace("-", "")
    sanitizedPhoneNumber = sanitizedPhoneNumber.replace("+", "")

    return sanitizedPhoneNumber

with ui.header().classes(replace='row items-center').style('background-color: #6A0DAD; color: white;') as header:
    ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=white')
    with ui.tabs() as tabs:
        ui.tab('Book Appointment')
        ui.tab('Track Trip')


with ui.footer(value=False).style('background-color: #6A0DAD; color: white;') as footer:
    ui.label('Footer')

with ui.left_drawer().style('background-color: #9966CC; color: black;') as left_drawer:
    userInputTextBox = ui.input(label='Enter your 10 digit phone number', placeholder='e.g. 719.555.1234', \
                    validation={'Phone number is too long': lambda value: len(sanitize_phone_number(value)) <= VALID_USA_CANADA_MEXICO_PHONE_NUMBER_LENGTH}).classes('w-full')  # Length incluses + symbol at start of phone number


with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
    ui.button(color='primaryColor',on_click=footer.toggle, icon='contact_support').props('fab')

with ui.tab_panels(tabs, value='Book Appointment').classes('w-full'):
    with ui.tab_panel('Book Appointment'):
        ui.label('Content of A')
    with ui.tab_panel('Track Trip'):
        ui.label('Content of B')

ui.run(title='Mobile Cuts Appd', native=True)

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
