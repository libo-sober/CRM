import hashlib


def set_md5(values):
    """
    加密函数
    :param values:需要被加密的字符串数据
    :return:加密后的数据
    """
    secret_key = 'username'.encode('utf-8')
    md5_value = hashlib.md5(secret_key)
    md5_value.update(values.encode('utf-8'))
    return md5_value.hexdigest()


