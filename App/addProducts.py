from flask import Flask, render_template, redirect, url_for,request

from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms import StringField, SubmitField,MultipleFileField
from wtforms.fields.core import IntegerField, SelectField , RadioField
from flask_uploads import UploadSet, configure_uploads,IMAGES
from wtforms.validators import DataRequired , Length, NumberRange
from flask_wtf.file import FileField, FileRequired, FileAllowed
import os
import sqlite3
basedir = os.path.abspath(os.path.dirname(__file__))
from App import app

Bootstrap(app)

# Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = 'this is secret'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'uploads') # you'll need to create a folder named uploads

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
conn = sqlite3.connect('buzzDatabase.db')
cur = conn.cursor()

def fetchEnumTable(tableName,columns ):
	conn = sqlite3.connect('buzzDatabase.db')
	cur = conn.cursor()
	query = "select "+columns+" from "+tableName
	data  = cur.execute(query).fetchall()
	return data

def insertData(q):
	conn = sqlite3.connect('buzzDatabase.db')
	cur = conn.cursor()

	cur.execute(q)
	return conn.commit()

class productForm(FlaskForm):
	types = fetchEnumTable("selling_opt","id,name")
	choices = fetchEnumTable("categories","id,name")
	photo = MultipleFileField(validators=[FileAllowed(photos, 'Image only!')])
	category = SelectField('Category',choices=choices, validators=[DataRequired()])
	title = StringField('Product Title', validators=[DataRequired()],_name="myCountry")
	description = StringField('Product Description', validators=[DataRequired()])
	quantity = IntegerField('Quantity', validators=[DataRequired(),NumberRange(min=1,max=None, message='Range should be >0')])
	type = RadioField('Sell type',choices=types, validators=[DataRequired()])
	tags = StringField('add Tags ')
	price = StringField(label=None)
	bidPrice = StringField("Bid base price")
	bidIncrement = StringField("minumum bid increase")
	submit = SubmitField('Submit')


@app.route('/addProduct', methods=['GET', 'POST'])
def addProducts():
	# names = get_names(ACTORS)
	# you must tell the variable 'form' what you named the class, above
	# 'form' is the variable name used in this template: index.html
	form = productForm()
	message=""
	tag_list = list(fetchEnumTable("tags","name"))
	finalTaglist= []
	for x in tag_list:
		finalTaglist.append(x[0].strip())
	print("lol i am called ",form.errors,form.validate_on_submit())
	if  form.validate_on_submit():
		for pic in form.photo.data:
			pic.filename = secure_filename(pic.filename)
			print(pic.filename,pic)
			filename = photos.save(pic)	
		print("done")
		title = form.title.data
		category = form.category.data
		description = form.description.data
		quantity = form.quantity.data
		type = form.type.data
		tags = form.tags.data
		query = """insert into products(category_id,user_id,product_description,title,product_availability,selling_option) values(%d,1,\'%s\',\'%s\',%d,%d)""" %(int(category) ,description, title, int(quantity),int(type))
		print(insertData(query))
		message = title+"  That actor is not name in our database."+category+" "+description+" "+str(quantity)+" "+type+" "+tags
	return render_template('addProduct.html', form=form, message=message ,tag_list=finalTaglist)

