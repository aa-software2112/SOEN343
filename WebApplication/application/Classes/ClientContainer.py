class Client(object):
    #Setting the client object attributes
    def __init__(self, row):
        self.id = row[0]
        self.firstName = row[1]
        self.lastName = row[2]
        self.physicalAddress = row[3]
        self.email = row[4]
        self.phoneNumber = row[5]
        self.username = row[6]
        self.password = row[7]
        self.isAdmin = row[8]
        self.isLogged = row[9]
        self.lastLogged = row[10]

    #this method defines how the object will be printed in the terminal for debugging purposes
    def __repr__(self):
        return 'id: {}, firstName: {}, lastName: {}, physicalAddress: {}, email: {}, phoneNumber: {}, username: {}' \
               ', password: {}, isAdmin: {}, isLogged: {}, lastLogged: {}'\
            .format(self.id, self.firstName, self.lastName, self.physicalAddress, self.email, self.phoneNumber, self.username
                    , self.password, self.isAdmin, self.isLogged, self.lastLogged)
