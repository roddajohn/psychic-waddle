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
    else:
        if user.thursday and not user.thursday_excused:
            if user.thursday_status == 3 and not user.wednesday_excused:
                if user.wednesday_status == 3:
                    return 'CREDIT'
                else:
                    return 'DO NOT CREDIT'
            elif user.thursday_status == 3 and user.wednesday_excused:
                return 'DO NOT STRIKE'
            elif user.wednesday_excused and not user.thursday_status == 3:
                return 'STRIKE'
            else:
                return 'DO NOT CREDIT'
        return 'DO NOTHING'

organization = sys.argv[1]

users = models.User.query.all()

actual_users = []

to_write = 'Four Digit,OSIS,Name,Wednesday Signed Up,Thursday Signed Up,Wednesday Excused,Thursday Excused,Wednesday Checkin,Wednesday Checkout,Thursday Checkin,Thursday Checkout,Wednesday Action,Thursday Action\n'

print actual_users

for user in users:
    if user.check_organization(organization):
        actual_users.append(user)
        
for user in actual_users:
    to_write += str(user.four_digit) + ',' + str(user.osis) + ',' + user.fname + ' ' + user.lname + ',' + str(user.wednesday) + ',' + str(user.thursday) + ',' + str(user.wednesday_excused) + ',' + str(user.thursday_excused) + ',' + str(user.wednesday_status == 1 or user.wednesday_status == 3) + ',' + str(user.wednesday_status == 2 or user.wednesday_status == 3) + ',' + str(user.thursday_status == 1 or user.thursday_status == 3) + ',' + str(user.thursday_status == 2 or user.thursday_status == 3) + ',' + determine_action(user, 'wednesday') + ',' + determine_action(user, 'thursday') + '\n'

open(organization + '.csv', 'w').write(to_write)

        

