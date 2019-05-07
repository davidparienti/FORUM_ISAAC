from flask import render_template,request, redirect, url_for,flash,session
from models import app, db, User, Discussion, Message
from utils import validate_password

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#hello this is just for a second commit


@app.route('/')
def index():
  discussions = Discussion.query.all()
  return render_template('index.html', discussions=discussions,session=session)


@app.route('/messages/<int:discussion_id>/', methods=['POST', 'GET'])
def messages(discussion_id):
	if request.method == 'POST':
		user = User.query.filter_by(username=session['username']).first()
		message = Message(
			text=request.form['text'], 
			discussion_id=discussion_id, 
			user_id=user.id)
		db.session.add(message)
		db.session.commit()    

	messages = Message.query.filter_by(discussion_id=discussion_id).order_by(Message.date.desc()).all()
	# fonction "order_by" pour afficher la liste du plus recent au plus ancien
	discussion = Discussion.query.filter_by(id=discussion_id).first()

	for message in messages:
		# print(message.user_id)
		message.user = User.query.filter_by(id=message.user_id).first()
		# print(user)
	return render_template('messages.html',messages=messages, discussion=discussion)

@app.route('/signup',methods = ['GET', 'POST'])
def signup():
	if 'username' in session:
		return redirect(url_for('index'))
	if request.method == 'POST':
		username = request.form['username'],
		password = request.form['password']

		if User.query.filter_by(username=request.form['username']).first() == None:
			if validate_password(password):
				user = User(username=request.form['username'],password=password)
				# flash('User saved succefuly')
				db.session.add(user)
				db.session.commit()
				session['username'] = username
				return redirect(url_for('index'))
			else:
				flash(' password is too weak')
		else:
			flash('Username already exist')
	return render_template('signup.html')


@app.route('/login',methods = ['GET', 'POST'])
def login():
	if 'chances' not in session:
		session['chances'] = 3

	if 'username' in session:
		return redirect(url_for('index'))

	if request.method == 'POST':
		if session['chances'] <= 1:
			flash ('Too many login attempts')
		else:
			user = User.query.filter_by(
				username=request.form['username'],
				password=request.form['password']
			).first()

			if user:
				session['username'] = request.form['username']
				return redirect(url_for('index'))

			else:
				session['chances'] -= 1  
				flash('Invalid credentials, you have {} chances remaining'.format(session['chances']))

	return render_template('login.html')

@app.route('/logout')
def logout():
	session.pop('username')
	return redirect(url_for('index'))

@app.route('/profil/<int:user_id>',methods = ['GET', 'POST'])
def profil(user_id):
	user = User.query.filter_by(id=user_id).first()
	messages = Message.query.filter_by(user_id=user_id).all()

	return render_template('profil.html', user=user, messages=messages)

	# if request.method == 'POST':
	# 	if 'new-username' in request.form:
	# 		new_username=request.form['new-username']
	# 		searched_user= User.query.filter_by(username=new_username).first()
	# 		if searched_user == None:
	# 			user.username = new_username
	# 			db.session.commit()
	# 			session['username'] = new_username
	# 			return redirect(request.path,code=302)
	# 		else:
	# 			flash('username is already taken')			

	# 	elif 'old-password' in request.form:
	# 		old_password=request.form['old-password']
	# 		new_password=request.form['new-password']
	# 		user= User.query.filter_by(username=session['username'], password=old_password).first()

	# 		if user != None:
	# 			if validate_password(new_password) and new_password != old_password:
	# 				user.password = new_password
	# 				flash ('You change your password with success')
	# 				db.session.commit()
	# 			else:
	# 			  	  flash('New password is too weak')   

	# 		else:
	# 			flash('invalid password')

	# 			return redirect(request.path,code=302)    

	# return render_template('profil.html', user=user, messages=messages)

@app.route('/profil/<int:user_id>/password',methods = ['GET', 'POST'])
def password_update(user_id):
	if 'old-password' in request.form:
		old_password=request.form['old-password']
		new_password=request.form['new-password']
		user= User.query.filter_by(username=session['username'], password=old_password).first()

		if user != None:
			if validate_password(new_password) and new_password != old_password:
				user.password = new_password
				flash ('You change your password with success')
				db.session.commit()
			else:
				user = User.query.filter_by(username=session['username']).first()
				flash('invalid password')  
   
	return redirect(url_for('profil', user_id=user.id))


@app.route('/profil/<int:user_id>/username',methods = ['GET', 'POST'])
def username_update(user_id):
	user = User.query.filter_by(id=user_id).first()
	if 'new-username' in request.form:
		new_username=request.form['new-username']
		searched_user= User.query.filter_by(username=new_username).first()
		if searched_user == None:
			user.username = new_username
			db.session.commit()
			session['username'] = new_username
		else:
			flash('username is already taken')
	return redirect(url_for('profil', user_id=user.id))