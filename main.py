def readxml():
    with open('test.xml', 'r') as r:
        return r.readlines()


def is_block(data):
    index = data.find('>')
    start = data[1:index]
    end = data.find('/' + start)
    end = data[end + 1:-1]
    return start == end


def encode_block(data):
    index = data.find('>')
    start = data[1:index]
    end = data.find('/' + start)
    end = data[end + 1:-1]
    if start == end:
        new_data = data[1 + index:-index - 2]
        return start, new_data


def is_list(data):
    index = data.find('>')
    start = data[1:index]
    end_index = data.find('/')
    end_line = end_index + len(start) + 1
    end = data[end_index + 1:end_line]
    next = data[end_line + 2:end_line + 2 + len(start)]
    return start == end and start == next


def is_line(data):
    index = data.find('>')
    start = data[1:index]
    end_index = data.find('/')
    end_line = end_index + len(start) + 1
    end = data[end_index + 1:end_line]
    return start == end


def encode_line(data):
    index = data.find('>')
    start = data[1:index]
    end_index = data.find('/')
    end_line = end_index + len(start) + 1
    end = data[end_index + 1:end_line]
    value = data[index + 1:end_index - 1]
    data = data[end_line + 1:]
    return start, value, data


def get_tags(data):
    start_tag = data[1:data.find('>')]
    slash_index = data.find('/')
    end_index = slash_index + len(start_tag) + 1
    next_tag = data[end_index + 2:end_index + 2 + len(start_tag)]
    return start_tag, next_tag, end_index


def encode_list(data):
    l = []
    start_tag, next_tag, end_index = get_tags(data)
    while start_tag == next_tag:
        start_tag, next_tag, end_index = get_tags(data)
        value = data[data.find('>') + 1:data.find('</')]
        l.append(value)
        data = data[end_index + 1:]
    return l, start_tag, data


def is_new(key, values):
    for l_key in values.keys():
        if l_key == key:
            return False
        else:
            pass
    return True


def delete_space(data):
    res = ''
    for line in data:
        res += line.strip()
    return res


def finish_dict(data):
    level = None
    d = {}
    for line in data[::-1]:
        if level is None:
            level = line['level']
            line.pop('level')
            d = line.copy()
        elif level == line['level']:
            line.pop('level')
            d.update(line.items())
        elif level > line['level']:
            level = line['level']
            d = {line['name']: d}
    return d


if __name__ == '__main__':
    xml = readxml()
    xml = delete_space(xml)
    level = 0
    list_xml = []
    while len(xml) > 0:
        if is_list(xml):
            l, key, xml = encode_list(xml)
            # print(f'[[new list {key} {l}]]')
            list_xml.append({key: l, 'level': level})
        elif is_line(xml):
            key, value, xml = encode_line(xml)
            # print(f'--new line {key}:{value}--')
            list_xml.append({key: value, 'level': level})
        elif is_block(xml):
            key, xml = encode_block(xml)
            # print(f'[new block {key}]')
            list_xml.append({'name': key, 'level': level})
            level += 1
        else:
            break
    print(finish_dict(list_xml))
