class Message(object):
    
    def __init__(self, sender, message, date, images=[], reactions=[]):
        self.sender = sender
        self.message = message
        self.date = date
        self.images = images
        self.reactions = reactions
    
    def __str__(self):
        return '<Message sender="{}", message="{}", date="{}">'.format(self.sender, self.message, self.date)
    
    def __repr__(self):
        return str(self)
    