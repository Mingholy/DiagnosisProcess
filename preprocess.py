# -*- coding: utf-8 -*-
"""
医案处理脚本
@liminghao
2017-03-03
"""
import re

keyword = ['病者', '病名', '原因',
           '证候', '诊断', '疗法',
           '处方', '复诊', '次方',
           '又方', '三诊', '三方',
           '四诊', '四方', '五诊',
           '五方', '六诊', '六方',
           '七诊', '七方', '八诊',
           '八方', '九诊', '十诊',
           '十一诊', '十二诊', '十三诊',
           '九方', '十方', '十一方',
           '十二方', '十三方', '说明',
           '效果', '廉按', '医者']


class MedicalCase:
    """
    医案类
    """

    def __init__(self):
        self._case_name = ''
        self._case_type = {'病案科属': '未标明科属'}
        self._case_doctor = '未记载医者'
        self._patient = ''
        self._sickness = ''
        self._etiology = ''
        self._syndromes = ''
        self._diagnosis = []
        self._therapy = '无'
        self._prescription = []
        self._efficacy = '无'
        self._explaination = {'说明': '无'}
        self._comment = '无'

    # 医案名称
    @property
    def case_name(self):
        return self._case_name

    @case_name.setter
    def case_name(self, line):
        self._case_name = line

    # 医案科属
    @property
    def case_type(self):
        return self._case_type

    @case_type.setter
    def case_type(self, line):
        self._case_type = line

    # 医者
    @property
    def case_doctor(self):
        return self._case_doctor

    @case_doctor.setter
    def case_doctor(self, line):
        self._case_doctor = line

    # 病者
    @property
    def patient(self):
        return self._patient

    @patient.setter
    def patient(self, patient_info):
        self._patient = patient_info

    # 病名
    @property
    def sickness(self):
        return self._sickness

    @sickness.setter
    def sickness(self, line):
        self._sickness = line

    # 原因
    @property
    def etiology(self):
        return self._etiology

    @etiology.setter
    def etiology(self, line):
        self._etiology = line

    # 证候
    @property
    def syndromes(self):
        return self._syndromes

    @syndromes.setter
    def syndromes(self, line):
        self._syndromes = line

    # 诊断
    @property
    def diagnosis(self):
        return self._diagnosis

    @diagnosis.setter
    def diagnosis(self, line):
        self._diagnosis = line

    # 疗法
    @property
    def therapy(self):
        return self._therapy

    @therapy.setter
    def therapy(self, line):
        self._therapy = line

    # 处方
    @property
    def prescription(self):
        return self._prescription

    @prescription.setter
    def prescription(self, line_list):
        self._prescription = line_list

    # 效果
    @property
    def efficacy(self):
        return self._efficacy

    @efficacy.setter
    def efficacy(self, line):
        self._efficacy = line

    # 说明
    @property
    def explaination(self):
        return self._explaination

    @explaination.setter
    def explaination(self, line):
        self._explaination = line

    # 编者评述
    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, line):
        self._comment = line


def read_file(filepath):
    """
    读取医案文本文件
    :param filepath: 文本文件路径
    :return: 文本全部行
    """
    raw_lines = []
    print('读取文件：' + filepath)
    print('*' * 50)
    with open(filepath, 'r', encoding='utf-8') as fileIn:
        for raw_line in fileIn:
            raw_lines.append(raw_line)
    return raw_lines


def write_file(lines, filepath):
    print('写入文件：' + filepath)
    with open(filepath, 'w', encoding='utf-8') as fileOut:
        lines = [line + '\n' for line in lines]
        fileOut.writelines(lines)


def read_dict(dictpath='./symptomsDict.txt'):
    read_dict = []
    print('读取症状词典：' + dictpath)
    print('*' * 50)
    with open(dictpath, 'r', encoding='utf8') as dictFile:
        for token in dictFile:
            read_dict.append(token.rstrip('\n'))
    return read_dict


# 原始文本格式化
def raw_format(lines):
    """
    医案结构格式化
    合并不合理断句
    :return: 每个部分一行，输出所有行
    """

    print('开始医案结构格式化')
    processed_lines = []
    for line in lines:
        line = line.replace('\n', '')
        if is_chapter_title(line) or is_case_name(line) or is_doctor_name(line) or is_case_content(line):
            processed_lines.append(line)
        else:
            processed_lines[-1] += line
    print('医案结构格式化完毕')
    print('*' * 50)
    return processed_lines


def is_chapter_title(line):
    """
    格式化方法：识别卷标题
    :param line: 一行文本
    :return: 是否是卷标题
    """
    reg_chapter_title = r'第\w+?卷\w+?病案'
    return re.search(reg_chapter_title, line)


def is_case_name(line):
    """
    格式化方法：识别医案标题
    :param line: 一行文本
    :return: 是否是医案标题
    """
    reg_case_name = r'^\w+案(（\w+科）)?'
    return re.search(reg_case_name, line)


def is_doctor_name(line):
    """
    格式化方法：识别医案来源（医生）
    :param line: 一行文本
    :return: 是否是医生
    """
    reg_doctor_name = r'^医者：\w+（\w+）'
    return re.search(reg_doctor_name, line)


def is_case_content(line):
    """
    格式化方法：识别医案内容（keyword中出现的）
    :param line: 一行文本
    :return: 是否是医案内容的开始字段
    """
    keyword_2 = line[0:2]
    keyword_3 = line[0:3]
    return (keyword_2 in keyword) or (keyword_3 in keyword)


# 信息抽取
def info_process(lines):
    mapper = {
        '医者': doctor_name_handler,
        '病者': patient_handler,
        '病名': sickness_handler,
        '原因': etiology_handler,
        '证候': syndromes_handler,
        '诊断': diagnosis_handler,
        '疗法': therapy_handler,
        '处方': prescription_handler,
        '复诊': diagnosis_handler,
        '次诊': diagnosis_handler,
        '次方': prescription_handler,
        '又方': prescription_handler,
        '三方': prescription_handler,
        '四方': prescription_handler,
        '五方': prescription_handler,
        '六方': prescription_handler,
        '七方': prescription_handler,
        '八方': prescription_handler,
        '九方': prescription_handler,
        '十方': prescription_handler,
        '十一方': prescription_handler,
        '十二方': prescription_handler,
        '十三方': prescription_handler,
        '三诊': diagnosis_handler,
        '四诊': diagnosis_handler,
        '五诊': diagnosis_handler,
        '六诊': diagnosis_handler,
        '七诊': diagnosis_handler,
        '八诊': diagnosis_handler,
        '九诊': diagnosis_handler,
        '十诊': diagnosis_handler,
        '十一诊': diagnosis_handler,
        '十二诊': diagnosis_handler,
        '十三诊': diagnosis_handler,
        '说明': explaination_handler,
        '效果': efficacy_handler,
        '廉按': comment_handler
    }
    result = []
    case = ''

    print('开始信息处理')
    print('*' * 50)
    for line in lines:
        if is_chapter_title(line):
            if case:
                result.append(case)
            # line = chapter_title_handler(line)
            pass
        elif is_case_name(line):
            if case:
                result.append(case)

            case = MedicalCase()
            case = case_name_handler(line, case)
        elif is_doctor_name(line):
            case = doctor_name_handler(line, case)
        elif line[0:2] in mapper.keys():
            case = mapper[line[0:2]](line, case)
        elif line[0:3] in mapper.keys():
            case = mapper[line[0:3]](line, case)
        else:
            # print('未处理的行：' + line)
            continue
    return result


def chapter_title_handler(line):
    """
    卷标题处理
    好像并不用做什么处理
    :param line: 卷标题行
    :return: 卷标题行
    """
    return line


def case_name_handler(line, case):
    """
    医案名称处理
    :param line: 医案名文本行
    :param case: 待更新医案
    :return: 更新后医案
    """
    re_name = r'\w+案'
    re_type = r'\w+科'

    case.case_name = {'病案名': re.search(re_name, line).group()}
    if re.search(re_type, line):
        case.case_type = {'病案科属': re.search(re_type, line).group()}
    return case


def doctor_name_handler(line, case):
    """
    医者名处理
    :param line: 文本行
    :param case: 待更新医案
    :return: 更新后医案
    """
    case.case_doctor = {'医者': (line.split('：'))[-1].strip(' \n')}
    return case


def patient_handler(line, case):
    """
    病人处理
    :param line: 病者文本行
    :param case: 当前医案
    :return: 更新后的医案
    """

    def is_age(item):
        re_1 = r'[逾一二三四五六七八九十两廿岁旬]'
        re_2 = r'(弱冠)|(不惑)|(而立)|(知命)|(知天命)|(花甲)|(古稀)|(耄耋)|(期颐)'
        flag = False
        if re.search(r'^年', item) and re.search(re_1, item):
            flag = True
        elif re.search(re_2, item):
            flag = True
        return flag

    def is_prof(item):
        re_prof_1 = r'^业'
        re_prof_2 = r'[业任界士农工商]|开设|商人|学生|员|经理'
        return re.search(re_prof_1, item) or re.search(re_prof_2, item)

    def is_sign(item):
        re_sign = r'[形体强壮瘦弱高矮胖]'
        return re.search(re_sign, item)

    tokens = (line.split('：')[1]).split('，')

    # 默认第一个短语就是病人名字
    patient_name = tokens[0]
    patient_sex = '男'
    patient_age = '不详'
    patient_prof = '不详'
    patient_sign = '不详'

    if re.search(r'[妻氏妇嫒姑媳室姐姊妹娥媪嫂母]|夫人|女士|女[^公子]', line):
        patient_sex = '女'
    for token in tokens:
        if is_age(token):
            # 病者年龄
            patient_age = token.replace('年', '')
        elif is_prof(token):
            patient_prof = token.strip(' \n')
        elif is_sign(token):
            patient_sign = token.strip(' \n')

    patient_info = {
        '病者姓名': patient_name,
        '病者性别': patient_sex,
        '病者年龄': patient_age,
        '病者职业': patient_prof,
        '病者体征': patient_sign
    }

    case.patient = patient_info
    return case


def sickness_handler(line, case):
    tokens = line.split('：')
    sickness = {tokens[0]: tokens[1].rstrip('。\n')}
    case.sickness = sickness
    return case


def etiology_handler(line, case):
    tokens = line.split('：')
    etiology = {tokens[0]: tokens[1].rstrip('。\n')}
    case.etiology = etiology
    return case


def syndromes_handler(line, case):
    syndromes = []
    additional_syndict = ['疼', '痛', '酸', '麻', '肿', '胀']
    line = line.split("：")[-1].strip('\n')
    big_syndrome_dict = syndrome_dict + additional_syndict
    for syndrome in big_syndrome_dict:
        if line.find(syndrome) != -1:
            re_str = '\w+(' + syndrome + ')\w+'
            re_synd = re.compile(re_str)
            tokens = re.search(re_synd, line)
            if tokens:
                syndromes.append(tokens.group())
    if not syndromes:
        syndromes.append(line)
    instance_syndromes = {
        '证候': syndromes
    }
    case.syndromes = instance_syndromes
    return case


def diagnosis_handler(line, case):
    big_dict = ['脉', '沉', '浮', '数', '左', '右', '寸', '关', '尺', '舌', '苔', '体', '面', '手', '身']\
            + syndrome_dict\
            + sickness_dict
    diagnosis = {}
    tokens = line.split('：')
    number_of_diagnosis = tokens[0]
    line = tokens[-1]
    for kwd in big_dict:
        if line.find(kwd) != -1:
            re_str = '\w*' + kwd + '\w*'
            re_diag = re.compile(re_str)
            tokens = re.findall(re_diag, line)
            for token in tokens:
                if token not in diagnosis.keys():
                    diagnosis[token] = 1
    instance_diagnosis = {
        number_of_diagnosis: list(diagnosis.keys())
    }
    case.diagnosis.append(instance_diagnosis)
    return case


def therapy_handler(line, case):
    case.therapy = {
        '疗法': line.strip('\n')
    }
    return case


def prescription_handler(line, case):
    reg_exp = r'[半一二两三四五六七八九十钱][半厘钱分两枚片颗滴瓢对杯碗](（.+?）)?'

    def repl(match):
        return match.group(0) + ' '

    def token_strip(token):
        return token.strip('，。、\n ')

    tokens = line.split('：')
    number_of_prescription = tokens[0]
    prescription = list(map(token_strip, tokens[-1].split(' ')))
    case.prescription.append({number_of_prescription: prescription})
    return case


def efficacy_handler(line, case):
    case.efficacy = {'效果': line.split('：')[-1].strip('\n')}
    return case


def explaination_handler(line, case):
    case.explaination = {'说明': line.split('：')[-1].strip('\n')}
    return case


def comment_handler(line, case):
    case.comment = {'廉按': line.split('：')[-1].strip('\n')}
    return case


syndrome_dict = read_dict()
sickness_dict = read_dict('sicknessDict.txt')

if __name__ == '__main__':
    raw_lines = read_file('./processed.txt')
    results = info_process(raw_lines)
    for result in results:
        print(result.case_name)
        print(result.case_type)
        print(result.case_doctor)
        print(result.patient)
        print(result.sickness)
        print(result.etiology)
        print(result.syndromes)
        print(result.diagnosis)
        print(result.therapy)
        print(result.prescription)
        print(result.efficacy)
        print(result.explaination)
        print(result.comment)
        print('\n')
