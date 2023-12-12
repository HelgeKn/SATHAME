import csv

data_path = r'D:\ThesisRepo\SATHAME\static\datasets\Swag\val.csv'

pred_path = r'D:\ThesisRepo\SATHAME\static\datasets\Swag\microsoft-deberta-v3-large-epoch-1.csv'

with open(data_path, 'r', encoding='utf-8') as data, \
    open(pred_path, 'r', encoding='utf-8') as pred, \
    open('Swag.txt', 'w', encoding='utf-8') as output:
    
    data_lines = csv.reader(data)
    pred_lines = csv.reader(pred)

    next(data_lines, None)
    next(pred_lines, None)

    for data_split_line, pred_split_line in zip(data_lines, pred_lines):
        id = str(data_split_line[0]).zfill(4)
        id = 'swag_' + id

        if data_split_line[-1] != pred_split_line[0]:
            build_result = id + '###' + data_split_line[7 + int(pred_split_line[0])] + '###' + data_split_line[7 + int(data_split_line[-1])] + '###' + data_split_line[3] 
            output.write(build_result + '\n')