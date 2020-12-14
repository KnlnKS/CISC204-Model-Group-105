def least_two_of_three(x, y, z):
    return (x & (y | z)) | (y & z)


def least_two_of_four(w, x, y, z):
    return least_two_of_three(w, x, y) | least_two_of_three(x, y, z) | least_two_of_three(y, z, w)


def least_two_of_five(v, w, x, y, z):
    return least_two_of_four(v, w, x, y) | least_two_of_four(w, x, y, z) | least_two_of_four(z, v, w, x)


def least_two_of_six(u, v, w, x, y, z):
    return least_two_of_five(u, v, w, x, y) | least_two_of_five(v, w, x, y, z) | least_two_of_five(z, u, v, w, x)


def least_four_of_six(u, v, w, x, y, z):
    l2o3 = least_two_of_three
    return (l2o3(u, v, w) & l2o3(x, y, z)) | (l2o3(z, u, v) & l2o3(w, x, y)) | (l2o3(y, z, u) & l2o3(v, w, x)) | (
                l2o3(u, y, w) & l2o3(x, v, z)) | (l2o3(u, z, w) & l2o3(x, v, y)) | (l2o3(u, x, y) & l2o3(v, w, z))
