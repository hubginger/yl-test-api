# coding=utf-8
"""
    yaml.load 和 yaml.dump

# 读取哪些列 :
column:
  - case_id
  - url
  - method
  - data
  - expected
  - expected_response
# 回写列 :
write_back:
    actual
# 读取列的列索引 :
column_index: [1, 2, 3, 4]

"""


# @Time    :  2024-01-01 20:23:37
# @Author  :  jiangtong
# @Email   :  jiangtong@yljt.cn
# @Project :  yljk_test_api
# @File    :  demo_yaml


class DoYaml:

    @staticmethod
    def change(path, key, value):
        with open(path, 'r', encoding='utf-8') as f:
            lines = []
            for line in f.readlines():
                if line != '\n':
                    lines.append(line)
            f.close()
        with open(path, 'w', encoding='utf-8') as f:
            flag = 0
            for line in lines:
                if key in line and '#' not in line:
                    leftstr = line.split(":")[0]
                    newline = "{0}: {1}".format(leftstr, value)
                    line = newline
                    f.write('%s\n' % line)
                    flag = 1
                else:
                    f.write('%s' % line)
            f.close()
        return flag


if __name__ == '__main__':
    yaml_path = r'D:\Job\YL\codes\temp\yljk_test_api\static\conf\excel.yml'
    # DoYaml.change(yaml_path, 'column_index', [1, 2, 3, 4])
    DoYaml.change(yaml_path, 'write_back', {'a':'aaa'})
    from common import do_conf

    _all = do_conf.read_all('excel')
    print(_all)
    print(type(_all.get('column_index')))
