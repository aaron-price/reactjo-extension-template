import os
import copy
import json
import re
from six import string_types
from helpers.data_detection import get_brackets, get_type, list_index_positions, detect_duplicate
from helpers.commas import soft_comma
from helpers.path_manager import parse_shortcuts

def file_append(path, content):
    file = open(path, 'a')
    file.write('\n' + content)
    file.close()

def file_append_safe(path, content):
    file = open(path, 'r').read()
    i = file.find(content)
    if i == -1:
        file_append(path, content)

def file_prepend(path, content):
    old_file = open(path, 'r').read()
    new_file = open(path, 'w')
    new_file.write(content + '\n')
    new_file.write(old_file)
    new_file.close()

def file_prepend_safe(path, content):
    file = open(path, 'r').read()
    i = file.find(content)
    if i == -1:
        file_prepend(path, content)

def file_write(path, content):
    file = open(path, 'w')
    file.write(content)
    file.close()

def file_remove(path):
    os.remove(path)

def json_read(path):
    with open(path, 'r') as file:
        return json.load(file)

def json_write(path, content):
    with open(path, 'w') as file:
        json.dump(content, file, indent = 4)

def file_read(path, data = None):
    if data == None:
        return open(path, 'r').read()
    else:
        string = open(path, 'r').read()
        start  = 0
        after_start = 0
        stop   = len(string)

        for target in data:
            if isinstance(target, string_types):
                obj     = string.find(target, start)
                start   = obj
                after_start = get_brackets(string, start)['start'] + 1
                stop    = get_brackets(string, start)['stop']
            else:
                indices = list_index_positions(string, start - 1, stop)
                obj     = indices[target]
                start   = obj
                after_start = get_brackets(string, start)['start'] + 1
                stop    = get_brackets(string, start)['stop']

        # checks for pesky tabs, spaces, and newlines
        def before_stop(count = 1):
            c = string[stop - count]
            if c in [' ','\n','\t']:
                return before_stop(count + 1)
            else:
                return stop - count + 1

        return {
            'start': start,
            'after_start': after_start,
            'stop': stop,
            'before_stop': before_stop(),
            'string': string[start:stop + 1]
        }

def obj_prepend(path, data):
    file = file_read(path)
    target = file_read(path, data['target'])
    after_start = target['after_start']
    existing_data = target['string']
    duplicate = detect_duplicate(existing_data, data['content'])
    if duplicate:
        print(data['content'] + ' already exists in ' + existing_data + '... skipping.')
    else:
        print("AFTER_START", target['after_start'])
        before = file[:after_start]
        content = data['content']
        after = file[after_start:]
        string = before + soft_comma(content, after)

        file_write(path, string)

def obj_append(path, data):
    # example data:
    # data = {
    #     'target': ['config', 'more'],
    #     'content': ",\n'kittens'"
    # }
    file = file_read(path)
    target = file_read(path, data['target'])

    before_stop = target['before_stop']
    existing_data = target['string']
    duplicate = detect_duplicate(existing_data, data['content'])
    if duplicate:
        print(data['content'] + ' already exists in ' + existing_data + '... skipping.')
    else:
        before = file[:before_stop]
        content = data['content']
        after = file[before_stop:]
        beginning = soft_comma(before, content)

        file_write(path, beginning + after)

def ln_remove(path, data):
    file = file_read(path)
    startIndex = file.find(data['target'])
    endIndex = file.find('\n', startIndex)
    start = file[:startIndex]
    end = file[endIndex:]

    file_write(path, start + end)

def ln_overwrite(path, data):
    file = file_read(path)
    startIndex = file.find(data['target'])
    endIndex = file.find('\n', startIndex)
    start = file[:startIndex]
    end = file[endIndex:]

    file_write(path, start + data['content'] + end)


def file_parse(path, data):
    string = file_read(path)
    item_starts   = [m.start() for m in re.finditer("<%", string)]
    item_ends     = [m.start() for m in re.finditer("%>", string)]
    items = []

    for n,i in enumerate(item_starts):
        start = item_starts[n]
        end   = item_ends[n] + 2
        item = string[start:end]
        key = item.strip("<%").strip("%>").strip(" ")

        items.append({'text': item, 'k': key})

    for i in items:
        string = string.replace(i['text'], data[i['k']], 1)

    return string

def file_manager(path, query, data = None):
    path = parse_shortcuts(path)
    q = query.lower()

    # If data is a path, then pass the file contents instead of the path
    if isinstance(data, string_types):
        if os.path.exists(parse_shortcuts(data)):
            data = file_manager(data, 'r')

    if q in ['?','exists']:
        return os.path.exists(path)
    if q in ['$' ,'path']:
        return path
    if q in ['w', 'write', 'create']:
        if isinstance(data, string_types):
            file_write(path, data)
        else:
            ln_overwrite(path, data)
    if q in ['d','remove','delete']:
        file_remove(path)
    if q in ['f','format']:
        return file_parse(path, data)
    if q in ['p', 'prepend']:
        if isinstance(data, string_types):
            file_prepend_safe(path, data)
        else:
            obj_prepend(path, data)
    if q in ['r', 'read','open']:
        if path.lower().endswith('.json'):
            return json_read(path)
        else:
            if data == None:
                return file_read(path, data)
            else:
                return file_read(path, data)['string']
    if q in ['a', 'append','add','after']:
        if isinstance(data, string_types):
            file_append_safe(path, data)
        else:
            obj_append(path, data)
