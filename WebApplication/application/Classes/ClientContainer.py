class Client(object):
    #Setting the client object attributes
    def __init__(self, id,firstName, lastName, physicalAddress, email
                 , phoneNumber, username, password, isAdmin, isLogged, lastLogged):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.physicalAddress = physicalAddress
        self.email = email
        self.phoneNumber = phoneNumber
        self.username = username
        self.password = password
        self.isAdmin = isAdmin
        self.isLogged = isLogged
        self.lastLogged = lastLogged

    #this method defines how the object will be printed in the terminal for debugging purposes
    def __repr__(self):
        return 'id: {}, firstName: {}, lastName: {}, physicalAddress: {}, email: {}, phoneNumber: {}, username: {}' \
               ', password: {}, isAdmin: {}, isLogged: {}, lastLogged: {}'\
            .format(self.id, self.firstName, self.lastName, self.physicalAddress, self.email, self.phoneNumber, self.username
                    , self.password, self.isAdmin, self.isLogged, self.lastLogged)
