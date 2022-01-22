import re
import os


class User:
    def register_user(self):
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_regex = r'\b[0-5]{3}[0-9]{4}[0-9]{4}\b'
        self.user_info = []
        self.user_info.append(input('First name: '))
        self.user_info.append(input('Last name: '))

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
                        self.user_info.append(email_input)
                break
            else:
                print('Please, enter a valid email.')

        while True:
            phone_input = input('Phone number: ')
            if re.fullmatch(phone_regex, phone_input):
                self.user_info.append(phone_input)
                break
            else:
                print ('Please enter a valid phone number')

        while True:
            password = input('Password: ')
            confirm_password = input('Confirm password: ')
            if password == confirm_password:
                self.user_info.append(password)
                self.add_user_info_for_regestiration(self.user_info)
                break
            else:
                print('Passwords do not match, please try again.')



    def add_user_info_for_regestiration(self, user_info):
        users = open('users', 'a')
        users.write('{}\n'.format(':'.join(user_info)))
                

    def auth_user(self):
        self.login_email = input('Enter your e-mail: ')
        self.login_password = input('Enter your password: ')
        users = open('users', 'r')
        for user in users:
            stripped_line = user.strip()
            email_from_info = stripped_line.split(':')[2]
            password_from_info = stripped_line.split(':')[-1]
            if self.login_email == email_from_info and self.login_password == password_from_info:
                campaigns_dialog(self.login_email)


class Campaign:
    def create_campaign(self, owner_email):
        self.campaign_info = []
        fund_regex = r'\b[0-9]+\b'
        self.campaign_info.append(input('Campaign title: '))
        self.campaign_info.append(input('Campaign details: '))

        while True:
            campaign_fund_target = input('Campaign total target (in EGP): ')
            if re.fullmatch(fund_regex,campaign_fund_target):
                self.campaign_info.append(campaign_fund_target)
                break
            else:
                print('Please, enter a number')
        
        self.campaign_info.append(input('Start date: '))
        self.campaign_info.append(input('End date: '))
        self.campaign_info.append(owner_email)
        users = open('campaigns', 'a')
        users.write('{}\n'.format(':'.join(self.campaign_info)))


    def show_campaigns(self):
        campaigns = open('campaigns', 'r')
        for campaign in campaigns:
            print(campaign.strip())


    def find_campaign(self):
        search_term = input('What campaign are you looking for?\n')
        campaigns = open('campaigns', 'r')
        for campaign in campaigns:
            campaign_info = campaign.strip()
            campaign_name = campaign_info.split(':')[0]
            if campaign_name == search_term:
                print(campaign_info)



    def delete_campaign(self, owner_email):
        with open('campaigns', 'r+') as campaigns:

            # Get a campaign name to delete
            campaign_to_delete = input('Enter campaign name to delete: ')

            for campaign in campaigns:
                campaign_info = campaign.strip()
                campaign_found_title = campaign_info.split(':')[0]
                campaign_found_email = campaign_info.split(':')[-1]


                if campaign_found_title == campaign_to_delete and campaign_found_email == owner_email:
                    # delete a campaign
                    os.system('sed -i "/{}/d" {}'.format(campaign_info, 'campaigns'))
                    

def campaigns_dialog(login_email):
    print('You can create campaign "c", see all campaigns "s", search for a campaign "f", delete one of your campaigns"d".')

    while True:
        user_action = input('Enter a letter referring to your action: ')
        campaign = Campaign()

        if user_action == 'c':
            campaign.create_campaign(login_email)
            break
        elif user_action == 'd':
            campaign.delete_campaign(login_email)
            break
        elif user_action == 's':
            campaign.show_campaigns()
            break
        elif user_action == 'f':
            campaign.find_campaign()
            break

        else:
            print('Please enter a valid action.')


def init_dialog():
    while True:
        user_intent = input('Do you want login "l", or register "r"?\n')

        user = User()
        if user_intent == 'l':
            user.auth_user()
            break
        elif user_intent == 'r':
            user.register_user()
            break
        else:
            print('Please enter a valid action.')


init_dialog()
