import re
import os

def init_dialog():
    while True:
        user_intent = input('Do you want login "l", or register "r"?\n')

        if user_intent == 'l':
            auth_user()
            break
        elif user_intent == 'r':
            register_user()
            break
        else:
            print('Please enter a valid action.')
            


def register_user():
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_regex = r'\b[0-5]{3}[0-9]{4}[0-9]{4}\b'
    user_info = []
    user_info.append(input('First name: '))
    user_info.append(input('Last name: '))

    while True:
        email_input = input('E-mail: ')
        if re.fullmatch(email_regex, email_input):
            users = open('users', 'r')
            for user in users:
                stripped_line = user.strip()
                email_from_info = stripped_line.split(':')[2]
                if email_input == email_from_info:
                    print('This account already exists')
                    exit()
                else:
                    user_info.append(email_input)
            break
        else:
            print('Please, enter a valid email.')

    while True:
        phone_input = input('Phone number: ')
        if re.fullmatch(phone_regex, phone_input):
            user_info.append(phone_input)
            break
        else:
            print ('Please enter a valid phone number')

    while True:
        password = input('Password: ')
        confirm_password = input('Confirm password: ')
        if password == confirm_password:
            user_info.append(password)
            users = open('users', 'a')
            users.write('{}\n'.format(':'.join(user_info)))
            break
        else:
            print('Passwords do not match, please try again.')



def auth_user():
    login_email = input('Enter your e-mail: ')
    login_password = input('Enter your password: ')
    users = open('users', 'r')
    for user in users:
        stripped_line = user.strip()
        email_from_info = stripped_line.split(':')[2]
        password_from_info = stripped_line.split(':')[-1]
        if login_email == email_from_info and login_password == password_from_info:
            reveal_projects_dialog(login_email)


def reveal_projects_dialog(login_email):
    print('You can create campaign "c", see all campaigns "s", search for a campaign "f", delete one of your campaigns"d".')

    while True:
        user_action = input('Enter a letter referring to your action: ')

        if user_action == 'c':
            create_campaign(login_email)
            break
        elif user_action == 'd':
            delete_campaign(login_email)
            break
        elif user_action == 's':
            show_campaigns()
            break
        elif user_action == 'f':
            find_campaign()
            break

        else:
            print('Please enter a valid action.')


def create_campaign(owner_email):
    campaign_info = []
    fund_regex = r'\b[0-9]+\b'
    campaign_info.append(input('Campaign title: '))
    campaign_info.append(input('Campaign details: '))

    while True:
        campaign_fund_target = input('Campaign total target (in EGP): ')
        if re.fullmatch(campaign_fund_target, fund_regex):
            campaign_info.append(campaign_fund_target)
            break
        else:
            print('Please, enter a number')
    
    campaign_info.append(input('Start date: '))
    campaign_info.append(input('End date: '))
    campaign_info.append(owner_email)


    users = open('campaigns', 'a')
    users.write('{}\n'.format(':'.join(campaign_info)))



def show_campaigns():
    campaigns = open('campaigns', 'r')
    for campaign in campaigns:
        print(campaign.strip())



def find_campaign():
    search_term = input('What campaign are you looking for?\n')
    campaigns = open('campaigns', 'r')
    for campaign in campaigns:
        campaign_info = campaign.strip()
        campaign_name = campaign_info.split(':')[0]
        if campaign_name == search_term:
            print(campaign_info)
        else:
            print('404: Sorry, It does not seem there is such a campaign.')



def delete_campaign(owner_email):
    with open('campaigns', 'r+') as campaigns:

        # Get a campaign name to delete
        campaign_to_delete = input('Enter campaign name to delete: ')

        for campaign in campaigns:
            campaign_info = campaign.strip()
            campaign_found_title = campaign_info.split(':')[0]
            campaign_found_email = campaign_info.split(':')[-1]


            if campaign_found_title == campaign_to_delete and campaign_found_email == owner_email:
                # delete a campaign
                os.system('sed -i "/{}/d" {}'.format(campaign_info, 'campains'))
                    

init_dialog()
