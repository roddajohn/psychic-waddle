from app import models, db
import sys

def determine_action(user, day):
    if day == 'wednesday':
        if user.wednesday and not user.wednesday_excused:
            if user.wednesday_status == 3:
                return 'DO NOT STRIKE'
            else:
                return 'STRIKE'
        return 'DO NOTHING'

organization = sys.argv[1]

users = models.User.query.all()

actual_users = []

to_write = 'Four Digit,OSIS,Name,Tuesday Signed Up,Tuesday Excused,Tuesday Status,Tuesday Action\n'

print actual_users

for user in users:
    if user.check_organization(organization):
        actual_users.append(user)
        
for user in actual_users:
    to_write += str(user.four_digit) + ',' + str(user.osis) + ',' + user.fname + ' ' + user.lname + ',' + str(user.wednesday) + ',' + str(user.wednesday_excused) + ',' + str(user.wednesday_status) + ',' + determine_action(user, 'wednesday') + '\n'

open(organization + '.csv', 'w').write(to_write)

        

