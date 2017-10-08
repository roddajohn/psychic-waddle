from app import models, db

output = 'Four Digit,OSIS,Name,Tuesday Signed up,Tuesday Excused,Wednesday Signed Up,Wednesday Excused\n'

for u in models.User.query.all():
    output += str(u.four_digit) + ',' + str(u.osis) + ',' + u.fname + ' ' + u.lname + ',' + str(u.wednesday) + ',' + str(u.wednesday_excused) + ',' + str(u.thursday) + ',' + str(u.thursday_excused) + '\n'

open('assignment.csv', 'w').write(output)
