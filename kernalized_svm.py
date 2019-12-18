import numpy as np
import cvxpy as cp

DEFAULT_K_PARAM = .05


def write_array(a):
    s = ""
    for e in a:
        s += str(e) + ','
    s = s[:-1]
    return s


def write_array_of_arrays(aa):
    s = ''
    for a in aa:
        s += write_array(a) + ';'
    return s[:-1]


def compute_kernel(k_type, X, Z, k_param=DEFAULT_K_PARAM):
    """
    k_type: the type of kernel to compute
    X: n input vectors of dim d
    Z: m input vectors of dim d
    k_param: a param for some kernels

    returns a nxm matrix where the i,jth element is
    the kernel of the ith element of X and jth element of Z
    """
    if k_type == "linear":
        return np.matmul(X, np.transpose(Z))

    return None


def dual_svm(K, yTr, C):
    """
    k: the nxn kernel matrix
    yTr: the training labels
    C: SVM param

    alpha: the alpha vector of the SVM dual optimization
    """
    y = yTr.flatten()
    N, _ = K.shape

    alpha = cp.Variable(N, nonneg=True)

    yTrParam = cp.Parameter(y.shape[0])
    yTrParam.value = y

    KParam = cp.Parameter(K.shape, PSD=True)
    KParam.value = K

    Cs = cp.Parameter(N)
    Cs.value = np.full(N, C)

    z = cp.Parameter(N)
    z.value = np.zeros(N)

    const = [cp.sum(cp.multiply(alpha, yTrParam)) == 0, alpha >= z,  alpha <= C]

    ya = cp.multiply(yTrParam, alpha)
    sum1 = sum(alpha)
    sum2 = sum(cp.quad_form(ya, K))
    goal = cp.Maximize(sum1 - (.5 * sum2))
    prob = cp.Problem(goal, const)
    prob.solve()

    return np.array(alpha.value).flatten()


def recover_bias(K, yTr, alpha, C):
    """
    function bias=recoverBias(K,yTr,alpha,C);
    Solves for the hyperplane bias term, which is uniquely specified by the
    support vectors with alpha values 0<alpha<C

    INPUT:
    K : nxn kernel matrix
    yTr : nx1 input labels
    alpha  : nx1 vector of alpha values
    C : regularization constant

    Output:
    bias : the scalar hyperplane bias of the kernel SVM specified by alphas
    """

    min_dist_middle = C+1
    corresponding_i = 0

    for i in range(len(alpha)):
        if abs((C/2) - alpha[i]) < min_dist_middle:
            min_dist_middle = abs(C/2-alpha[i])
            corresponding_i = i

    summation = 0
    for i in range(len(alpha)):
        summation += alpha[i] * yTr[i] * K[corresponding_i][i]

    bias = 1/yTr[corresponding_i]-summation
    return bias


def create_svm(xTr, yTr, C, k_type, path, k_param=DEFAULT_K_PARAM):
    K = compute_kernel(k_type, xTr, xTr, k_param)
    a = dual_svm(K, yTr, C)
    b = recover_bias(K, yTr, a, C)

    file = open(path, 'w+')
    file.write(write_array(a) + '\n')
    file.write(write_array_of_arrays(xTr) + '\n')
    file.write(write_array(yTr) + '\n')
    file.write(str(b) + '\n')
    file.write(str(k_type) + '\n')
    file.write(str(k_param) + '\n')
    file.close()

    def classify(xTe):
        results = []
        kTe = compute_kernel(k_type, xTe, xTr, k_param)
        for i in range(len(xTe)):
            ay = a[:]*yTr[:]
            ks = kTe[i][:]
            form = sum(np.multiply(ay, ks)) + b
            results.append(1 if form > 0 else -1)
        return np.array(results)

    return classify


# def calc_params(path, xTr, yTr, C, k_type, k_param=DEFAULT_K_PARAM):
#     K = compute_kernel(k_type, xTr, xTr, k_param)
#     a = dual_svm(K, yTr, C)
#     b = recover_bias(K, yTr, a, C)

#     file = open(path, 'w+')
#     file.write(write_array(a) + '\n')
#     file.write(str(b) + '\n')
#     file.write(str(k_type) + '\n')
#     file.write(str(k_param) + '\n')
#     file.close()


def load_svm(path_params):
    params_txt = open(str(path_params), "r+")
    line = params_txt.readline().replace('\n', '')
    # a = np.fromstring(line, dtype=float, sep=' ')
    a = np.fromstring(line, dtype=float, sep=',')
    line = params_txt.readline().replace('\n', '')
    x = []
    pos_lines = line.split(';')
    for v in pos_lines:
        x.append(np.fromstring(v, dtype=float, sep=','))
    xTr = np.array(x)
    line = params_txt.readline().replace('\n', '')
    yTr = np.fromstring(line, dtype=float, sep=',')
    line = params_txt.readline().replace('\n', '')
    b = float(line)
    line = params_txt.readline().replace('\n', '')
    k_type = line
    line = params_txt.readline().replace('\n', '')
    k_param = float(line)
    params_txt.close()

    # x = []
    # y = []
    # data_txt = open(str(path_data_pos), "r")
    # pos_lines = data_txt.readlines()
    # for line in pos_lines:
    #     x.append(np.fromstring(line, dtype=float, sep=','))
    #     y.append(1)
    # data_txt.close()

    # data_txt = open(str(path_data_neg), "r")
    # neg_lines = data_txt.readlines()
    # for line in neg_lines:
    #     x.append(np.fromstring(line, dtype=float, sep=','))
    #     y.append(-1)
    # data_txt.close()

    # xTr = np.array(x)
    # yTr = np.array(y)

    def classify(xTe):
        results = []
        kTe = compute_kernel(k_type, xTe, xTr, k_param)
        for i in range(len(xTe)):
            ay = a[:]*yTr[:]
            ks = kTe[i][:]
            form = sum(np.multiply(ay, ks)) + b
            results.append(1 if form > 0 else -1)
        return np.array(results)

    return classify
