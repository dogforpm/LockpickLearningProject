# Imports
from app import app, db
from app.models import Users

# Generates part of db for testing
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Users': Users}

if __name__=='__main__':
     app.run(debug=True)