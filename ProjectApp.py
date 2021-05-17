# Imports
from app import app, db
from app.models import Users, Lesson, Question

# Generates db for testing
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Users': Users, 'Lesson': Lesson, 'Test': Test, 'Question':Question}

if __name__=='__main__':
     app.run(debug=True)