from tkinter import *
import tkinter.messagebox as Mb
import mysql.connector
from sklearn import linear_model
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

fac=mysql.connector.connect(
    host="localhost",
    user="Username",
    password="Password",
    database="project"
    )
c=fac.cursor(buffered=True)

def login_db():


    def logged():


        def farmer():


            def add_p(mail):


                def add_p_db():
                    c.execute("select uid from users where mail_id='"+mail+"'")
                    r=c.fetchall()
                    for i in r:
                        id=i
                        break
                    id=int(id[0])
                    pid=e2.get()
                    pname=e3.get()
                    minq=e5.get()
                    maxq=e4.get()
                    pr=e6.get()

                    if(pid=="" or pid=="" or pname=="" or minq =="" or maxq =="" or pr==""):
                        Mb.showinfo("Insert Status","All fields are required")
                    else:
                        
                        c.execute("select pid from products")
                        for i in c:
                            #print(i)
                            if i[0]==int(pid):
                                Mb.showerror("Create Error","Product already present")
                        else:
                            c.execute("insert into products values('"+pid+"','"+pname +"','"+minq+"','"+maxq+"','"+pr+"','"+str(id)+"')")
                            Mb.showinfo("Insert Status","Added Succussfully")
                            c.execute("commit")

                            e2.delete(0,'end')
                            e3.delete(0,'end')
                            e4.delete(0,'end')
                            e5.delete(0,'end')
                            e6.delete(0,'end')



                #farmer_win.destroy()
                add_p_win=Toplevel(farmer_win)
                add_p_win.title("Farmer - Add Product")
                add_p_win.geometry("500x300")

                l1=Label(add_p_win,text="Add Product Page",font="times 15")
                l1.grid(row=1,column=1)
                l3=Label(add_p_win,text="Product-Id",font="times 15")
                l3.grid(row=2,column=1)
                l4=Label(add_p_win,text="Product Name",font="times 15")
                l4.grid(row=3,column=1)
                l5=Label(add_p_win,text="Total quantity",font="times 15")
                l5.grid(row=4,column=1)
                l6=Label(add_p_win,text="Minimum quantity",font="times 15")
                l6.grid(row=5,column=1)
                l7=Label(add_p_win,text="Price",font="times 15")
                l7.grid(row=6,column=1)


                
                pid=IntVar()
                e2=Entry(add_p_win,textvariable=pid)
                e2.grid(row=2,column=2)
                pname=StringVar()
                e3=Entry(add_p_win,textvariable=pname)
                e3.grid(row=3,column=2)
                min_q=IntVar()
                e4=Entry(add_p_win,textvariable=min_q)
                e4.grid(row=4,column=2)
                max_q=IntVar()
                e5=Entry(add_p_win,textvariable=max_q)
                e5.grid(row=5,column=2)
                p=IntVar()
                e6=Entry(add_p_win,textvariable=p)
                e6.grid(row=6,column=2)


                b1=Button(add_p_win,text="Add Product",width=20,command=add_p_db)
                b1.grid(row=7,column=2)
                
                
                


            def rem_p(mail):

                def rem_p_db():
                    pi=e1.get()
                    try:
                        c.execute("select uid from users where mail_id='"+mail+"'")
                        r=c.fetchall()
                        for i in r:
                            id1=i
                            break
                        id1=int(id1[0])
                        #print(id1)
                        c.execute("delete from products where pid='"+str(pi)+"' and user_id='"+str(id1)+"'")
                        Mb.showinfo("Product Status","Product Deleted Sucussfully")
                        c.execute("commit")
                    except:
                        Mb.showerror("Product Status","Product not found")
                    
                
            


                #farmer_win.destroy()
                rem_p_win=Toplevel(farmer_win)
                rem_p_win.title("Farmer - Remove Product")
                rem_p_win.geometry("500x300")

                l1=Label(rem_p_win,text="Remove Product Page",font="times 15")
                l1.grid(row=1,column=1)
                l2=Label(rem_p_win,text="Product-Id",font="times 15")
                l2.grid(row=2,column=1)
                

                pid=IntVar()
                e1=Entry(rem_p_win,textvariable=pid)
                e1.grid(row=2,column=2)
                

                b1=Button(rem_p_win,text="Remove Product",width=20,command=rem_p_db)
                b1.grid(row=4,column=2)
            
                


            def predict(a,my_p_win):
                    #print("inside",a)
                    c.execute("select sum(sale) from sales where product_id="+str(a)+" group by dot order by dot")
                    results = c.fetchall()
                    saleslist = np.array(list(map(lambda x:[x[0]],results))).reshape(-1,1)
                    if len(saleslist)==0:
                        Mb.showerror("Predict Status","The Product has not made any sales yet!")
                    else:
                        idlist = np.array(list(map(lambda x:x,range(0,len(saleslist))))).reshape(-1,1)
                        regr = linear_model.LinearRegression()
                        regr.fit(idlist,saleslist)
                        print("Coefficient - ",regr.coef_)
                        print("Intercept - ",regr.intercept_)
                        count = len(idlist)
                        id = []
                        predict = []
                        for i in range(5):
                            predict.append(regr.predict(np.array([count+i]).reshape(-1,1))[0][0])
                            id.append(count+i)
                        graph_win = Toplevel(my_p_win)
                        graph_win.geometry("500x300")
                        graph_win.title("Prediction")
                        df = pd.DataFrame({'day':id, 'sales':predict})
                        figure = plt.Figure(figsize=(6,5), dpi=100)
                        ax = figure.add_subplot(111)
                        chart_type = FigureCanvasTkAgg(figure, graph_win)
                        chart_type.get_tk_widget().pack()
                        df = df[['day','sales']]
                        df.plot(kind='line', legend=True, ax=ax)
                        print("sales")
                        print(df)
                        ax.set_title('Sales prediction')

            def my_p(mail):
                #farmer_win.destroy()
                #print(mail)
                my_p_win=Toplevel(farmer_win)
                my_p_win.title("Farmer - My Products")
                my_p_win.geometry("500x300")
                c.execute("select uid from users where mail_id='"+mail+"'")
                r=c.fetchall()
                for i in r:
                    id=i
                    break
                id=int(id[0])
                c.execute("SELECT pid,p_name,min_quan,max_quan FROM products where user_id="+str(id))
                #c.execute("SELECT pid,p_name,min_quan,max_quan FROM products")
                rc=c.rowcount
                if(rc==0):
                    Mb.showerror("Product list","There are no products.")
                else:
                    i=0
                    for products in c: 
                        for j in range(len(products)):
                            e = Entry(my_p_win, width=10, fg='blue') 
                            e.grid(row=i, column=j) 
                            e.insert(END, products[j])
                        e = Button(my_p_win, text ="Predict sales", command = lambda p = products[0] : predict(p,my_p_win))
                        e.grid(row=i,column=j+1)
                        i=i+1  
                
                

                

            #check.destroy()
            farmer_win=Toplevel(check)
            farmer_win.title("Farmer Page")
            farmer_win.geometry("500x300")
            
            b1=Button(farmer_win,text="ADD PRODUCT",width=20,command=lambda:add_p(mid))
            b1.grid(row=1,column=1)
            b2=Button(farmer_win,text="REMOVE PRODUCT",width=20,command=lambda:rem_p(mid))
            b2.grid(row=2,column=1)
            b3=Button(farmer_win,text="MY PRODUCT",width=20,command=lambda:my_p(mid))
            b3.grid(row=3,column=1)

        def consumer():

            def buy_p():
                from datetime import datetime 
                todays_date = datetime.now()
                date = todays_date.date()
                p1=e1.get()
                q=e2.get()
                #print("Value p1: ",p1)
                #print(p1)
                try:
                    
                    c.execute("select price from products where pid="+p1)
                    results = c.fetchall()
                    #print(results)
                    for i in results:
                        pr=i
                        #print(i)
                        break
                    #print(type(pr))
                    pr=float(pr[0])
                    maxq=[]
                    try:
                        c.execute("select min_quan from products where pid="+p1)
                        n=c.fetchall()
                        for i in n:
                            minq=i
                            break
                        c.execute("select max_quan from products where pid="+p1)
                        n1=c.fetchall()
                        for i in n1:
                            maxq=i
                            break


                        minq=int(minq[0])
                        #print(minq)
                        maxq=int(maxq[0])
                        #print(maxq)
                        q=int(q)
                        s=0
                        if(q<maxq):
                            if(q>=minq):
                                s=maxq-q
                                pr=pr*q
                        
                                try:
                                    c.execute("update products set max_quan="+str(s)+" where pid="+p1)
                                    Mb.showinfo("Update Status","Updated Successfully")
                                    c.execute("commit")
                                    try:
                                        #date="2020-11-24"
                                        c.execute("insert into sales values('"+str(date)+"','"+str(pr)+"','"+str(p1)+"')")
                                        Mb.showinfo("Insert Status","Added Sucessfully")
                                        c.execute("commit")
                                    except TypeError as e:
                                        print(e)
                                        Mb.showerror("Insert Status","Insertion Unsucessful")
                                except TypeError as e:
                                    print(e)
                                    Mb.showerror("Update status","Unsuccessful")
                            else:
                                Mb.showerror("Buying Status","Minimum Quantity not reached")
                    except TypeError as e:
                        print(e)
                        Mb.showerror("Getting data Status","Unsuccesful")

                except:
                    Mb.showerror("Product-Id Status","Product Unavailabe")

        
        
            
            def quicksort():
                def buy():
                    from datetime import datetime 
                    todays_date = datetime.now()
                    date = todays_date.date()
                    p1=e1.get()
                    q=e2.get()
                    #print("Value p1: ",p1)
                    c.execute("select price from products where pid="+p1)
                    results = c.fetchall()
                    #print("Answer:",results)
                    for i in results:
                        pr1=i
                        #print(i)
                        break
                    #print(type(pr1))
                    pr1=float(pr1[0])
                    maxq=[]
                    try:
                        c.execute("select min_quan from products where pid="+p1)
                        n=c.fetchall()
                        for i in n:
                            minq=i
                            break
                        c.execute("select max_quan from products where pid="+p1)
                        n1=c.fetchall()
                        for i in n1:
                            maxq=i
                            break


                        minq=int(minq[0])
                        #print(minq)
                        maxq=int(maxq[0])
                        #print(maxq)
                        q=int(q)
                        s=0
                        if(q<maxq):
                            if(q>=minq):
                                s=maxq-q
                                pr1=pr1*q
                        
                                try:
                                    c.execute("update products set max_quan="+str(s)+" where pid="+p1)
                                    Mb.showinfo("Update Status","Updated Successfully")
                                    c.execute("commit")
                                    try:
                                        #date="2020-11-14"
                                        c.execute("insert into sales values('"+str(date)+"','"+str(pr1)+"','"+str(p1)+"')")
                                        Mb.showinfo("Insert Status","Added Sucessfully")
                                        c.execute("commit")
                                    except TypeError as e:
                                        print(e)
                                        Mb.showerror("Insert Status","Insertion Unsucessful")
                                except TypeError as e:
                                    print(e)
                                    Mb.showerror("Update status","Unsuccessful")
                            else:
                                Mb.showerror("Buying Status","Minimum Quantity not reached")
                    except TypeError as e:
                        print(e)
                        Mb.showerror("Getting data Status","Unsuccesful")
                quick_win=Toplevel(consumer_win)
                quick_win.title("Products - Sorted By -Price")
                quick_win.geometry("500x300")

                
                c.execute("SELECT pid,p_name,min_quan,max_quan,price from products order by price")
                i=0
                for products in c: 
                    for j in range(len(products)):
                        e = Entry(quick_win, width=10, fg='blue') 
                        e.grid(row=i, column=j) 
                        e.insert(END, products[j])
                    i=i+1
                rc=c.rowcount

                l1=Label(quick_win,text="Product Id",font="times 15")
                l1.grid(row=rc+1,column=1)
                pid=IntVar()
                e1=Entry(quick_win,textvariable=pid)
                e1.grid(row=rc+1,column=2)
                l2=Label(quick_win,text="Quantity",font="times 15")
                l2.grid(row=rc+2,column=1)
                kg=IntVar()
                e2=Entry(quick_win,textvariable=kg)
                e2.grid(row=rc+2,column=2)
                b1=Button(quick_win,text="BUY PRODUCT",width=20,command=buy)
                b1.grid(row=rc+3,column=2)
            
                
                
                
                

            #check.destroy()
            consumer_win=Toplevel(check)
            consumer_win.title("Consumer Page")
            consumer_win.geometry("600x300")


            c.execute("SELECT pid,p_name,min_quan,max_quan,price from products")
            i=0
            for products in c: 
                for j in range(len(products)):
                    e = Entry(consumer_win, width=10, fg='blue') 
                    e.grid(row=i, column=j) 
                    e.insert(END, products[j])
                i=i+1
            rc=c.rowcount

            l1=Label(consumer_win,text="Product Id",font="times 15")
            l1.grid(row=rc+1,column=1)
            pid=IntVar()
            e1=Entry(consumer_win,textvariable=pid)
            e1.grid(row=rc+1,column=2)
            l2=Label(consumer_win,text="Quantity",font="times 15")
            l2.grid(row=rc+2,column=1)
            kg=IntVar()
            e2=Entry(consumer_win,textvariable=kg)
            e2.grid(row=rc+2,column=2)
            
            b1=Button(consumer_win,text="BUY PRODUCT",width=20,command=buy_p)
            b1.grid(row=rc+3,column=2)
            
            b2=Button(consumer_win,text="SORT-BY PRICE",width=20,command=quicksort)
            b2.grid(row=0,column=5)
            



        root.destroy()
        check=Tk()
        check.title("Register")
        check.geometry("500x300")

        l1=Label(check,text="Choose Who you are?",font="times 15")
        l1.grid(row=1,column=1)

        b1=Button(check,text="FARMER",width=20,command=farmer)
        b1.grid(row=2,column=1)
        b2=Button(check,text="CONSUMER",width=20,command=consumer)
        b2.grid(row=2,column=2)
    def failed():
        l1=Label(root,text="Account Doesn't Exists.... Signup",font="times 15")
        l1.grid(row=4,column=3)
        b2=Button(root,text="SignUp",width=20,command=Signup)
        b2.grid(row=5,column=3)


    mid=e1.get()
    password=e2.get()


    if(mid=="" or password==""):
        Mb.showinfo("Login Status","All fields are required")
    else:
        sql = "select mail_id,pass from users where mail_id = %s and pass = %s"
        c.execute(sql,[(mid),(password)])
        e1.delete(0,'end')
        e2.delete(0,'end')
        results = c.fetchall()
        if results:
            for i in results:
                logged()
                break
        else:
            failed()


def Signup():

    def signup_db():
        uid=e1.get()
        name=e2.get()
        un=e3.get()
        mid=e4.get()
        pa=e5.get()

        if(uid=="" or name=="" or un=="" or mid =="" or pa ==""):
            Mb.showinfo("Insert Status","All fields are required")
        else:
            c.execute("select uid from users")
            for i in c:
                if i==(uid,):
                    Mb.showerror("Create Error","User-Id already present")
            else:
                c.execute("insert into users values('"+uid+"','"+name +"','"+un+"','"+mid+"','"+pa+"')")
                Mb.showinfo("Insert Status","Created Succussfully")
                c.execute("commit")
                

                e1.delete(0,'end')
                e2.delete(0,'end')
                e3.delete(0,'end')
                e4.delete(0,'end')
                e5.delete(0,'end')
        
        l6=Label(signup_win,text="Account Created",font="times 10")
        l6.grid(row=7,column=3)
        
        
        


    #root.destroy()
    signup_win=Toplevel(root)
    signup_win.title("Sign up Page")
    signup_win.geometry("500x300")
    #signup_win.configure(bg='blue')
    l1=Label(signup_win,text="User-Id",font="times 15",width=10)
    l1.grid(row=1,column=1)
    l2=Label(signup_win,text="User-Name",font="times 15",width=10)
    l2.grid(row=2,column=1)
    l3=Label(signup_win,text="Phone Number",font="times 15",width=10)
    l3.grid(row=3,column=1)
    l4=Label(signup_win,text="Mail-Id",font="times 15",width=10)
    l4.grid(row=4,column=1)
    l5=Label(signup_win,text="Password",font="times 15",width=10)
    l5.grid(row=5,column=1)
    
    
    
    id=IntVar()
    e1=Entry(signup_win,textvariable=id)
    e1.grid(row=1,column=2)
    name=StringVar()
    e2=Entry(signup_win,textvariable=name)
    e2.grid(row=2,column=2)
    phno=IntVar()
    e3=Entry(signup_win,textvariable=phno)
    e3.grid(row=3,column=2)
    mailid=StringVar()
    e4=Entry(signup_win,textvariable=mailid)
    e4.grid(row=4,column=2)
    pas=StringVar()
    e5=Entry(signup_win,textvariable=pas)
    e5.grid(row=5,column=2)
    
    

    b1=Button(signup_win,text="Sign up",width=20,command=signup_db)
    b1.grid(row=6,column=2)

    
    signup_win.mainloop()





        

root=Tk()
root.title("Farmer And COnsumer")
root.geometry("500x300")
#root.configure(bg='blue')
l1=Label(root,text="Mail-Id",font="times 15",width=10)
l1.grid(row=1,column=1)
l2=Label(root,text="Password",font="times 15",width=10)
l2.grid(row=2,column=1)

mailid=StringVar()
e1=Entry(root,textvariable=mailid)
e1.grid(row=1,column=2)
pas=StringVar()
e2=Entry(root,textvariable=pas)
e2.grid(row=2,column=2)

                

b1=Button(root,text="Login",width=20,command=login_db)
b1.grid(row=3,column=2)

b2=Button(root,text="Sign up",width=20,command=Signup)
b1.grid(row=3,column=3)

root.mainloop()

