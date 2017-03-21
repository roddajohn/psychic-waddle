from flask import render_template, flash, redirect, request, session, url_for, jsonify
from forms import *
from app import app, db, models
from sqlalchemy import or_

from datetime import datetime

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    user = None
    if 'username' in session and session['username']:
        user = models.User.query.filter_by(username = session['username']).first()

    return render_template("index.html", user = user)

@app.route('/create', methods=['GET', 'POST'])
def create():
    create_form = CreateForm()

    if create_form.validate_on_submit():
        new_user = models.User(fname = create_form.fname.data,
                               lname = create_form.lname.data,
                               nickname = create_form.nickname.data,
                               username = create_form.username.data,
                               email = create_form.email.data,
                               osis = create_form.osis.data,
                               four_digit = create_form.four_digit.data,
                               organizations = ','.join(create_form.organizations.data),
                               permissions = '')
        new_user.set_password(create_form.password.data)
        new_user.add_permission('user')
        new_user.wednesday = True
        new_user.wednesday_excused = False
        new_user.thursday_excused = False
        new_user.wednesday_status = 0
        new_user.thursday_status = 0
        db.session.add(new_user)
        db.session.commit()
        flash('You have signed up!')
        return redirect('login')

    return render_template('create.html', create_form = create_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        session['username'] = login_form.username.data
        return redirect('index')

    return render_template('login.html', login_form = login_form)

@app.route('/user_view', methods=['GET', 'POST'])
def user_view():
    user = models.User.query.filter_by(username = session['username']).first()

    if not user:
        flash('Please login')
        return redirect('index')

    return render_template('user_view.html', user = user, organizations = app.config['ORGANIZATIONS'])

@app.route('/logout', methods=['GET'])
def logout():
    user = models.User.query.filter_by(username = session['username']).first()

    if not user:
        flash('Please login')
        return redirect('index')

    session.pop('username')
    flash('You have been logged out')
    return redirect('index')

@app.route('/api/add_organization/<string:organization>', methods=['GET'])
def add_organization(organization = ''):
    user = models.User.query.filter_by(username = session['username']).first()

    if not user:
        flash('Please login')
        return redirect('index')
        
    user.add_organization(organization)
    return redirect('user_view')

@app.route('/api/remove_organization/<string:organization>', methods=['GET'])
def remove_organization(organization = ''):
    user = models.User.query.filter_by(username = session['username']).first()

    if not user:
        flash('Please login')
        return redirect('index')

    user.remove_organization(organization)
    return redirect('user_view')

@app.route('/toggle_wednesday')
def toggle_wednesday():
    user = models.User.query.filter_by(username = session['username']).first()

    if not user:
        flash('Please login')
        return redirect('index')
        
    user.wednesday = not user.wednesday
    db.session.commit()
    return redirect('user_view')

@app.route('/toggle_thursday')
def toggle_thursday():
    user = models.User.query.filter_by(username = session['username']).first()

    if not user:
        flash('Please login')
        return redirect('index')
        
    user.thursday = not user.thursday
    db.session.commit()
    return redirect('user_view')

@app.route('/users', methods = ['GET', 'POST'])
@app.route('/users/<int:page>', methods = ['GET', 'POST'])
@app.route('/users/<int:page>/', methods = ['GET', 'POST'])
@app.route('/users/<int:page>/<string:search_field>', methods = ['GET', 'POST'])
def users(page = 1, search_field = ""):
    user = models.User.query.filter_by(username = session['username']).first()

    if not user:
        flash('Please login')
        return redirect('index')

    if not user.check_permission('admin'):
        flash('You must be an administrator to view this page')
        return redirect('index')

    search_form = SearchForm()

    users = models.User.query
    
    if search_form.validate_on_submit():
        search_field = search_form.search_field.data
        return redirect(url_for('users', page = page, search_field = search_field))

    if search_field == 'Red Cross':
        search_field = 'red_cross'
    elif search_field == 'ARISTA':
        search_field = 'arista'
    elif search_field == 'Big Sibs':
        search_field = 'big_sibs'
    elif search_field == 'Key Club':
        search_field = 'key_club'
        
    if search_field == 'thursday' or search_field == 'Thursday':
        users = users.filter_by(thursday = True, thursday_excused = False)
    elif search_field == 'wednesday' or search_field == 'Wednesday':
        users = users.filter_by(wednesday = True, wednesday_excused = False)
        
    else:
        users = users.filter(
            or_(models.User.fname.like('%' + search_field + '%'),
                models.User.lname.like('%' + search_field + '%'),
                models.User.nickname.like('%' + search_field + '%'),
                models.User.four_digit.like('%' + search_field + '%'),
                models.User.organizations.like('%' + search_field + '%'),
                models.User.osis.like('%' + search_field + '%')))

    users = users.paginate(page, app.config['ELEMENTS_PER_PAGE'], False)

    wednesday_volunteers = len(models.User.query.filter_by(wednesday = True).filter_by(wednesday_excused = False).all())
    thursday_volunteers = len(models.User.query.filter_by(thursday = True).filter_by(thursday_excused = False).all())

    return render_template('users.html', user = user, users = users, organizations = app.config['ORGANIZATIONS'], search_form = search_form, search_field = search_field, wednesday_volunteers = wednesday_volunteers, thursday_volunteers = thursday_volunteers)

@app.route('/admin_user_view/<int:user_id>')
def admin_user_view(user_id = 0):
    user = models.User.query.filter_by(username = session['username']).first()

    if not user:
        flash('Please login')
        return redirect('index')

    if not user.check_permission('admin'):
        flash('You must be an administrator to view this page')
        return redirect('index')
        
    u = models.User.query.filter_by(id = user_id).first()
    if not u:
        flash('User not found')
        return redirect('users')

    return render_template('admin_user_view.html', user = user, u = u, organizations = app.config['ORGANIZATIONS'])

@app.route('/toggle_wednesday_excused/<int:user_id>')
def toggle_wednesday_excused(user_id = 0):
    user = models.User.query.filter_by(username = session['username']).first()

    if not user:
        flash('Please login')
        return redirect('index')

    if not user.check_permission('admin'):
        flash('You must be an administrator to view this page')
        return redirect('index')
        
    u = models.User.query.filter_by(id = user_id).first()
    if not u:
        flash('User not found')
        return redirect('users')

    u.wednesday_excused = not u.wednesday_excused
    db.session.commit()

    return redirect(url_for('admin_user_view', user_id = u.id))

@app.route('/toggle_thursday_excused/<int:user_id>')
def toggle_thursday_excused(user_id = 0):
    user = models.User.query.filter_by(username = session['username']).first()

    if not user:
        flash('Please login')
        return redirect('index')

    if not user.check_permission('admin'):
        flash('You must be an administrator to view this page')
        return redirect('index')
        
    u = models.User.query.filter_by(id = user_id).first()
    if not u:
        flash('User not found')
        return redirect('users')

    u.thursday_excused = not u.thursday_excused
    db.session.commit()

    return redirect(url_for('admin_user_view', user_id = u.id))

@app.route('/wednesday_checkin', methods=['GET', 'POST'])
def wednesday_checkin():
    user = models.User.query.filter_by(username = session['username']).first()

    if not user:
        flash('Please login')
        return redirect('index')

    if not user.check_permission('admin'):
        flash('You must be an administrator to view this page')
        return redirect('index')
        
    four_digit_form = FourDigitForm()

    if four_digit_form.validate_on_submit():
        user_to_checkin = models.User.query.filter_by(four_digit = four_digit_form.search_field.data).first()
        if not user_to_checkin:
            flash("That user was not found")
            return redirect('wendesday_checkin')

        if four_digit_form.method.data == 'checkin':
            user_to_checkin.wednesday_status = 1
            flash("Checked %s in" % user_to_checkin.fname)
            user_to_checkin.timestamp_wednesday_checked_in = datetime.today()
        else:
            user_to_checkin.wednesday_status = 0
            flash("Unchecked %s in" % user_to_checkin.fname)
        db.session.commit()
        return redirect('wednesday_checkin')

    return render_template('wednesday_checkin.html', user = user, four_digit_form = four_digit_form)

@app.route('/wednesday_checkout', methods=['GET', 'POST'])
def wednesday_checkout():
    user = models.User.query.filter_by(username = session['username']).first()

    if not user:
        flash('Please login')
        return redirect('index')

    if not user.check_permission('admin'):
        flash('You must be an administrator to view this page')
        return redirect('index')
        
    four_digit_form = FourDigitFormCheckout()

    if four_digit_form.validate_on_submit():
        user_to_checkout = models.User.query.filter_by(four_digit = four_digit_form.search_field.data).first()
        if not user_to_checkout:
            flash("That user was not found")
            return redirect('wendesday_checkout')

        if four_digit_form.method.data == 'checkout':
            if user_to_checkout.wednesday_status == 1:
                user_to_checkout.wednesday_status = 3
            else:
                user_to_checkout.wednesday_status = 2
            user_to_checkin.timestamp_wendesday_checked_out = datetime.today()
            flash("Checked %s out" % user_to_checkout.fname)
        else:
            if user_to_checkout.wednesday_status == 2:
                user_to_checkout.wednesday_status = 0
            else:
                user_to_checkout.wednesday_status = 1
            flash("Unchecked %s out" % user_to_checkout.fname)
        db.session.commit()
        return redirect('wednesday_checkout')

    return render_template('wednesday_checkout.html', user = user, four_digit_form = four_digit_form)

@app.route('/thursday_checkin', methods=['GET', 'POST'])
def thursday_checkin():
    user = models.User.query.filter_by(username = session['username']).first()

    if not user:
        flash('Please login')
        return redirect('index')

    if not user.check_permission('admin'):
        flash('You must be an administrator to view this page')
        return redirect('index')
        
    four_digit_form = FourDigitForm()

    if four_digit_form.validate_on_submit():
        user_to_checkin = models.User.query.filter_by(four_digit = four_digit_form.search_field.data).first()
        if not user_to_checkin:
            flash("That user was not found")
            return redirect('wendesday_checkin')

        if four_digit_form.method.data == 'checkin':
            user_to_checkin.thursday_status = 1
            flash("Checked %s in" % user_to_checkin.fname)
        else:
            user_to_checkin.thursday_status = 0
            flash("Unchecked %s in" % user_to_checkin.fname)
        db.session.commit()
        return redirect('thursday_checkin')

    return render_template('thursday_checkin.html', user = user, four_digit_form = four_digit_form)

@app.route('/thursday_checkout', methods=['GET', 'POST'])
def thursday_checkout():
    user = models.User.query.filter_by(username = session['username']).first()

    if not user:
        flash('Please login')
        return redirect('index')

    if not user.check_permission('admin'):
        flash('You must be an administrator to view this page')
        return redirect('index')
        
    four_digit_form = FourDigitFormCheckout()

    if four_digit_form.validate_on_submit():
        user_to_checkout = models.User.query.filter_by(four_digit = four_digit_form.search_field.data).first()
        if not user_to_checkout:
            flash("That user was not found")
            return redirect('wendesday_checkout')
            
        if four_digit_form.method.data == 'checkout':
            if user_to_checkout.thursday_status == 1:
                user_to_checkout.thursday_status = 3
            else:
                user_to_checkout.thursday_status = 2
            flash("Checked %s out" % user_to_checkout.fname)
        else:
            if user_to_checkout.thursday_status == 2:
                user_to_checkout.thursday_status = 0
            else:
                user_to_checkout.thursday_status = 1
            flash("Unchecked %s out" % user_to_checkout.fname)
        db.session.commit()
        return redirect('thursday_checkout')

    return render_template('thursday_checkout.html', user = user, four_digit_form = four_digit_form)

@app.route('/wednesday_counter')
def wednesday_counter():
    user = models.User.query.filter_by(username = session['username']).first()

    if not user:
        flash('Please login')
        return redirect('index')

    if not user.check_permission('admin'):
        flash('You must be an administrator to view this page')
        return redirect('index')
    checked_in = len(models.User.query.filter(or_(models.User.wednesday_status == 1, models.User.wednesday_status == 3)).all())
    checked_out = len(models.User.query.filter_by(wednesday_status = 3).all())

    return render_template('wednesday_counter.html', user = user, checked_in = checked_in, checked_out = checked_out)

@app.route('/thursday_counter')
def thursday_counter():
    user = models.User.query.filter_by(username = session['username']).first()

    if not user:
        flash('Please login')
        return redirect('index')

    if not user.check_permission('admin'):
        flash('You must be an administrator to view this page')
        return redirect('index')
    checked_in = len(models.User.query.filter(or_(models.User.thursday_status == 1, models.User.thursday_status == 3)).all())
    checked_out = len(models.User.query.filter_by(thursday_status = 3).all())

    return render_template('thursday_counter.html', user = user, checked_in = checked_in, checked_out = checked_out)

@app.route('/make_admin/<int:user_id>')
def toggle_admin(user_id = 0):
    user = models.User.query.filter_by(username = session['username']).first()

    if not user:
        flash('Please login')
        return redirect('index')

    if not user.check_permission('admin'):
        flash('You must be an administrator to view this page')
        return redirect('index')
        
    u = models.User.query.filter_by(id = user_id).first()
    if not u:
        flash('User not found')
        return redirect('users')
        
    if u.check_permission('admin'):
        u.remove_permission('admin')
        flash('%s\'s admin privledges revoked!' % u.fname)
    else:
        u.add_permission('admin')
        flash('%s made admin!' % u.fname)
    return redirect(url_for('admin_user_view', user_id = u.id))

@app.route('/users_wednesday_checked_in', methods = ['GET', 'POST'])
@app.route('/users_wednesday_checked_in/<int:page>', methods = ['GET', 'POST'])
@app.route('/users_wednesday_checked_in/<int:page>/', methods = ['GET', 'POST'])
@app.route('/users_wednesday_checked_in/<int:page>/<string:search_field>', methods = ['GET', 'POST'])
def users_wednesday_checked_in(page = 1, search_field = ""):
    user = models.User.query.filter_by(username = session['username']).first()

    if not user:
        flash('Please login')
        return redirect('index')

    if not user.check_permission('admin'):
        flash('You must be an administrator to view this page')
        return redirect('index')

    search_form = SearchForm()

    users = models.User.query.filter(models.User.wednesday_status == 1)
    
    if search_form.validate_on_submit():
        search_field = search_form.search_field.data
        return redirect(url_for('users_wednesday_checked_in', page = page, search_field = search_field))

    if search_field == 'Red Cross':
        search_field = 'red_cross'
    elif search_field == 'ARISTA':
        search_field = 'arista'
    elif search_field == 'Big Sibs':
        search_field = 'big_sibs'
    elif search_field == 'Key Club':
        search_field = 'key_club'
        
    if search_field == 'thursday' or search_field == 'Thursday':
        users = users.filter_by(thursday = True, thursday_excused = False)
    elif search_field == 'wednesday' or search_field == 'Wednesday':
        users = users.filter_by(wednesday = True, wednesday_excused = False)
        
    else:
        users = users.filter(
            or_(models.User.fname.like('%' + search_field + '%'),
                models.User.lname.like('%' + search_field + '%'),
                models.User.nickname.like('%' + search_field + '%'),
                models.User.four_digit.like('%' + search_field + '%'),
                models.User.organizations.like('%' + search_field + '%'),
                models.User.osis.like('%' + search_field + '%')))

    users = users.paginate(page, app.config['ELEMENTS_PER_PAGE'], False)

    return render_template('users_wednesday_checked_in.html', user = user, users = users, organizations = app.config['ORGANIZATIONS'], search_form = search_form, search_field = search_field)

@app.route('/users_wednesday_checked_out', methods = ['GET', 'POST'])
@app.route('/users_wednesday_checked_out/<int:page>', methods = ['GET', 'POST'])
@app.route('/users_wednesday_checked_out/<int:page>/', methods = ['GET', 'POST'])
@app.route('/users_wednesday_checked_out/<int:page>/<string:search_field>', methods = ['GET', 'POST'])
def users_wednesday_checked_out(page = 1, search_field = ""):
    user = models.User.query.filter_by(username = session['username']).first()

    if not user:
        flash('Please login')
        return redirect('index')

    if not user.check_permission('admin'):
        flash('You must be an administrator to view this page')
        return redirect('index')

    search_form = SearchForm()

    users = models.User.query.filter(or_(models.User.wednesday_status == 2, models.User.wednesday_status == 3))
    
    if search_form.validate_on_submit():
        search_field = search_form.search_field.data
        return redirect(url_for('users_wednesday_checked_out', page = page, search_field = search_field))

    if search_field == 'Red Cross':
        search_field = 'red_cross'
    elif search_field == 'ARISTA':
        search_field = 'arista'
    elif search_field == 'Big Sibs':
        search_field = 'big_sibs'
    elif search_field == 'Key Club':
        search_field = 'key_club'
        
    if search_field == 'thursday' or search_field == 'Thursday':
        users = users.filter_by(thursday = True, thursday_excused = False)
    elif search_field == 'wednesday' or search_field == 'Wednesday':
        users = users.filter_by(wednesday = True, wednesday_excused = False)
        
    else:
        users = users.filter(
            or_(models.User.fname.like('%' + search_field + '%'),
                models.User.lname.like('%' + search_field + '%'),
                models.User.nickname.like('%' + search_field + '%'),
                models.User.four_digit.like('%' + search_field + '%'),
                models.User.organizations.like('%' + search_field + '%'),
                models.User.osis.like('%' + search_field + '%')))

    users = users.paginate(page, app.config['ELEMENTS_PER_PAGE'], False)

    return render_template('users_wednesday_checked_out.html', user = user, users = users, organizations = app.config['ORGANIZATIONS'], search_form = search_form, search_field = search_field)

@app.route('/users_thursday_checked_in', methods = ['GET', 'POST'])
@app.route('/users_thursday_checked_in/<int:page>', methods = ['GET', 'POST'])
@app.route('/users_thursday_checked_in/<int:page>/', methods = ['GET', 'POST'])
@app.route('/users_thursday_checked_in/<int:page>/<string:search_field>', methods = ['GET', 'POST'])
def users_thursday_checked_in(page = 1, search_field = ""):
    user = models.User.query.filter_by(username = session['username']).first()

    if not user:
        flash('Please login')
        return redirect('index')

    if not user.check_permission('admin'):
        flash('You must be an administrator to view this page')
        return redirect('index')

    search_form = SearchForm()

    users = models.User.query.filter(models.User.thursday_status == 1)
    
    if search_form.validate_on_submit():
        search_field = search_form.search_field.data
        return redirect(url_for('users_thursday_checked_in', page = page, search_field = search_field))

    if search_field == 'Red Cross':
        search_field = 'red_cross'
    elif search_field == 'ARISTA':
        search_field = 'arista'
    elif search_field == 'Big Sibs':
        search_field = 'big_sibs'
    elif search_field == 'Key Club':
        search_field = 'key_club'
        
    if search_field == 'thursday' or search_field == 'Thursday':
        users = users.filter_by(thursday = True, thursday_excused = False)
    elif search_field == 'wednesday' or search_field == 'Wednesday':
        users = users.filter_by(wednesday = True, wednesday_excused = False)
        
    else:
        users = users.filter(
            or_(models.User.fname.like('%' + search_field + '%'),
                models.User.lname.like('%' + search_field + '%'),
                models.User.nickname.like('%' + search_field + '%'),
                models.User.four_digit.like('%' + search_field + '%'),
                models.User.organizations.like('%' + search_field + '%'),
                models.User.osis.like('%' + search_field + '%')))

    users = users.paginate(page, app.config['ELEMENTS_PER_PAGE'], False)

    return render_template('users_thursday_checked_in.html', user = user, users = users, organizations = app.config['ORGANIZATIONS'], search_form = search_form, search_field = search_field)

@app.route('/users_thursday_checked_out', methods = ['GET', 'POST'])
@app.route('/users_thursday_checked_out/<int:page>', methods = ['GET', 'POST'])
@app.route('/users_thursday_checked_out/<int:page>/', methods = ['GET', 'POST'])
@app.route('/users_thursday_checked_out/<int:page>/<string:search_field>', methods = ['GET', 'POST'])
def users_thursday_checked_out(page = 1, search_field = ""):
    user = models.User.query.filter_by(username = session['username']).first()

    if not user:
        flash('Please login')
        return redirect('index')

    if not user.check_permission('admin'):
        flash('You must be an administrator to view this page')
        return redirect('index')

    search_form = SearchForm()

    users = models.User.query.filter(or_(models.User.thursday_status == 2, models.User.thursday_status == 3))

    if search_form.validate_on_submit():
        search_field = search_form.search_field.data
        return redirect(url_for('users_thursday_checked_out', page = page, search_field = search_field))

    if search_field == 'Red Cross':
        search_field = 'red_cross'
    elif search_field == 'ARISTA':
        search_field = 'arista'
    elif search_field == 'Big Sibs':
        search_field = 'big_sibs'
    elif search_field == 'Key Club':
        search_field = 'key_club'
        
    if search_field == 'thursday' or search_field == 'Thursday':
        users = users.filter_by(thursday = True, thursday_excused = False)
    elif search_field == 'wednesday' or search_field == 'Wednesday':
        users = users.filter_by(wednesday = True, wednesday_excused = False)
        
    else:
        users = users.filter(
            or_(models.User.fname.like('%' + search_field + '%'),
                models.User.lname.like('%' + search_field + '%'),
                models.User.nickname.like('%' + search_field + '%'),
                models.User.four_digit.like('%' + search_field + '%'),
                models.User.organizations.like('%' + search_field + '%'),
                models.User.osis.like('%' + search_field + '%')))

    users = users.paginate(page, app.config['ELEMENTS_PER_PAGE'], False)

    return render_template('users_thursday_checked_out.html', user = user, users = users, organizations = app.config['ORGANIZATIONS'], search_form = search_form, search_field = search_field)

@app.route('/users_admins', methods = ['GET', 'POST'])
@app.route('/users_admins/<int:page>', methods = ['GET', 'POST'])
@app.route('/users_admins/<int:page>/', methods = ['GET', 'POST'])
@app.route('/users_admins/<int:page>/<string:search_field>', methods = ['GET', 'POST'])
def users_admins(page = 1, search_field = ""):
    search_form = SearchForm()
    user = models.User.query.filter_by(username = session['username']).first()

    if not user:
        flash('Please login')
        return redirect('index')

    if not user.check_permission('admin'):
        flash('You must be an administrator to view this page')
        return redirect('index')

    users = models.User.query.filter(models.User.permissions.like('%admin%'))

    if search_form.validate_on_submit():
        search_field = search_form.search_field.data
        return redirect(url_for('users_admins', page = page, search_field = search_field))

    if search_field == 'Red Cross':
        search_field = 'red_cross'
    elif search_field == 'ARISTA':
        search_field = 'arista'
    elif search_field == 'Big Sibs':
        search_field = 'big_sibs'
    elif search_field == 'Key Club':
        search_field = 'key_club'
        
    if search_field == 'thursday' or search_field == 'Thursday':
        users = users.filter_by(thursday = True, thursday_excused = False)
    elif search_field == 'wednesday' or search_field == 'Wednesday':
        users = users.filter_by(wednesday = True, wednesday_excused = False)
        
    else:
        users = users.filter(
            or_(models.User.fname.like('%' + search_field + '%'),
                models.User.lname.like('%' + search_field + '%'),
                models.User.nickname.like('%' + search_field + '%'),
                models.User.four_digit.like('%' + search_field + '%'),
                models.User.organizations.like('%' + search_field + '%'),
                models.User.osis.like('%' + search_field + '%')))

    users = users.paginate(page, app.config['ELEMENTS_PER_PAGE'], False)
    
    return render_template('users_admins.html', user = user, users = users, organizations = app.config['ORGANIZATIONS'], search_form = search_form, search_field = search_field)



