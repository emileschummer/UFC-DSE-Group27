import pywhatkit

number= 1
Message= 'Tijn braincell'
while number < 100:
    print(number , Message)
    number += 1
    # Replace with the recipient's phone number (including country code)
    phone_number = "+31648443464"  # Dutch format example

    # Send each message
    for i in range(1, 100):
        message = f"{i} {Message}"
        # Schedule message with 30 second intervals to avoid blocking
        pywhatkit.sendwhatmsg_instantly(phone_number, message, 15, True)


        