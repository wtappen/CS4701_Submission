import data_loader
import train_identifier
from utils import log
import utils
from pathlib import Path
import kernalized_svm

root = Path('.')
training_dir = root / 'training_data'
val_dir = root / 'validation_data'
test_dir = root / 'test_data'
model_dir = root / 'saved_models'
fs_tr_dir_small = training_dir / 'normal_all_tr' / 'faceScrub'
fs_val_dir_small = val_dir / 'normal_all_val' / 'faceScrub'

player_list = [
    'Brynn_Szczesniak',
    # 'Jay_Tappen',
    # 'Leigh_Tappen',
    'Megan_Backus',
    'Nhat',
    # 'Skip_Tappen',
    'Will_Tappen',
]

model_all_expressive = model_dir / 'model_all_expressive'
model_all_normal = model_dir / 'model_all_normal'
model_individual_expressive_small = model_dir / 'model_individual_expressive_small'
model_individual_normal_small = model_dir / 'model_individual_normal_small'
model_individual_expressive_large = model_dir / 'model_individual_expressive_large'
model_individual_normal_small = model_dir / 'model_individual_normal_small'

tr_expressive = training_dir / 'expressive_all_tr'
tr_normal = training_dir / 'normal_all_tr'
val_expressive = val_dir / 'expressive_all_val'
val_normal = val_dir / 'normal_all_val'
test_expressive = test_dir / 'expressive_all_test'
test_normal = test_dir / 'normal_all_test'

training_log = './results/training/tr_result'
val_log = './results/validation/val_result'
test_log = './results/testing/test_result'

k_type = 'linear'
c_min = .1
c_max = .1


def make_model_name(name, label, c):
    return Path(str(name) + '_' + str(label) + '_' + str(c) + '.txt')


def make_vecs():
    utils.set_logger('log')
    log(utils.separator())

    data_loader.convert_data_to_vectors(root_path_str='./training_data/expressive_all_tr', text_file_str='tr_data.txt')
    data_loader.convert_data_to_vectors(root_path_str='./training_data/normal_all_tr', text_file_str='tr_data.txt')
    data_loader.convert_data_to_vectors(root_path_str='./faceScrub_big_train', text_file_str='tr_data.txt')
    data_loader.convert_data_to_vectors(root_path_str='./validation_data/expressive_all_val', text_file_str='val_data.txt')
    data_loader.convert_data_to_vectors(root_path_str='./validation_data/normal_all_val', text_file_str='val_data.txt')
    data_loader.convert_data_to_vectors(root_path_str='./test_data/expressive_all_test', text_file_str='test_data.txt')
    data_loader.convert_data_to_vectors(root_path_str='./test_data/normal_all_test', text_file_str='test_data.txt')
    log(utils.separator())


def train_all(training_dir, model_path):
    C = c_min
    while C <= c_max:
        train_identifier.train_model_all(tr_expressive, C, k_type, model_path)
        C *= 10


def train_individual(training_base_dir, model_path):
    C = c_min
    while C <= c_max:
        for p in player_list:
            train_identifier.train_model(tr_expressive / p, fs_tr_dir_small, C, k_type, model_path)
        C *= 10
        # train_identifier.test_model_all(model_dict, val_dir / 'expressive_all_val', 'val_data.txt', 'Validation')


def validate_on_all(val_dir, model_path):
    # model path is model_all_expressive for instance
    C = c_min
    while C <= c_max:
        model_dict = {}
        for p in player_list:
            m = kernalized_svm.load_svm(make_model_name(model_path, p, C))
            model_dict[p] = m
        train_identifier.test_model_all(model_dict, val_dir, 'test_data.txt', 'Test', model_path, C, k_type)
        C *= 10



# train_identifier.test_model(m, val_dir / 'expressive_all_val' / p, fs_val_dir_small, 'val_data.txt', 'Validation')


# utils.set_path_logger('./results/testing')
# m_orig = train_identifier.train_model(training_dir / 'expressive_all_tr' / 'Nhat', fs_tr_dir_small, .1, 'linear', model_dir / 'TESTING')

# m_loaded = kernalized_svm.load_svm(model_dir / 'TESTINGNhat0.1.txt', training_dir / 'expressive_all_tr' / 'Nhat' / 'tr_data.txt', fs_tr_dir_small / 'tr_data.txt')
# train_identifier.test_model(m_loaded, val_dir / 'expressive_all_val' / 'Nhat', fs_val_dir_small, 'val_data.txt', 'Validation')

# utils.set_path_logger(training_log)
# train_all(tr_expressive, model_all_expressive)
# train_individual(tr_expressive, model_individual_expressive_small)
# train_all(tr_normal, model_all_normal)
# train_individual(tr_normal, model_individual_normal_small)

# utils.set_path_logger(val_log)
# validate_on_all(val_expressive, model_all_expressive)
# validate_on_all(val_normal, model_all_expressive)

# validate_on_all(val_expressive, model_individual_expressive_small)
# validate_on_all(val_normal, model_individual_expressive_small)

# validate_on_all(val_expressive, model_all_normal)
# validate_on_all(val_normal, model_all_normal)

# validate_on_all(val_expressive, model_individual_normal_small)
# validate_on_all(val_normal, model_individual_normal_small)


utils.set_path_logger(test_log)
validate_on_all(test_expressive, model_all_expressive)
validate_on_all(test_expressive, model_all_expressive)