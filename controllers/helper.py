import globalinstance


class NoteQuery:
    query = globalinstance.query

    def __init__(self, sender_id):
        self.sender_id = sender_id
        self.instance_attrs()
    
    def instance_attrs(self):
        self.query.set_temp(self.sender_id, 'is_finish', False)
        self.query.set_temp(self.sender_id, 'title', None)
        self.query.set_temp(self.sender_id, 'source_ref', None)
        self.query.set_temp(self.sender_id, 'records', [])

        # attrs declaration
        self.is_finish = self.query.get_temp(self.sender_id, 'is_finish')
        self.title = self.query.get_temp(self.sender_id, 'title')
        self.source_ref = self.query.get_temp(self.sender_id, 'source_ref')
        self.records = self.query.get_temp(self.sender_id, 'records')

    def get_attr(self, attr):
        self[attr] = self.query.get_temp(self.sender_id, attr)
        return self[attr]
    
    def update_attr(self, attr, value):
        self.query.set_temp(self.sender_id, attr, value)
        return self.get_attr(attr)
    
    def update_records(self, value) -> list:
        self.query.set_temp(self.sender_id, 'records', self.records.append(value))
        self.records = self.query.get_temp(self.sender_id, 'records')
        return self.records
    
    def ready_for_operation(self):
        try:
            assert self.is_finish == True
            assert self.title is not None
            assert self.source_ref is not None
            assert len(self.records) != 0
            return True
        except:
            return False
    
    def reset(self):
        self.instance_attrs()



