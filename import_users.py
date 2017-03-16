from app import models, db
import sys

file_to_parse = sys.argv[1]

text = open(sys.argv[1]).read()

for line in text.split('\n'):
    if file_to_parse == 'big_sibs.csv':
        osis = int(line.split(',')[4])
        user = models.User.query.filter_by(osis = osis).first()
        if user:
            user.add_organization('big_sibs')
            user.thursday = True
        else:
            new_user = models.User(fname = line.split(',')[0],
                                   lname = line.split(',')[1],
                                   nickname = "",
                                   username = line.split(',')[3],
                                   email = line.split(',')[2],
                                   osis = int(line.split(',')[4]),
                                   four_digit = int(line.split(',')[3]),
                                   organizations = 'big_sibs,',
                                   permissions = '')
            new_user.set_password(line.split(',')[4])
            new_user.add_permission('user')
            new_user.wednesday = True
            new_user.thursday = True
            new_user.wednesday_excused = False
            new_user.thursday_excused = False
            new_user.wednesday_status = 0
            new_user.thursday_status = 0
            db.session.add(new_user)
            db.session.commit()

    else:
        osis = int(line.split(',')[4])
        user = models.User.query.filter_by(osis = osis).first()
        if user:
            user.add_organization('arista')
        else:
            new_user = models.User(fname = line.split(',')[0],
                                   lname = line.split(',')[1],
                                   nickname = "",
                                   username = line.split(',')[3],
                                   email = line.split(',')[5],
                                   osis = int(line.split(',')[4]),
                                   four_digit = int(line.split(',')[3]),
                                   organizations = 'arista,',
                                   permissions = '')
            new_user.set_password(line.split(',')[4])
            new_user.add_permission('user')
            new_user.wednesday = True
            new_user.thursday = False
            new_user.wednesday_excused = False
            new_user.thursday_excused = False
            new_user.wednesday_status = 0
            new_user.thursday_status = 0
            db.session.add(new_user)
            db.session.commit()
