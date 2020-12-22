import datetime
last_id = 0


class Note:
    def __init__(self, memo, tags=''):
        self.memo = memo
        self.tags = tags
        self.creation_date = datetime.date.today()
        global last_id
        last_id += 1
        self.id = last_id

    def match(self, filter):
        return filter in self.memo or filter in self.tags


class Notebook:
    def __init__(self):
        self.notes = dict()

    def new_note(self, memo, tags=''):
        self.notes[last_id] = Note(memo, tags)

    def _find_note(self, note_id):
        note = self.notes.get(note_id)
        if note:
            return note
        return None

    def modify_attribute(self, note_id, attribute, value):
        note = self._find_note(note_id)
        if note:
            note.__setattr__(attribute, value)
            return True
        return False

    def modify_memo(self, note_id, memo):
        return self.modify_attribute(note_id, 'memo', memo)

    def modify_tags(self, note_id, tags):
        return self.modify_attribute(note_id, 'tags', tags)

    def search(self, filter):
        return {id:note for id, note in self.notes.items() if note.match(filter)}
