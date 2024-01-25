from ampalibe import Model, Messenger
from models.notemodel import NoteModel
from models.noteinstancemodel import NoteInstanceModel
from faker import Faker
from faker.providers import internet
import utils


note_model = NoteModel(utils.get_env_value("NOTE_COLLECTION"))
note_instance_model = NoteInstanceModel(utils.get_env_value("NOTE_INSTANCE_COLLECTION"))
chat = Messenger()
query = Model()
fake = Faker()
fake.add_provider(internet)
data_search_center = utils.load_search_data(note_model)
chat.get_started()

is_logged = False

var_records = []