from app import db, lm

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(60), unique=False)
    lname = db.Column(db.String(60), unique=False)
    organization = db.Column(db.String(120), unique=False)
    email = db.Column(db.String(120), unique=False)
    password = db.Column(db.String(20), unique=False)

    #In general this method should just return True unless the object represents a user that should not be
    #allowed to authenticate for some reason.
    @property
    def is_authenticated(self):
        return True

    #The is_active property should return True for users unless they are inactive,
    #for example because they have been banned.
    @property
    def is_active(self):
        return True

    #should return True only for fake users that are not supposed to log in to the system.
    @property
    def is_anonymous(self):
        return False

    #should return a unique identifier for the user, in unicode format.
    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    #loads a user from the database.
    @lm.user_loader
    def load_user(id):
        return User.query.get(int(id))


    def __repr__(self):
        return '<Customer %r>' % self.id
