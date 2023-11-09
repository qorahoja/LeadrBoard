import logging
import csv
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram import executor
import uuid
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram import types



API_TOKEN = '6520726101:AAH1wIZScQxiHArxAat0YLX_gmomr6GhVLc'  # Replace with your actual API token
YOUR_BOT_USERNAME = 'TimeFor_Leader_grups_bot'  # Replace with your bot's username

user_data = {}
add_member_links = {}
admin_user_ids = ['5850618492'] 


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
class Form:
    waiting_for_name = 1
    waiting_for_surname = 2
    waiting_for_team = 3
    waiting_for_admin_team = 4


def catch_memberID(team):
    with open('members.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row if present

        answer = []
        for row in reader:
            if row[2] == team:
                answer.append(row[0])
        return answer


def save_backend(team_name):
    answer = catch_memberID(team_name)
    print(answer)
    with open(f"{team_name}_backend.csv", 'a', newline='') as file:
        writer = csv.writer(file)
        for id in answer:
            writer.writerow([id])
        print("success")






def save_to_csv_memember(user_id, username, team):
    with open('members.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user_id,username, team])

def save_to_csv(user_id, name, surname, team):
    with open('data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user_id, name, surname, team])
        admin_user_ids.append(user_id)


# Helper function to check if team and user match
def check_team_and_user_match(user_id, team_name):
    with open('data.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            if len(row) >= 4 and row[3] == team_name and int(row[0]) == user_id:
                return True
    return False

def check_user(user_id):
    with open('members.csv', "r", newline='') as file:
        reader = csv.reader(file)
        for i in reader:
            if i[0] == user_id:
                answer = 'You are in'
                

def save_to_csv(user_id, name, surname, team):
    with open('data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user_id, name, surname, team])
        admin_user_ids.append(user_id)




    

# Define a dictionary to store user nicknames based on user IDs
user_nicknames = {}

@dp.message_handler(commands=['start'])
async def process_start(message: types.Message):
    user_id = message.from_user.id

    await message.answer("Assalomu alaykum! Ismingizni kiriting.")
    user_data[user_id] = {"state": Form.waiting_for_name}

    

    if user_id not in user_data:
        if message.text.startswith('/start add_member_'):

            user_nickname = message.from_user.username
            link_command = message.text.split('_')
            user_id = message.from_user.id

            if len(link_command) == 3:
                link_uuid = link_command[2]
                admin_team_name = link_command[1]

                # Check if the link is valid and belongs to an admin
                if link_uuid in add_member_links:
                    # Store the admin team name and user_id
                    add_member_links[link_uuid]["admin_id"] = user_id
                    add_member_links[link_uuid]["admin_team"] = admin_team_name

                    if user_id in admin_user_ids:
                        await message.answer("You have been recognized as an admin.")
                        

                    
                    else:
                        await message.answer(f"You are welcome to {team_name} team")
                        
                        # Cache the user's nickname
                        user_nicknames[user_id] = user_nickname
                        
                        # You can now access the user's nickname using user_id as the key

                        save_to_csv_memember(user_id, user_nickname, team_name)
                        
                        
                        return
                else:
                    await message.answer("Invalid link.")
            else:
                await message.answer("Invalid link. Use it like: /start add_member_team_name_UUID")

        
    

@dp.message_handler(lambda message: user_data.get(message.from_user.id) and user_data[message.from_user.id]["state"] == Form.waiting_for_name)
async def process_name(message: types.Message):
    user_data[message.from_user.id]["name"] = message.text
    await message.answer("Iltimos familiyangizni kiriting.")
    user_data[message.from_user.id]["state"] = Form.waiting_for_surname

@dp.message_handler(lambda message: user_data.get(message.from_user.id) and user_data[message.from_user.id]["state"] == Form.waiting_for_surname)
async def process_surname(message: types.Message):
    user_data[message.from_user.id]["surname"] = message.text
    await message.answer("Iltimos jamoa nomini kiriting.")
    user_data[message.from_user.id]["state"] = Form.waiting_for_team

@dp.message_handler(lambda message: user_data.get(message.from_user.id) and user_data[message.from_user.id]["state"] == Form.waiting_for_team)
async def process_team(message: types.Message):
    user_data[message.from_user.id]["team"] = message.text
    user_info = user_data[message.from_user.id]

    full_name = f"{user_info['name']} {user_info['surname']}"
    team = user_info['team']

    response = f"Ismingiz: {full_name}\nJamoa nomingiz: {team}"

    save_to_csv(message.from_user.id, user_info['name'], user_info['surname'], user_info['team'])

    inline_kb = types.InlineKeyboardMarkup(row_width=2)
    accept_btn = types.InlineKeyboardButton("Accept", callback_data="accept")
    edit_btn = types.InlineKeyboardButton("Edit", callback_data="edit")

    inline_kb.add(accept_btn, edit_btn)

    await message.answer(response, reply_markup=inline_kb)

@dp.callback_query_handler(lambda c: c.data == 'accept')
async def process_accept(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if user_id in user_data:
        await callback_query.answer("You have accepted the information.")
        del user_data[user_id]

@dp.callback_query_handler(lambda c: c.data == 'edit')
async def process_edit(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if user_id in user_data:
        await callback_query.answer("You have chosen to edit your information.")
        user_data[user_id]["state"] = Form.waiting_for_name
        await callback_query.message.answer("Assalomu alaykum! Ismingizni kiriting.")
    else:
        await callback_query.answer("Your data has already been accepted or does not exist.")

@dp.message_handler(commands=['admin'])
async def process_admin_command(message: types.Message):
    user_id = message.from_user.id

    if user_id in admin_user_ids:
        # Prompt the admin to enter their team name
        await message.answer("Enter your team name:")
        user_data[user_id] = {"state": Form.waiting_for_admin_team}
    else:
        await message.answer("You are not an admin.")

@dp.message_handler(lambda message: user_data.get(message.from_user.id) and user_data[message.from_user.id]["state"] == Form.waiting_for_admin_team)
async def process_admin_team(message: types.Message):
    user_id = message.from_user.id
    admin_team_name = message.text

    if check_team_and_user_match(user_id, admin_team_name):

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        global team_name
        team_name = message.text
        



        

        # Define your custom keyboard layout
        

        # Define the keyboard buttons
        buttons = [
            KeyboardButton("Ish boshlash"),
            KeyboardButton("Members"),
            KeyboardButton("Add Member"),  # Added "Add Member" button
        ]

        # Add the buttons to the keyboard layout
        keyboard.add(*buttons)


        await message.answer("Welcome, admin!", reply_markup=keyboard)

        
    else:
        await message.answer("Team name does not match. You are not an admin or the team name is incorrect.")

    # Clear the user's state
    del user_data[user_id]




@dp.message_handler(lambda message: message.text.lower() == "members")
async def send_members_data(message: types.Message):
    global members_data

    with open('members.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row if present

        members_data = []
        member_count = 0  # Initialize a counter for sequential numbers

        for row in reader:
            if row and len(row) >= 3 and row[2] == team_name:
                member_count += 1
                member_username = f"@{row[1]}"  # Add "@" sign in front of username
                members_data.append(f"{member_count}. {member_username}")

        if members_data:
            members_info = "\n".join(members_data)
            await message.answer(f"Members in your team:\n{members_info}")
        else:
            await message.answer("No members found in your team.")


@dp.message_handler(lambda message: message.text.lower() == "ish boshlash")
async def work(message: types.Message):
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        
        buttons = [
            KeyboardButton("Web site"),
            KeyboardButton("Telegram bot"),
            KeyboardButton('Back')
              # Added "Add Member" button
        ]

        # Add the buttons to the keyboard layout
        keyboard.add(*buttons)

        await message.answer("Choice your work", reply_markup=keyboard)



@dp.message_handler(lambda message: message.text.lower() == "back")
async def Web_Site(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    
    buttons = [
            KeyboardButton("Ish boshlash"),
            KeyboardButton("Members"),
            KeyboardButton("Add Member"),  # Added "Add Member" button
        ]

        # Add the buttons to the keyboard layout
    keyboard.add(*buttons)

    await message.answer("Back", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text.lower() == "web site")
async def Web_Site(message: types.Message):
    global member_data
    member_data = []
    member_count = 0  # Initialize a counter for sequential numbers

    with open('members.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row if present

        for row in reader:
            if row and len(row) >= 3 and row[2] == team_name:  # Replace team_name with your desired team name
                member_count += 1
                member_username = f"@{row[1]}"  # Add "@" sign in front of username
                member_data.append(f"{member_count}. {member_username}")

    if member_data:
        members_info = "\n".join(member_data)
        await message.answer(f"Please select worker(s) for Backend:\n{members_info}\n"
                             "Enter the numbers of the members separated by commas (e.g., 1, 2, 5):")
    else:
        await message.answer("No members found in your team.")

@dp.message_handler(lambda message: message.text and ',' in message.text)
async def select_multiple_members(message: types.Message):
    choices = message.text.split(',')
   
    
    selected_members = []

    for choice in choices:

            selected_number = int(choice.strip())
            if 1 <= selected_number <= len(member_data):
                selected_member_info = member_data[selected_number - 1]
                selected_members.append(selected_member_info)
    
    
    save_backend(team_name)                



    
        

    if selected_members:
        selected_members_info = "\n".join(selected_members)
        await message.answer(f"You have selected the following worker(s) for Backend:\n{selected_members_info}")
    else:
        await message.answer("Invalid selection. Please choose valid member numbers separated by commas.")





# @dp.message_handler(lambda message: message.text.lower() == "monoboss" and message.from_user.id in admin_user_ids)
# async def process_monoboss_command(message: types.Message):
#     # The admin sent "Monoboss" in a monospace format
#     response_message = "```\n"
#     response_message += "Hello, admin!\n"
#     response_message += "You have initiated the 'Add member' process.\n"
#     response_message += "Please follow the instructions to add a member."
#     response_message += "\n```"

#     await message.answer(response_message, parse_mode="Markdown")


@dp.message_handler(lambda message: message.text.lower() == "add member" and message.from_user.id in admin_user_ids)
async def process_add_member_command(message: types.Message):
        user_id = message.from_user.id
        link_uuid = str(uuid.uuid4())
        deep_link = f"https://t.me/{YOUR_BOT_USERNAME}?start=add_member_{link_uuid}"
        add_member_links[link_uuid] = {"admin_id": user_id}

        await message.answer(f"Use the following link to add members to your team:\n{deep_link}")


async def process_start_from_link(message: types.Message):
    link = message.text.split("/")[-1]
    link_uuid = link.replace("add_member_", "")
    if link_uuid in add_member_links:
        user_id = message.from_user.id
        user_nickname = message.from_user.username
        add_member_links[link_uuid]["user_id"] = user_id
        add_member_links[link_uuid]["user_nickname"] = user_nickname

        # Record user information in memembers.csv
        admin_id = add_member_links[link_uuid]["admin_id"]
        admin_team_name = add_member_links[link_uuid]["admin_team"]
        save_to_csv_memember(user_id, user_nickname, admin_team_name)

        # Notify the admin
        admin_notification = f"{user_nickname} has been added to your team."
        await bot.send_message(admin_id, admin_notification)

        # Send a success message to the user
        await message.answer("Congratulations! You have been added to the team.")

        # Store link_uuid in add_member_links
        add_member_links[link_uuid]["link_uuid"] = link_uuid
    else:
        await message.answer("Invalid link.")



if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
