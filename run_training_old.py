import data_loader
import train_identifier
from utils import log
import utils
from pathlib import Path


root = Path('.')
training_dir = root / 'training_data'
val_dir = root / 'validation_data'
test_dir = root / 'test_data'
fs_tr_dir = training_dir / 'expressive_all_tr' / 'faceScrub_train'
fs_val_dir = val_dir / 'expressive_all_val' / 'faceScrub_val'


utils.set_logger('log')

log(utils.separator())

# # data_loader.convert_data_to_vectors(root_path_str='./Data7', text_file_str='tr_data.txt')
# # data_loader.convert_data_to_vectors(root_path_str='./Validation', text_file_str='val_data.txt')
# # data_loader.convert_data_to_vectors(root_path_str='./Test', text_file_str='test_data.txt')


# m = train_identifier.train_model(training_dir / 'expressive_all_tr' / 'Brynn_Szczesniak', fs_tr_dir, .1, 'linear')
# model_dict = {'Brynn_Szczesniak': m}

# # c = .01
# # for i in range (1, 8):
# #     c *= 10
# #     m = train_identifier.train_model('./Data6', c, 'linear')
# #     train_identifier.test_model(m, "./Validation", "val_data.txt", 'Validation')

# # m = train_identifier.train_model('./Data7', 1000000, 'linear')
# # train_identifier.test_model(model_dict, "./Will_val", "val_data.txt", 'Validation')
# train_identifier.test_model_all(model_dict, val_dir / 'expressive_all_val',  "val_data.txt", 'Validation')
# train_identifier.test_model(m, val_dir / 'expressive_all_val' / 'Brynn_Szczesniak', fs_val_dir, 'val_data.txt', 'Validation')

data_loader.convert_data_to_vectors(root_path_str='./training_data/expressive_all_tr', text_file_str='tr_data.txt')
data_loader.convert_data_to_vectors(root_path_str='./validation_data/expressive_all_val', text_file_str='val_data.txt')
data_loader.convert_data_to_vectors(root_path_str='./test_data/expressive_all_test', text_file_str='test_data.txt')



log(utils.separator())
