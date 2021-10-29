# Задание №2: Закодируйте любую строку из трех слов по алгоритму Хаффмана.

from collections import deque as dq

print('Здравствуйте! Вас приветствует программа для кодировки любой строки из трёх '
      'слов по алгоритму Хаффмана')


class UsersNode:
    def __init__(self, value, users_letter=None, left=None, right=None):
        self.value = value
        self.users_letter = users_letter
        self.right = right
        self.left = left


def search_users(node, path='',):
    if node.users_letter is not None:
        node.value = 0
        return node.users_letter, path
    if node.right is not None and node.right.value != 0:
        error_our = search_users(node.right, path=f'{path}1')
        if node.right.value == 0 and node.left.value == 0:
            spamnode.value = 0
        return error_our
    if node.left is not None and node.left.value != 0:
        error_our = search_users(node.left, path=f'{path}0')
        if node.right.value == 0 and node.left.value == 0:
            node.value = 0
        return error_our


s = input('Введите строку для кодирования в двоичным коде на руском языке: \n')


users_d = {}
for y in s:
    if y not in users_d :
        users_d [y] = 1
    else:
        users_d [y] += 1

node_list = dq([UsersNode(users_d [i], i) for i in users_d])

for i in range(len(users_d )-1):
    node_list = dq(sorted(node_list, key=lambda node: node.value))
    first_el = node_list.popleft()
    second_el = node_list.popleft()
    new_node = UsersNode(first_el.value + second_el.value, left=first_el, right=second_el)
    node_list.appendleft(new_node)
tree_users = node_list[0]


users_l = {}
for _ in range(len(users_d )):
    k = search_users(tree_users)
    users_l[k[0]] = k[1]
del tree_users

print(f'Введённая Вами строка из трёх букв :\n{s}')

print('Ваша строка в двоичном коде: ')
for p in s:
    print(users_l[p], end=' ')

print()

print('Спасибо, что воспользовались нашей программой! ')
