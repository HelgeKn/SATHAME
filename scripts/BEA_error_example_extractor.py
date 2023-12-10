import errant

def extract_sentences_from_gold(path):
    with open(path, 'r', encoding='utf-8') as file:
        # Read the lines of the file
        lines = file.readlines()

    sentences = []

    for line in lines:
        if line.startswith('S '):
            sentences.append(line[2:].strip())

    with open('sentences.txt', 'w', encoding='utf-8') as file:
        for sentence in sentences:
            file.write(sentence + '\n')

def create_m2_from_corrections(org_path, corr_path):
    with open(org_path, 'r', encoding='utf-8') as file:
        # Read the lines of the file
        org_lines = file.readlines()

    with open(corr_path, 'r', encoding='utf-8') as file:
        # Read the lines of the file
        corr_lines = file.readlines()
    
    counter = 0

    with open('edits.txt', 'w', encoding='utf-8') as file:
        for org_line, corr_line in zip(org_lines, corr_lines):
            annotator = errant.load('en')
            orig = annotator.parse(org_line)
            cor = annotator.parse(corr_line)
            edits = annotator.annotate(orig, cor)

            file.write('S ' + org_line)

            for e in edits:
                file.write('A ' + str(e.o_start) + ' ' + str(e.o_end) + '|||' + str(e.type) + '|||' + e.c_str + '|||REQUIRED|||-NONE-|||0' + '\n')
            
            file.write('\n')
            counter += 1
            print(counter)

def apply_edits(m2_path):
    with open(m2_path, 'r', encoding='utf-8') as file:
        # Read the lines of the file
        lines = file.readlines()

    # List to store the corrected sentences
    corrected_sentences = []

    for line in lines:
        # If the line starts with "S ", add it to corrected_sentences
        if line.startswith('S '):
            corrected_sentences.append(line[2:].strip().split())
            length_diff = 0

        # If the line starts with "A ", apply the correction
        elif line.startswith('A '):
            # Parse the correction
            parts = line[2:].split('|||')
            start, end = map(int, parts[0].split())
            correction = parts[2].split()

            # If the correction is a "noop", continue to the next line
            if parts[1] == 'noop':
                continue

            start += length_diff
            end += length_diff

            # Apply the correction to the last sentence in corrected_sentences
            sentence = corrected_sentences[-1]
            if start == end:  # Addition
                corrected_sentences[-1] = sentence[:start] + correction + sentence[start:]
            else:  # Replacement or removal
                corrected_sentences[-1] = sentence[:start] + correction + sentence[end:]

            length_diff += len(correction) - (end - start)

    # Write the corrected sentences to a new file
    with open('corrected_sentences.txt', 'w', encoding='utf-8') as file:
        for sentence in corrected_sentences:
            file.write(' '.join(sentence) + '\n')

def compare_files(file1_path, file2_path, file3_path):
    with open(file1_path, 'r', encoding='utf-8') as file1, \
         open(file2_path, 'r', encoding='utf-8') as file2, \
         open(file3_path, 'r', encoding='utf-8') as file3, \
         open('pre_bea.txt', 'w', encoding='utf-8') as output:

        correct_lines = file3.readlines()
        correct_lines = iter(correct_lines)
        counter_correct = 0
        current_sentence = ''

        for i, (line1, line2) in enumerate(zip(file1, file2), start=1):
            if line1.strip() != line2.strip():
                id_str = str(i).zfill(4)  # Make the ID always 4 characters long

                # Get the original sentence            
                for correct_line in correct_lines:
                    if correct_line.startswith('S '):
                        if counter_correct == (i - 1):
                            current_sentence = correct_line[2:]
                            counter_correct += 1
                            break
                        counter_correct += 1

                if current_sentence:
                    current_sentence = current_sentence.rstrip('\n')
                    output.write(f'{id_str}###{current_sentence}\n')
                    current_sentence = ''

def extend_bea_file(file1_path, file2_path, file3_path):
    with open(file1_path, 'r', encoding='utf-8') as file1, \
         open(file2_path, 'r', encoding='utf-8') as file2, \
         open(file3_path, 'r', encoding='utf-8') as file3, \
         open('bea.txt', 'w', encoding='utf-8') as output:
        
        main_lines = file1.readlines()
        wrong_lines = file3.readlines()
        correct_lines = file2.readlines()

        wrong_lines = iter(wrong_lines)
        correct_lines = iter(correct_lines)

        counter_wrong = 0
        counter_correct = 0

        for main_line in main_lines:
            split_line = main_line.split('###')

            current_id = split_line[0]
            current_text = split_line[1]

            # print(current_id)
            # print(current_text)

            search = int(current_id) - 1

            # Get the wrong edits
            wrong_edits = []
            for wrong_line in wrong_lines:
                if wrong_line.startswith('S '):
                    if counter_wrong == search:
                        counter_wrong += 1
                        break
                    counter_wrong += 1
            
            for wrong_line in wrong_lines:
                if not wrong_line.startswith('A '):
                    break
                wrong_split = wrong_line[2:].split('|||')
                wrong_edits.append(wrong_split[0] + '|||' + wrong_split[1] + '|||' + wrong_split[2])

            if not wrong_edits:
                wrong_edits.append('no prediction')

            # Get the correct edits
            correct_edits = []
            for correct_line in correct_lines:
                if correct_line.startswith('S '):
                    if counter_correct == search:
                        counter_correct += 1
                        break
                    counter_correct += 1
            
            for correct_line in correct_lines: 
                if not correct_line.startswith('A '):
                    break
                correct_split = correct_line[2:].split('|||')
                correct_edits.append(correct_split[0] + '|||' + correct_split[1] + '|||' + correct_split[2])
            
            # Combine edits
            combined_wrong = '@@@'.join(wrong_edits)
            combined_correct = '@@@'.join(correct_edits)

            # Write full line to file
            current_text = current_text.rstrip('\n')
            output.write(f'{current_id}###{combined_wrong}###{combined_correct}###{current_text}\n')
                

path1 = r'D:\ThesisRepo\SATHAME\static\datasets\BEA2019\input.txt'
path2 = r'D:\ThesisRepo\SATHAME\static\datasets\BEA2019\output_no_new_lines.txt'
path3 = r'D:\ThesisRepo\SATHAME\static\datasets\BEA2019\ABCN.dev.gold.bea19.m2'
path4 = r'D:\ThesisRepo\SATHAME\static\datasets\BEA2019\corrected_sentences.txt'
path5 = r'D:\ThesisRepo\SATHAME\static\datasets\BEA2019\edits.txt'
path6 = r'D:\ThesisRepo\SATHAME\static\datasets\BEA2019\pre_bea.txt'

# create_m2_from_corrections(path1, path2)
# apply_edits(path3)
# compare_files(path4, path2, path5)
extend_bea_file(path6, path3, path5)

print('Done')