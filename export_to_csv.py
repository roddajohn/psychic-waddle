from app import models, db
import sys

def determine_action(user, day):
    if day == 'wednesday':
        if user.wednesday and not user.wednesday_excused:
            if user.wednesday_status == 3:
                return 'CREDIT 2'
            else:
                return 'STRIKE'
        return 'DO NOTHING'
    if day == 'thursday':
        if not user.wednesday_status == 3:
            if user.thursday_status == 3:
                return 'CREDIT 2'
            else:
                return 'STRIKE'
        else:
            if user.thursday_status == 3:
                return 'CREDIT 4'
            else:
                return 'DO NOTHING'
            
organization = sys.argv[1]

users = models.User.query.all()

actual_users = []

for user in users:
    if user.check_organization(organization):
        actual_users.append(user)

if organization == 'arista':
    to_write = 'Four Digit,OSIS,Name,Tuesday Signed Up,Tuesday Excused,Tuesday Status,Wednesday Signed Up, Wednesday Excused,Wednesday Status,Tuesday Action,Wednesday Action\n'
    for user in actual_users:
        to_write += str(user.four_digit) + ',' + str(user.osis) + ',' + user.fname + ' ' + user.lname + ',' + str(user.wednesday) + ',' + str(user.wednesday_excused) + ',' + str(user.wednesday_status) + ',' + str(user.thursday) + ',' + str(user.thursday_excused) + ',' + str(user.thursday_status) + ',' + determine_action(user, 'wednesday') + determine_action(user, 'thursday') + '\n'
        
else:
    to_write = 'Four Digit,OSIS,Name,Tuesday Signed Up,Tuesday Excused,Tuesday Status,Wednesday Signed Up, Wednesday Excused,Wednesday Status\n'
    for user in actual_users:
        to_write += str(user.four_digit) + ',' + str(user.osis) + ',' + user.fname + ' ' + user.lname + ',' + str(user.wednesday) + ',' + str(user.wednesday_excused) + ',' + str(user.wednesday_status) + ',' + str(user.thursday) + ',' + str(user.thursday_excused) + ',' + str(user.thursday_status) + ',' + determine_action(user, 'wednesday') + determine_action(user, 'thursday') + '\n'


open(organization + '.csv', 'w').write(to_write)

        

