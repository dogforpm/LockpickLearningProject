# imports
import os

# Sets directory of project file
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    # Generate enviromental secret key as well as default secret key should 
    # an enviromental one not generate
    SECRET_KEY = os.environ.get('SECRET_KEY') or '1QaZsE4RfVgY7UjMkO0P'
    # Initialise database to be used in project
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'LPLearning.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False