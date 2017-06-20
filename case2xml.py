#!/usr/bin/env python
# encoding: utf8
import preprocess as pr
import xml.etree.ElementTree as et

def read_file(filepath):
    raw_lines = []
    print('reading file' + filepath)
    print('*' * 50)
    with open(filepath, 'r', encoding='utf-8') as fileIn:
        for raw_line in fileIn:
            raw_lines.append(raw_line)
    return raw_lines

def is_prescription(line):
    return line.startswith('处方') or line.startswith('次方') or \
           line.startswith('又方') or line.startswith('三方') or \
           line.startswith('四方') or line.startswith('五方') or \
           line.startswith('六方') or line.startswith('七方') or \
           line.startswith('八方') or line.startswith('九方') or \
           line.startswith('十方') or line.startswith('十一方') or \
           line.startswith('十二方') or line.startswith('十三方')

def is_diagnosis(line):
    return line.startswith('三诊') or \
           line.startswith('四诊') or \
           line.startswith('五诊') or \
           line.startswith('六诊') or \
           line.startswith('七诊') or \
           line.startswith('八诊') or \
           line.startswith('九诊') or \
           line.startswith('十诊') or \
           line.startswith('十一诊') or \
           line.startswith('十二诊') or \
           line.startswith('十三诊')

"""
hooks functions:
if is_chapter_title(line) returns true:
    new a xml root node and set line as its title;
    set each line following as its attribute untill 'LIANAN' is found;
    while 'LIANAN' is found, set this line as the last element of this xml tree and write it to file.
"""
if __name__ == '__main__':
    result_lines = []
    lines = read_file('./processed.txt')
    print('Start process')
    print('*' * 50)
    i = 0
    for line in lines:
        if pr.is_chapter_title(line):
            # discard chapter title.
            continue
        if pr.is_case_name(line):
            # create a new root node:
            case = et.Element('case')

            # create case-title  node
            caseTitle = et.SubElement(case, 'case-title')
            # set this line as attr text
            caseTitle.text = line
            continue
        if pr.is_doctor_name(line):
            # create doctor node and set text
            doctor = et.SubElement(case, 'doctor')
            doctor.text = line
            continue
        if line.startswith('病者'):
            patient = et.SubElement(case, 'patient')
            patient.text = line
            continue
        if line.startswith('病名'):
            sickness = et.SubElement(case, 'sickness')
            sickness.text = line
            continue
        if line.startswith('原因'):
            etiology = et.SubElement(case, 'etiology')
            etiology.text = line
            continue
        if line.startswith('证候'):
            syndromes = et.SubElement(case, 'syndromes')
            syndromes.text = line
            continue
        if line.startswith('诊断'):
            diagnosis = et.SubElement(case, 'diagnosis')
            diagnosis.text = line
            continue
        if line.startswith('疗法'):
            therapy = et.SubElement(case, 'therapy')
            therapy.text = line
            continue
        if is_prescription(line):
            prescription = et.SubElement(case, 'prescription')
            prescription.text = line
            continue
        if is_diagnosis(line):
            diagnosis = et.SubElement(case, 'diagnosis')
            diagnosis.text = line
            continue
        if line.startswith('说明'):
            explaination = et.SubElement(case, 'explaination')
            explaination.text = line
            continue
        if line.startswith('效果'):
            efficacy = et.SubElement(case, 'efficacy')
            efficacy.text = line
            continue
        if line.startswith('廉按'):
            comment = et.SubElement(case, 'comment')
            comment.text = line
            continue
        if line == '\n':
            tree = et.ElementTree(case)
            tree.write('case-' + str(i) + '.xml')
            i = i + 1



