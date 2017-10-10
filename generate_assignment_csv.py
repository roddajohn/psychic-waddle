from app import models, db

output = 'Four Digit,OSIS,Name,Tuesday Signed up,Tuesday,Wednesday\n'

for u in models.User.query.all():
    if u.wednesday_excused:
        wed = 'Excused'
    elif u.wednesday:
        wed = 'Yes'
    else:
        wed = 'No'

    if u.thursday_excused:
        thurs = 'Excused'
    elif u.thursday:
        thurs = 'Yes'
    else:
        thurs = 'No'
    
    output += str(u.four_digit) + ',' + str(u.osis) + ',' + u.fname.strip() + ' ' + u.lname.strip() + ',' + wed + ',' + thurs + '\n'

open('assignment.csv', 'w').write(output)
