from regressions.regression import Regression
from students_reader import load_students_json, save_students_json, load_students_csv, save_students_csv
from regressions.log_regression import non_lin_reg_test, non_lin_keras_test, lin_reg_test, lin_keras_test


def students_reader_json_test():
    students = load_students_json('../resources/reader/students.json')
    save_students_json('../resources/reader/saved/students_saved.json', students)
    students = load_students_json('../resources/reader/saved/students_saved.json')
    [print(s)for s in students]


def students_reader_csv_test():
    students = load_students_csv('../resources/reader/students.csv')
    save_students_csv('../resources/reader/saved/students_saved.csv', students)
    students = load_students_csv('../resources/reader/saved/students_saved.csv')
    [print(s)for s in students]


def regression_test():
    Regression.distance_field_example()
    Regression.linear_reg_example()
    Regression.bi_linear_reg_example()
    Regression.n_linear_reg_example()
    Regression.poly_reg_example()
    Regression.quadratic_reg_example()


def log_regression_test():
    lin_reg_test()
    lin_keras_test()
    non_lin_reg_test()
    non_lin_keras_test()





if __name__ == '__main__':
    log_regression_test()






