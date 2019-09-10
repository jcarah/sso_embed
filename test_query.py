from flask import Flask

from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *
engine = create_engine('sqlite:///sso.db', echo=True)

Session = sessionmaker(bind=engine)
s = Session()
query = s.query(User).filter(User.username.in_(['admin']), User.password.in_(['password']) )
result = query.first().permissions


print str(result).split(',')
