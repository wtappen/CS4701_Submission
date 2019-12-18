import data_loader
import kernalized_svm
import numpy as np
from utils import log
from utils import log_csv
from pathlib import Path

# C = 1000000
# kernel_type = 'linear'


def make_model_name(name, label, c):
    return Path(str(name) + '_' + str(label) + '_' + str(c) + '.txt')


def make_numeric_labels(y, correct_label):
    """
    a list of 1's and -1's where each element of y is a 1 if it is the correct
    label, othewise it is a -1
    """
    numeric_labels = []
    for l in y:
        if l == correct_label:
            numeric_labels.append(1)
        else:
            numeric_labels.append(-1)
    return numeric_labels


def calc_acc(actual_labels, preds):
    """
    returns the decimal percentage of correct predictions
    """
    count = 0
    false_neg = 0
    false_pos = 0
    true_neg = 0
    true_pos = 0
    num_examples = len(actual_labels)
    for j in range(num_examples):
        if actual_labels[j] == preds[j]:
            count += 1
            if actual_labels[j] < 0:
                true_neg += 1
            else:
                true_pos += 1
        elif preds[j] < 0:
            false_neg += 1
        else:
            false_pos += 1
    acc = count / num_examples
    if true_pos + false_pos == 0:
        precision = 'NaN'
    else:
        precision = true_pos / (true_pos + false_pos)  # cost of false pos is high
    if true_pos + false_neg == 0:
        recall = 'NaN'
    else:
        recall = true_pos / (true_pos + false_neg)  # cost of false neg is high
    if precision == 'NaN' or recall == 'NaN':
        f1 = 'NaN'
    else:
        f1 = 2 * (precision * recall) / (precision + recall)
    # return count / num_examples, false_neg, false_pos, true_neg, true_pos
    return acc, precision, recall, f1


def train_and_validate_all(k_param):
    """
    trains an SVM for each face from the data from data_loader and returns
    a dictionary of these models. Also performs k-fold cross valdiation on each
    model.
    """
    xTr_partition, yTr_partition, xV_partition, yV_partition, label_set, xAll, yAll = data_loader.load_vectors(k_param)
    models = {}

    for correct_label in label_set:
        log('Training for: ' + correct_label)
        num_partitions = len(xTr_partition)
        cumulative_acc = 0

        for i in range(num_partitions):
            xTr = xTr_partition[i]
            yTr = yTr_partition[i]
            xV = xV_partition[i]
            yV = yV_partition[i]

            tr_numeric_labels = make_numeric_labels(yTr, correct_label)
            v_numeric_labels = make_numeric_labels(yV, correct_label)

            svm_classifier = kernalized_svm.create_svm(xTr, np.array(tr_numeric_labels), C, kernel_type)
            pred = svm_classifier(np.array(xV))

            partition_acc, _, _ = calc_acc(v_numeric_labels, pred)
            log('Accuracy for partition ' + str(i) + ': ' + str(partition_acc))
            cumulative_acc += partition_acc

        overall_acc = cumulative_acc / num_partitions
        log('Overall cross-validation accuracy: ' + str(overall_acc))

        tr_all_numeric_labels = make_numeric_labels(yAll, correct_label)

        final_svm_classifier = kernalized_svm.create_svm(xAll, np.array(tr_all_numeric_labels), C, kernel_type)
        models[correct_label] = final_svm_classifier

        final_preds = final_svm_classifier(xAll)

        training_acc, _, _, _ = calc_acc(tr_all_numeric_labels, final_preds)
        log("Final training accuracy: " + str(training_acc))
        log('')

    return models


def train_model_all(path_name, C, kernel_type, model_path):
    """
    Trains models for everyone in directory
    """

    xTr, yTr, label_set = data_loader.load_vectors(path_name, 'tr_data.txt')
    models = {}

    log('C: ' + str(C))
    log('kernel type: ' + kernel_type + '\n')

    for correct_label in label_set:
        log('Training for: ' + correct_label)
        tr_numeric_labels = make_numeric_labels(yTr, correct_label)
        svm_classifier = kernalized_svm.create_svm(xTr, np.array(tr_numeric_labels), C, kernel_type, make_model_name(model_path, correct_label, C))
        models[correct_label] = svm_classifier
        preds = svm_classifier(xTr)
        training_acc, precision, recall, f1 = calc_acc(tr_numeric_labels, preds)
        log("Training accuracy: " + str(training_acc))
        log('Precision: ' + str(precision))
        log('Recall: ' + str(recall))
        log('F1 score: ' + str(f1))
        log('')
        stats_list = [model_path, correct_label, C, kernel_type, training_acc, precision, recall, f1]
        log_csv(stats_list)

    return models


def train_model(pos_path_name, neg_path_name, C, kernel_type, model_path):

    xTr_pos, yTr_pos, pos_label = data_loader.load_vectors_of_class(pos_path_name, 'tr_data.txt', 1)
    xTr_neg, yTr_neg, neg_label = data_loader.load_vectors_of_class(neg_path_name, 'tr_data.txt', -1)
    xTr = np.concatenate((xTr_pos, xTr_neg))
    yTr = np.concatenate((yTr_pos, yTr_neg))

    log('C: ' + str(C))
    log('kernel type: ' + kernel_type + '\n')

    log('Training for: ' + pos_label)
    # tr_numeric_labels = make_numeric_labels(yTr, correct_label)
    svm_classifier = kernalized_svm.create_svm(xTr, yTr, C, kernel_type, make_model_name(model_path, pos_label, C))
    preds = svm_classifier(xTr)
    training_acc, precision, recall, f1 = calc_acc(yTr, preds)
    log("Training accuracy: " + str(training_acc))
    log('Precision: ' + str(precision))
    log('Recall: ' + str(recall))
    log('F1 score: ' + str(f1))
    log('')
    stats_list = [model_path, pos_label, C, kernel_type, training_acc, precision, recall, f1]
    log_csv(stats_list)

    return svm_classifier


def test_model_all(models, path_name, text_file, test_or_validation, model_path, C, kernel_type):
    xTest, yTest, label_set = data_loader.load_vectors(path_name, text_file)
    for correct_label in label_set:
        if correct_label in models:
            test_numeric_labels = make_numeric_labels(yTest, correct_label)
            test_pred = models[correct_label](np.array(xTest))
            # test_acc, false_neg, false_pos, true_neg, true_pos = calc_acc(test_numeric_labels, test_pred)
            # log(test_or_validation + ' accuracy for ' + correct_label + ': ' + str(test_acc))
            # log('False negatives for ' + correct_label + ': ' + str(false_neg))
            # log('False positives for ' + correct_label + ': ' + str(false_pos))
            # log('True negatives for ' + correct_label + ': ' + str(true_neg))
            # log('True positives for ' + correct_label + ': ' + str(true_pos))
            # log('')
            acc, precision, recall, f1 = calc_acc(test_numeric_labels, test_pred)
            log(test_or_validation + ' accuracy for ' + correct_label + ': ' + str(acc))
            log('Precision for ' + correct_label + ': ' + str(precision))
            log('Recall for ' + correct_label + ': ' + str(recall))
            log('F1 score for ' + correct_label + ': ' + str(f1))
            log('')
            stats_list = [model_path, path_name, correct_label, C, kernel_type, acc, precision, recall, f1]
            log_csv(stats_list)


def test_model(model, pos_path_name, neg_path_name, text_file, test_or_validation):
    xTest_pos, yTest_pos, pos_label = data_loader.load_vectors_of_class(pos_path_name, text_file, 1)
    xTest_neg, yTest_neg, neg_label = data_loader.load_vectors_of_class(neg_path_name, text_file, -1)
    xTest = np.concatenate((xTest_pos, xTest_neg))
    yTest = np.concatenate((yTest_pos, yTest_neg))

    test_pred = model(np.array(xTest))

    acc, precision, recall, f1 = calc_acc(yTest, test_pred)
    log(test_or_validation + ' accuracy for ' + pos_label + ': ' + str(acc))
    log('Precision for ' + pos_label + ': ' + str(precision))
    log('Recall for ' + pos_label + ': ' + str(recall))
    log('F1 score for ' + pos_label + ': ' + str(f1))
    log('')