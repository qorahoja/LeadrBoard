
        
 

# async def send_scheduled_message(chat_id, text, scheduled_time):
#     current_time = datetime.datetime.now()
#     time_difference = scheduled_time - current_time

#     if time_difference.total_seconds() > 0:
#         await asyncio.sleep(time_difference.total_seconds())
#         await bot.send_message(chat_id, text, parse_mode=types.ParseMode.MARKDOWN)
#     else:
#         print("Scheduled time is in the past. Message not sent.")

# if __name__ == '__main__':
#     # Replace with your desired chat_id, message text, and scheduled time
#     chat_id = 5850618492
#     message_text = "Hello, this is a scheduled message!"
#     scheduled_time = datetime.datetime(2023, 11, 4, 15, 2)  # Adjust the date and time as needed

#     asyncio.run(send_scheduled_message(chat_id, message_text, scheduled_time))
