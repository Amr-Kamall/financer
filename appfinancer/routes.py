from datetime import datetime
import os
from flask import render_template, request, url_for, flash, redirect 
from flask_login import login_required, login_user ,current_user, logout_user
from appfinancer.forms import  ImportForm, LoginForm, LoginFormadmin, AddForm , ExportForm
from appfinancer import  app , bcrypt , db
import sqlite3 as sql
from appfinancer.models import User, Exporttable, Importtable
from werkzeug.utils import secure_filename

#=======================================================================================

#=======================================================================================


selected_location = "1"
select_location = "1"
@app.route('/save_selected_location', methods=['POST'])
def save_selected_location():
    global selected_location
    data = request.get_json()
    selected_location = data['selectedLocation']
    print(selected_location)
    return 'تم حفظ القيمة بنجاح'

@app.route('/save_select_location', methods=['POST'])
def save_select_location():
    global select_location
    data = request.get_json()
    select_location = data['selectLocation']
    print(select_location)
    return 'تم حفظ القيمة بنجاح'




@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated :
        return redirect(url_for("home"))
    form = LoginForm()
    formadmin = LoginFormadmin()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user , remember = form.remember.data)
            next_page = request.args.get('next')
            flash(f"لقد تم دخولك بنجاح {current_user.name} اهلا بك ", 'success')
            return redirect(next_page) if next_page  else redirect(url_for('home'))
        else:
            flash('اسم المستخدم أو كلمة المرور غير صحيحة.', 'danger')
            formadmin.usernameadmin.data = ''  # مسح محتوى حقل اسم المستخدم
            formadmin.passwordadmin.data = ''  # مسح محتوى حقل كلمة المرور





#<------------------------------------------login admin-------------------------------------->
    elif formadmin.validate_on_submit():
        user = User.query.filter_by(username=formadmin.usernameadmin.data).first()
        if user and user.password == formadmin.passwordadmin.data:
            if user.username == 'admin':
                login_user(user , remember = formadmin.remember.data)
                next_page = request.args.get('next')
                flash(f"لقد تم دخولك بنجاح {current_user.name} اهلا بك ", 'success')
                return redirect(url_for('userpage'))
            else:
                flash('لا يسمح لك بالدخول.', 'danger')
        else:
            flash('اسم المستخدم أو كلمة المرور غير صحيحة.', 'danger')
            formadmin.usernameadmin.data = ''  # مسح محتوى حقل اسم المستخدم
            formadmin.passwordadmin.data = ''  # مسح محتوى حقل كلمة المرور

    return render_template('index.html', title='Financer', form=form, formadmin=formadmin )





@app.route('/home')
@login_required
def home():
    user_id = current_user.name


    con = sql.connect("instance/financer.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM exporttable WHERE user_id = ?",(user_id,))
    exporttable_cont = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM importtable WHERE user_id = ?",(user_id,))
    importtable_cont = cur.fetchone()[0]
     # حساب مجموع ارقام الصادره خلال اليوم
    cur.execute("SELECT SUM(price) FROM exporttable WHERE user_id=? AND dates >= date('now', 'start of day')", (user_id,))
    day_total = cur.fetchone()[0]

    # حساب مجموع ارقام الصادره خلال الشهر
    cur.execute("SELECT SUM(price) FROM exporttable WHERE user_id=? AND dates >= date('now', 'start of month')", (user_id,))
    month_total = cur.fetchone()[0]

    # حساب مجموع ارقام الصادره خلال السنة
    cur.execute("SELECT SUM(price) FROM exporttable WHERE user_id=? AND dates >= date('now', 'start of year')", (user_id,))
    year_total = cur.fetchone()[0]
     # حساب مجموع ارقام الوارده خلال اليوم
    cur.execute("SELECT SUM(price) FROM importtable WHERE user_id=? AND dates >= date('now', 'start of day')", (user_id,))
    day_import = cur.fetchone()[0]

    # حساب مجموع ارقام الوارده خلال الشهر
    cur.execute("SELECT SUM(price) FROM importtable WHERE user_id=? AND dates >= date('now', 'start of month')", (user_id,))
    month_import = cur.fetchone()[0]

    # حساب مجموع ارقام الوارده خلال السنة
    cur.execute("SELECT SUM(price) FROM importtable WHERE user_id=? AND dates >= date('now', 'start of year')", (user_id,))
    year_import = cur.fetchone()[0]

    # إغلاق الاتصال بقاعدة البيانات
    cur.close()
    con.close()

    # تخزين نتائج الصادره في متغيرات
    day_total = day_total if day_total else 0
    month_total = month_total if month_total else 0
    year_total = year_total if year_total else 0
    # تخزين نتائج الوارده في متغيرات
    day_import = day_import if day_import else 0
    month_import = month_import if month_import else 0
    year_import= year_import if year_import else 0


    return render_template("home.html" , 
                           username = current_user , 
                           exporttable_cont = exporttable_cont , 
                           importtable_cont = importtable_cont,
                           day_total=day_total,
                           month_total=month_total,
                           year_total=year_total,
                           day_import=day_import,
                           month_import=month_import,
                           year_import=year_import
                           )

@app.route('/pdfexport')
@login_required
def pdfexport():

    return render_template("pdfexport.html")


@app.route('/adminimport')
@login_required
def adminimport():
    global select_location

    con = sql.connect("instance/financer.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT DISTINCT locationwork FROM users")
    location = [row[0] for row in cur.fetchall()]
    cur.execute("select * from importtable")
    if select_location == '1':
        data = cur.fetchall()
    else:
        cur.execute("SELECT * FROM users JOIN importtable ON users.name = importtable.user_id WHERE users.locationwork = ?" , (select_location,))
        data = cur.fetchall()
    return render_template("adminimport.html", datas=data, location=location )


@app.route('/adminexport' , methods=['GET', 'POST'])
@login_required
def adminexport():

    global selected_location

    con = sql.connect("instance/financer.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT DISTINCT locationwork FROM users")
    locations = [row[0] for row in cur.fetchall()]
    cur.execute("select * from exporttable")
    if selected_location == '1':
        data = cur.fetchall()
    else:
        cur.execute("SELECT * FROM users JOIN exporttable ON users.name = exporttable.user_id WHERE users.locationwork = ?" , (selected_location,))
        data = cur.fetchall()
    return render_template("adminexport.html", datas=data, locations=locations )




#<------------------------------------user-------------------------------------------------------->
@app.route('/userpage')
@login_required
def userpage():
    con = sql.connect("instance/financer.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from users")
    data = cur.fetchall()
    return  render_template('userpage.html' , datas =  data)


@app.route('/add_user' , methods = ['GET','POST'] )
@login_required
def add_user():

    formِadd = AddForm()

    if formِadd.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(formِadd.password.data).decode('utf-8')
        password = formِadd.password.data
        user = User(
            name=formِadd.name.data , 
            username=formِadd.username.data , 
            password=password ,
            locationwork=formِadd.locationwork.data
            )
        
        db.session.add(user)
        db.session.commit()
        flash(f"   لقد تم تسجيل {formِadd.username.data} بنجاح  ", 'success')
        return redirect(url_for("userpage"))
    return render_template("add_user.html" , formِadd=formِadd)


@app.route("/edit_user/<string:id>" , methods = ['POST', 'GET'])
@login_required
def edit_user(id):

    if request.method == 'POST':
        name     = request.form['name']
        username = request.form['username']
        password = request.form['password']
        locationwork = request.form['locationwork']
        con = sql.connect("instance/financer.db")
        cur = con.cursor()
        cur.execute("UPDATE users SET name=?, passWord=?, locationwork=?  , userName=? WHERE id =? ", (name, password, locationwork, username , id))
        con.commit()
        flash('لقد تمت تحديث البيانات بنجاح' , 'success')
        return redirect(url_for("userpage"))

    con = sql.connect("instance/financer.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from users where ID = ?", (id,))
    data = cur.fetchone()

    return render_template('edit_user.html' , datas = data)


@app.route("/delete_user/<string:id>" ,methods =['GET'])
@login_required
def delete_user(id):
    con = sql.connect("instance/financer.db")
    cur = con.cursor()
    cur.execute("delete from  users where ID = ?" , (id,))
    con.commit()
    flash('لقد تم حذف المستخدم بنجاح' , 'warning')
    
    
    return redirect(url_for("userpage"))
#<------------------------------------------end  user page ------------------------------------------->









#<------------------------------------export-------------------------------------------------------->
@app.route('/exportpage')
@login_required

def exportpage():
    con = sql.connect("instance/financer.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from exporttable")
    data = cur.fetchall()
    return  render_template('exportpage.html' , datas =  data)



@app.route('/add_export', methods=['GET', 'POST'])
@login_required
def add_export():
    exportform = ExportForm()

    if exportform.validate_on_submit():
        uploaded_file = request.files['image_file']
        if uploaded_file:
            filename = secure_filename(uploaded_file.filename)
            filepath = os.path.normpath(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            uploaded_file.save(filepath)

            exports = Exporttable(
                band=exportform.band.data,
                price=exportform.price.data,
                amount=exportform.amount.data,
                note=exportform.note.data,
                image_file=filename,
                user_id=current_user.name
            )

            db.session.add(exports)
            db.session.commit()


            flash("تمت إضافة البيانات بنجاح", 'success')
            return redirect(url_for("exportpage"))
    return render_template("add_export.html", exportform=exportform )





@app.route("/edit_export/<string:id>", methods=['POST', 'GET'])
@login_required
def edit_export(id):
    if request.method == 'POST':
        band = request.form['band']
        price = request.form['price']
        amount = request.form['amount']
        note = request.form['note']
        upload_file = request.files['image_file']
        user_id = request.form['user_id']

        if upload_file:
            filename = secure_filename(upload_file.filename)
            file_path = os.path.normpath(os.path.join(app.config['UPLOAD_FOLDER'] , filename))
            filepath = os.path.normpath(os.path.join( filename))
            upload_file.save(file_path)

        con = sql.connect("instance/financer.db")
        cur = con.cursor()
        cur.execute("UPDATE exporttable SET band=?, price=?, amount=?, note=?, image_file=?, user_id=? WHERE id=?",
                    (band, price, amount, note, filepath, user_id, id))
        con.commit()
        flash('لقد تمت تحديث البيانات بنجاح', 'success')
        return redirect(url_for("exportpage"))

    con = sql.connect("instance/financer.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from exporttable where ID = ?", (id,))
    data = cur.fetchone()

    return render_template('edit_export.html', datas=data)



@app.route("/delete_export/<string:id>" ,methods =['GET'])
@login_required
def delete_export(id):
    con = sql.connect("instance/financer.db")
    cur = con.cursor()
    cur.execute("delete from  exporttable where ID = ?" , (id,))
    con.commit()
    flash('لقد تم حذف البند بنجاح' , 'warning')
    
    
    return redirect(request.referrer)
#<------------------------------------------end  export page ------------------------------------------->







#<------------------------------------import-------------------------------------------------------->
@app.route('/importpage')
@login_required

def importpage():
    con = sql.connect("instance/financer.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from importtable")
    data = cur.fetchall()
    return  render_template('importpage.html' , datas =  data)


@app.route('/add_import' , methods = ['GET','POST'] )
@login_required
def add_import():

    importform = ImportForm()

    if importform.validate_on_submit():
        uploaded_file = request.files['image_file']
        if uploaded_file:
            filename = secure_filename(uploaded_file.filename)
            filepath = os.path.normpath(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            uploaded_file.save(filepath)

            imports = Importtable(
                band = importform.band.data ,
                price = importform.price.data ,
                amount = importform.amount.data ,
                note = importform.note.data ,
                image_file = filename ,
                user_id = current_user.name
            )
        
        db.session.add(imports)
        db.session.commit()
        flash(f"   لقد تم الاضافة بنجاح  ", 'success')
        return redirect(url_for("importpage"))
    return render_template("add_import.html" , importform=importform )


@app.route("/edit_import/<string:id>", methods=['POST', 'GET'])
@login_required
def edit_import(id):
    if request.method == 'POST':
        band = request.form['band']
        price = request.form['price']
        amount = request.form['amount']
        note = request.form['note']
        upload_file = request.files['image_file']
        user_id = request.form['user_id']

        if upload_file:
            filename = secure_filename(upload_file.filename)
            file_path = os.path.normpath(os.path.join(app.config['UPLOAD_FOLDER'] , filename))
            filepath = os.path.normpath(os.path.join( filename))
            upload_file.save(file_path)

        con = sql.connect("instance/financer.db")
        cur = con.cursor()
        cur.execute("UPDATE importtable SET band=?, price=?, amount=?, note=?, image_file=?, user_id=? WHERE id=?",
                    (band, price, amount, note, filepath, user_id, id))
        con.commit()
        flash('لقد تمت تحديث البيانات بنجاح', 'success')
        return redirect(url_for("importpage"))

    con = sql.connect("instance/financer.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from importtable where ID = ?", (id,))
    data = cur.fetchone()

    return render_template('edit_import.html', datas=data)


@app.route("/delete_import/<string:id>" ,methods =['GET'])
@login_required
def delete_import(id):
    con = sql.connect("instance/financer.db")
    cur = con.cursor()
    cur.execute("delete from  importtable where ID = ?" , (id,))
    con.commit()
    flash('لقد تم حذف البند بنجاح' , 'warning')
    
    
    return redirect(request.referrer)
#<------------------------------------------end  import page ------------------------------------------->





@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))