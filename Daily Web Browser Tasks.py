import webbrowser

# Define URL lists for each section
sections = {
    "Mon1": [
        'https://www.xxxxxxxxxxxx.com/xxxxxxxxxxxxxxxx'
    ],
    "Tues1": [
        'https://www.xxxxxxxxxxxx.com/xxxxxxxxxxxxxxxx'
    ],
    "Tues2": [
        'https://www.xxxxxxxxxxxx.com/xxxxxxxxxxxxxxxx'
    ],
    "Wed1": [
        'https://www.xxxxxxxxxxxx.com/xxxxxxxxxxxxxxxx'
    ],
    "Fri1": [
        'https://www.xxxxxxxxxxxx.com/xxxxxxxxxxxxxxxx'

    ]
}

# Ask the user for a section name
section = input("Enter the section name (Mon1, Tues1, Tues2, Wed1, Fri1): ").strip()

# Open the URLs for the selected section
if section in sections:
    for url in sections[section]:
        webbrowser.open(url, new=0)
    print(f"Opened {len(sections[section])} links for {section}.")
else:
    print("Invalid section name. Please try again.")
