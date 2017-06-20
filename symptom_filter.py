# -*- coding: utf-8 -*-
"""
医案症状过滤
@liminghao
2017-04-08
"""
import re


def read_file(filepath):
    raw_lines = []
    print('reading file' + filepath)
    print('*' * 50)
    with open(filepath, 'r', encoding='utf-8') as fileIn:
        for raw_line in fileIn:
            raw_lines.append(raw_line)
    return raw_lines


def write_file(lines, filepath):
    print('Writing file: ' + filepath)
    with open(filepath, 'w', encoding='utf-8') as fileOut:
        lines_to_write = [line + '\n' for line in lines]
        fileOut.writelines(lines_to_write)


def main_process(line):
    self_feeling_dict = r'疼|痛|酸楚?|麻|木|痒|胀|冷|[^清]热|闷' \
                        r'|悸|烦|沉重|倦|乏|无力|坠|拘急|僵硬' \
                        r'|善?饥|易?渴|爽|咳|嗽|痉|挛|汗|眠|昏'
    self_feeling_degree = r'轻微|轻度|中度|重度|极度|略|微'
    physical_signs_shape = r'薄|厚|粘|黏|稠|腻|滑|甲错|凹陷|干枯' \
                           r'|外翻|结节|[脉寸关尺舌体面手喉]|洪数|溏|痰'
    physical_signs_analogy = r'\w{2,3}如[^前此常初]\w+\b'
    physical_signs_color = r'[浅淡深黯暗]?[赤红白黄青黑紫皂]色?'
    body_keyword = r'全身|浑身|周身|身'
    partial_keyword = r'[心肺肝胆脾胃胯肾]'
    continuous_keyword = r'[一二三四五六七八九十][年]|[月日]'
    discrete_keyword = r'断续|间或'
    period_keyword = r'早|晚|晨|夜|(日间)|暮|朝|上午|下午'
    condition_keyword = r'(遇\w+则)|则'

    self_feeling_tokens = []
    degree_tokens = []
    shape_tokens = []
    analogy_tokens = []
    color_tokens = []
    body_tokens = []
    partial_tokens = []
    time_prop_tokens = []
    unrecognized = []

    line_content = line.split('：')[-1]
    tokens = re.split('\W+', line_content)

    for token in tokens:
        if re.search('{0}|{1}|{2}|{3}'.format(continuous_keyword, condition_keyword, period_keyword, discrete_keyword),
                     token):
            time_prop_tokens.append(token)
        elif re.search(self_feeling_degree, token):
            degree_tokens.append(token)
        elif re.search(self_feeling_dict, token):
            self_feeling_tokens.append(token)
        elif re.search(physical_signs_shape, token):
            shape_tokens.append(token)
        elif re.search(physical_signs_analogy, token):
            analogy_tokens.append(token)
        elif re.search(physical_signs_color, token):
            color_tokens.append(token)
        elif re.search(body_keyword, token):
            body_tokens.append(token)
        elif re.search(partial_keyword, token):
            partial_tokens.append(token)
        else:
            unrecognized.append(token)

    result = {
        '自觉': self_feeling_tokens,
        '程度': degree_tokens,
        '形态类比': analogy_tokens,
        '体征（他觉）': shape_tokens,
        '颜色': color_tokens,
        '全身症状': body_tokens,
        '局部症状': partial_tokens,
        '时间属性': time_prop_tokens,
        '未识别': unrecognized
    }
    return result


if __name__ == '__main__':
    result_lines = []
    lines_in = read_file('./processed.txt')
    line_head = ['原因', '证候', '诊断', '复诊', '次诊', '三诊',
                  '四诊', '五诊', '六诊', '七诊', '八诊', '九诊', '十诊',
                  '十一诊', '十二诊', '十三诊']
    print('读取文本完毕')
    print('*' * 50)
    print('开始识别')
    for line_in in lines_in:
        line_head = line_in.split('：')[0]
        if line_head in line_heads:
            result_dict = main_process(line_in)
            result_lines.append('原句：' + line_in)
            for key in result_dict:
                result_lines.append(key)
                result_lines.append('[' + ','.join(result_dict[key]) + ']')
            result_lines.append('*' * 80)
    print('写入文件')
    write_file(result_lines, './symptom_extracted.txt')
