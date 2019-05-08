from flask import Flask,request,jsonify,render_template
import json
import sqlite3
import ast
db=sqlite3.connect('database.db')
db.execute("CREATE TABLE IF NOT EXISTS tab(id INTEGER PRIMARY KEY,name VARCHAR(25),sprite VARCHAR(255),fg VARCHAR(255),bg VARCHAR(255),desc VARCHAR(255))")


app=Flask(__name__)
@app.route('/api/pokemon/<int:id>', methods=['GET'])
def send(id):
    db=sqlite3.connect('database.db')
    con=db.cursor()
    con.execute("select * from tab where id=?",(str(id),))
    data=con.fetchall()
    if(len(data)==0):
        return render_template("404.html"),404
    data=data[0]
    #print("\n\n\n\n\n\n",data,"\n\n\n\n\n\n\n")
    s="{'pokemon': {'id': '"+str(data[0])+"','name': '"+str(data[1])+"','sprite': '"+str(data[2])+"','cardColours': {'fg': '"+str(data[3])+"','bg': '"+str(data[4])+"','desc': '"+str(data[5])+"'}"+"}"+"}"
    #s='{"pokemon": {"id": '+str(data[0])+',"name": "'+str(data[1])+',"sprite": '+data[2]+',"cardColours": {"fg": '+data[3]+',"bg": '+data[4]+',"desc": '+data[5]+'}'+'}'+'}'
    con.close()
    s=ast.literal_eval(s)
    s['pokemon']['id']=int(s['pokemon']['id'])
    return jsonify(s)

@app.route('/api/pokemon/', methods=['POST'])
def insert():
    if(request.json):
        with sqlite3.connect('database.db') as db:
            con=db.cursor()
            con.execute("INSERT INTO tab(name,sprite,fg,bg,desc)VALUES(?,?,?,?,?)",(request.json['pokemon']['name'],request.json['pokemon']['sprite'],str(request.json['pokemon']['cardColours']['fg']),str(request.json['pokemon']['cardColours']['bg']),str(request.json['pokemon']['cardColours']['desc'])))
            lastid=con.execute("SELECT max(id) from tab").fetchall()[0][0]
            #print(lastid)
            con.execute("select * from tab where id=?",(str(lastid),))
            data=con.fetchall()[0]
            #print(data)
            s="{'pokemon': {'id': '"+str(data[0])+"','name': '"+str(data[1])+"','sprite': '"+str(data[2])+"','cardColours': {'fg': '"+str(data[3])+"','bg': '"+str(data[4])+"','desc': '"+str(data[5])+"'}"+"}"+"}"
            #print(type(s),"\n\n\n\n\n\n",s,"\n\n\n\n\n\n\n")
            db.commit()
            s=ast.literal_eval(s)
            s['pokemon']['id']=int(s['pokemon']['id'])
    return jsonify(s)

@app.route('/api/pokemon/<int:id>', methods=['PATCH'])
def update(id):
    db=sqlite3.connect('database.db')
    con=db.cursor()
    con.execute("select * from tab where id=?",(str(id),))
    data=con.fetchall()
    if(len(data)==0):
        return render_template("404.html"),404
    data=data[0]
    
    q=[]
    if(request.json):
        if('name' in request.json['pokemon']):
            q.append('name')
            q.append(request.json['pokemon']['name'])
            q.append(str(id))
            q=tuple(q)
            db.execute("UPDATE tab SET %s='%s' WHERE id=%s"%q)
        q=[]
        if('sprite' in request.json['pokemon']):
            q.append('sprite')
            q.append(request.json['pokemon']['sprite'])
            q.append(str(id))
            q=tuple(q)
            db.execute("UPDATE tab SET %s='%s' WHERE id=%s"%q)
        q=[]
        if('cardColours' in request.json['pokemon']):
            q.append('fg')
            q.append(request.json['pokemon']['cardColours']['fg'])
            q.append('bg')
            q.append(request.json['pokemon']['cardColours']['bg'])
            q.append('desc')
            q.append(request.json['pokemon']['cardColours']['desc'])
            q.append(str(id))
            q=tuple(q)
            db.execute("UPDATE tab SET %s='%s',%s='%s',%s='%s' WHERE id=%s"%q)
    con.execute("select * from tab where id=?",(str(id),))
    data=con.fetchall()[0]
    #print(data)
    s="{'pokemon': {'id': '"+str(data[0])+"','name': '"+str(data[1])+"','sprite': '"+str(data[2])+"','cardColours': {'fg': '"+str(data[3])+"','bg': '"+str(data[4])+"','desc': '"+str(data[5])+"'}"+"}"+"}"
    db.commit()
    s=ast.literal_eval(s)
    s['pokemon']['id']=int(s['pokemon']['id'])
    return jsonify(s)

@app.route('/api/pokemon/<int:id>', methods=['DELETE'])
def remove(id):
    db=sqlite3.connect('database.db')
    con=db.cursor()
    con.execute("select * from tab where id=?",(str(id),))
    
    data=con.fetchall()
    if(len(data)==0):
        return render_template("404.html"),404
    data=data[0]

    s="{'pokemon': {'id': '"+str(data[0])+"','name': '"+str(data[1])+"','sprite': '"+str(data[2])+"','cardColours': {'fg': '"+str(data[3])+"','bg': '"+str(data[4])+"','desc': '"+str(data[5])+"'}"+"}"+"}"
    con.execute("delete from tab where id=?",(str(id),))
    db.commit()
    con.close()
    s=ast.literal_eval(s)
    s['pokemon']['id']=int(s['pokemon']['id'])
    return jsonify(s)
app.run(port=8006,debug=True)

db.commit()
db.close()

