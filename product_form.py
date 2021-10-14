from datetime import time
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.core import IntegerField, SelectField , RadioField
from wtforms.validators import DataRequired , Length, NumberRange
import sqlite3

import sqlite3

conn = sqlite3.connect('buzzDatabase.db')
cur = conn.cursor()

def fetchEnumTable(tableName,columns ):
	conn = sqlite3.connect('buzzDatabase.db')
	cur = conn.cursor()
	query = "select "+columns+" from "+tableName
	data  = cur.execute(query).fetchall()
	print(data)
	return data

def insertData(q):
	conn = sqlite3.connect('buzzDatabase.db')
	cur = conn.cursor()

	cur.execute(q)
	return conn.commit()

class NameForm(FlaskForm):
	choices = ["loda","lasan"]
	types = fetchEnumTable("selling_opt","selling_option,selling_type")
	choices = fetchEnumTable("categories","category_id,category_name")
	category = SelectField('Category',choices=choices, validators=[DataRequired()])
	title = StringField('Product Title', validators=[DataRequired()],_name="myCountry")
	description = StringField('Product Description', validators=[DataRequired()])
	quantity = IntegerField('How many products in number avaialable', validators=[DataRequired(),NumberRange(min=1,max=None, message='Range should be >0')])
	type = RadioField('Sell type',choices=types, validators=[DataRequired()])
	tags = StringField('add Tags ')
	submit = SubmitField('Submit')

app = Flask(__name__)
Bootstrap(app)

# Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

@app.route('/', methods=['GET', 'POST'])
def index():
	# names = get_names(ACTORS)
	# you must tell the variable 'form' what you named the class, above
	# 'form' is the variable name used in this template: index.html
	form = NameForm()
	message = ""
	tag_list = list(fetchEnumTable("tags","tag_name"))
	finalTaglist= []
	for x in tag_list:
		finalTaglist.append(x[0].strip())
	print(finalTaglist)
	if form.validate_on_submit():
		title = form.title.data
		category = form.category.data
		description = form.description.data
		quantity = form.quantity.data
		type = form.type.data
		tags = form.tags.data
		query = """insert into products(category_id,user_id,product_description,title,product_availability,selling_option) values(%d,1,\'%s\',\'%s\',%d,%d)""" %(int(category) ,description, title, int(quantity),int(type))
		print(insertData(query))
		message = title+"  That actor is not name in our database."+category+" "+description+" "+str(quantity)+" "+type+" "+tags
	return render_template('index.html', form=form, message=message ,tag_list=finalTaglist)
# Flask-Bootstrap requires this line

if __name__ == '__main__':
	app.run(host="0.0.0.0",debug=True)