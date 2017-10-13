from app import models, db
import sys

u = models.User(
    four_digit = int(sys.argv[1]),
    username = sys.argv[1],
    osis = int(sys.argv[2]),
    fname = sys.argv[3],
    lname = sys.argv[4],
    nickname = '',
    organizations = 'big_sibs,',
    permissions = ''
)
u.set_password(str(u.osis))
u.add_permission('user')
u.wednesday = True
u.thursday = True
u.wednesday_excused = False
u.thursday_excused = False
u.wednesday_status = 0
u.thursday_status = 0
db.session.add(u)
db.session.commit()
