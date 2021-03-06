from unittest.mock import patch
from nose.tools import ok_, eq_, raises

import moncli.columnvalue as cv
import moncli.entities as e
from moncli.enums import ColumnType, BoardKind

USERNAME = 'test.user@foobar.org' 
GET_ME_RETURN_VALUE = e.user.User(**{'creds': None, 'id': '1', 'email': USERNAME})

@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.create_board')
@patch('moncli.api_v2.create_column')
def test_should_add_new_column(create_column, create_board, get_me):

    # Arrange
    title = 'Text Column 1'
    column_type = ColumnType.text
    get_me.return_value = GET_ME_RETURN_VALUE
    create_board.return_value = {'id': '1', 'name': 'Test Board 1'}
    create_column.return_value = {'id': '1', 'title': title, 'type': column_type}
    client = e.client.MondayClient(USERNAME, '', '')
    board = client.create_board('Test Board 1', BoardKind.public)

    # Act 
    column = board.add_column(title, column_type)

    # Assert
    ok_(column != None)
    eq_(column.title, title)
    eq_(column.type, column_type)


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.create_board')
@patch('moncli.api_v2.get_boards')
def test_should_retrieve_list_of_columns(get_columns, create_board, get_me):

    # Arrange
    title = 'Text Column 1'
    column_type = ColumnType.text
    get_me.return_value = GET_ME_RETURN_VALUE
    create_board.return_value = {'id': '1', 'name': 'Test Board 1'}
    get_columns.return_value = [{'id': '1', 'columns': [{'id': '1', 'title': title, 'type': column_type}]}]
    client = e.client.MondayClient(USERNAME, '', '')
    board = client.create_board('Test Board 1', BoardKind.public)

    # Act 
    columns = board.get_columns()

    # Assert
    ok_(columns != None)
    eq_(len(columns), 1)
    eq_(columns[0].title, title)
    eq_(columns[0].type, column_type)


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.create_board')
@patch('moncli.api_v2.create_group')
def test_should_create_a_new_group(create_group, create_board, get_me):

    # Arrange
    title = 'Group 1'
    get_me.return_value = GET_ME_RETURN_VALUE
    create_board.return_value = {'id': '1', 'name': 'Test Board 1'}
    create_group.return_value = {'id': '1', 'title': title}
    client = e.client.MondayClient(USERNAME, '', '')
    board = client.create_board('Test Board 1', BoardKind.public)

    # Act 
    group = board.add_group(title)

    # Assert
    ok_(group != None)
    eq_(group.title, title)


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.create_board')
@patch('moncli.api_v2.get_boards')
def test_should_retrieve_a_list_of_groups(get_boards, create_board, get_me):

    # Arrange
    title = 'Group 1'
    get_me.return_value = GET_ME_RETURN_VALUE
    create_board.return_value = {'id': '1', 'name': 'Test Board 1'}
    get_boards.return_value = [{'id': '1', 'groups': [{'id': '1', 'title': title}]}]
    client = e.client.MondayClient(USERNAME, '', '')
    board = client.create_board('Test Board 1', BoardKind.public)

    # Act 
    groups = board.get_groups()

    # Assert
    ok_(groups != None)
    eq_(len(groups), 1)
    eq_(groups[0].title, title)


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.create_board')
@raises(e.exceptions.NotEnoughGetGroupParameters)
def test_board_should_fail_to_retrieve_a_group_from_too_few_parameters(create_board, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    create_board.return_value = {'id': '1', 'name': 'Test Board 1'}
    client = e.client.MondayClient(USERNAME, '', '')
    board = client.create_board('Test Board 1', BoardKind.public)

    # Act 
    board.get_group()


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.create_board')
@raises(e.exceptions.TooManyGetGroupParameters)
def test_board_should_fail_to_retrieve_a_group_from_too_many_parameters(create_board, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    create_board.return_value = {'id': '1', 'name': 'Test Board 1'}
    client = e.client.MondayClient(USERNAME, '', '')
    board = client.create_board('Test Board 1', BoardKind.public)

    # Act 
    board.get_group(id='group1', title='Group 1')


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.create_board')
@patch('moncli.api_v2.get_boards')
def test_should_retrieve_a_group_by_id(get_boards, create_board, get_me):

    # Arrange
    id = '1'
    title = 'Group 1'
    get_me.return_value = GET_ME_RETURN_VALUE
    create_board.return_value = {'id': '1', 'name': 'Test Board 1'}
    get_boards.return_value = [{'id': '1', 'groups': [{'id': id, 'title': title}]}]
    client = e.client.MondayClient(USERNAME, '', '')
    board = client.create_board('Test Board 1', BoardKind.public)

    # Act 
    group = board.get_group(id=id)

    # Assert
    ok_(group != None)
    eq_(group.id, id)
    eq_(group.title, title)


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.create_board')
@patch('moncli.api_v2.get_boards')
def test_should_retrieve_a_group_by_title(get_boards, create_board, get_me):

    # Arrange
    id = '1'
    title = 'Group 1'
    get_me.return_value = GET_ME_RETURN_VALUE
    create_board.return_value = {'id': '1', 'name': 'Test Board 1'}
    get_boards.return_value = [{'id': '1', 'groups': [{'id': id, 'title': title}]}]
    client = e.client.MondayClient(USERNAME, '', '')
    board = client.create_board('Test Board 1', BoardKind.public)

    # Act 
    group = board.get_group(title=title)

    # Assert
    ok_(group != None)
    eq_(group.id, id)
    eq_(group.title, title)


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.create_board')
@patch('moncli.api_v2.create_item')
def test_should_create_an_item(create_item, create_board, get_me):

    # Arrange
    board_id = '1'
    name = 'Item 1'
    get_me.return_value = GET_ME_RETURN_VALUE
    create_board.return_value = {'id': board_id, 'name': 'Test Board 1'}
    create_item.return_value = {'id': '1', 'name': name, 'board': {'id': board_id}}
    client = e.client.MondayClient(USERNAME, '', '')
    board = client.create_board('Test Board 1', BoardKind.public)

    # Act 
    item = board.add_item(name)

    # Assert
    ok_(item != None)
    eq_(item.name, name)


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.create_board')
@patch('moncli.api_v2.create_item')
def test_board_should_create_an_item_within_group(create_item, create_board, get_me):

    # Arrange
    board_id = '2'
    name = 'Item 2'
    group_id = 'group2'
    get_me.return_value = GET_ME_RETURN_VALUE
    create_board.return_value = {'id': board_id, 'name': 'Test Board 1'}
    create_item.return_value = {'id': '2', 'name': name, 'board': {'id': board_id}}
    client = e.client.MondayClient(USERNAME, '', '')
    board = client.create_board('Test Board 1', BoardKind.public)

    # Act 
    item = board.add_item(name, group_id=group_id)

    # Assert
    ok_(item != None)
    eq_(item.name, name)


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.create_board')
@patch('moncli.api_v2.create_item')
def test_board_should_create_an_item_with_dict_column_values(create_item, create_board, get_me):

    # Arrange
    board_id = '3'
    name = 'Item 3'
    group_id = 'group2'
    get_me.return_value = GET_ME_RETURN_VALUE
    create_board.return_value = {'id': board_id, 'name': 'Test Board 1'}
    create_item.return_value = {'id': '3', 'name': name, 'board': {'id': board_id}}
    client = e.client.MondayClient(USERNAME, '', '')
    board = client.create_board('Test Board 1', BoardKind.public)

    # Act 
    item = board.add_item(name, group_id=group_id, column_values={'status':{'index': 0}})

    # Assert
    ok_(item != None)
    eq_(item.name, name)


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.create_board')
@patch('moncli.api_v2.create_item')
def test_board_should_create_an_item_with_list_column_values(create_item, create_board, get_me):

    # Arrange
    board_id = '3'
    name = 'Item 4'
    group_id = 'group2'
    get_me.return_value = GET_ME_RETURN_VALUE
    create_board.return_value = {'id': board_id, 'name': 'Test Board 1'}
    create_item.return_value = {'id': '4', 'name': name, 'board': {'id': board_id}}
    client = e.client.MondayClient(USERNAME, '', '')
    board = client.create_board('Test Board 1', BoardKind.public)
    status_column = cv.create_column_value('status', ColumnType.status, 'Status', index=0, settings=e.objects.StatusSettings(labels={'0':'Test'}))

    # Act 
    item = board.add_item(name, group_id=group_id, column_values=[status_column])

    # Assert
    ok_(item != None)
    eq_(item.name, name)


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.create_board')
@patch('moncli.api_v2.get_boards')
@patch('moncli.api_v2.get_items')
def test_should_retrieve_a_list_of_items(get_items, get_boards, create_board, get_me):

    # Arrange
    board_id = '1'
    name = 'Item 1'
    get_me.return_value = GET_ME_RETURN_VALUE
    create_board.return_value = {'id': board_id, 'name': 'Test Board 1'}
    get_boards = [{'id': '1', 'items': [{'id': '1'}]}]
    get_items.return_value = [{'id': '1', 'name': name, 'board': {'id': board_id}}]
    client = e.client.MondayClient(USERNAME, '', '')
    board = client.create_board('Test Board 1', BoardKind.public)

    # Act 
    items = board.get_items()

    # Assert
    ok_(items != None)
    eq_(len(items), 1)
    eq_(items[0].name, name)


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.create_board')
@patch('moncli.api_v2.get_items_by_column_values')
def test_should_retrieve_a_list_of_items_by_column_value(get_items_by_column_values, create_board, get_me):

    # Arrange
    board_id = '1'
    name = 'Item 1'
    get_me.return_value = GET_ME_RETURN_VALUE
    create_board.return_value = {'id': board_id, 'name': 'Test Board 1'}
    get_items_by_column_values.return_value = [{'id': '1', 'name': name, 'board': {'id': board_id}}]
    client = e.client.MondayClient(USERNAME, '', '')
    board = client.create_board('Test Board 1', BoardKind.public)

    # Act 
    column_value = cv.create_column_value('text_column_01', ColumnType.text, value='Some Value')
    items = board.get_items_by_column_values(column_value)

    # Assert
    ok_(items != None)
    eq_(len(items), 1)
    eq_(items[0].name, name)


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.create_board')
@raises(e.exceptions.NotEnoughGetColumnValueParameters)
def test_should_fail_from_too_few_parameters(create_board, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    create_board.return_value = {'id': '1', 'name': 'Test Board 1'}
    client = e.client.MondayClient(USERNAME, '', '')
    board = client.create_board('Test Board 1', BoardKind.public)

    # Act 
    board.get_column_value()


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.create_board')
@raises(e.exceptions.TooManyGetColumnValueParameters)
def test_should_fail_from_too_many_parameters(create_board, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    create_board.return_value = {'id': '1', 'name': 'Test Board 1'}
    client = e.client.MondayClient(USERNAME, '', '')
    board = client.create_board('Test Board 1', BoardKind.public)

    # Act 
    board.get_column_value(id='text_column_01', title='Text Column 01')


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.create_board')
@patch('moncli.api_v2.get_boards')
def test_should_get_column_value_by_id(get_boards, create_board, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    create_board.return_value = {'id': '1', 'name': 'Test Board 1'}
    get_boards.return_value = [{'id': '1', 'columns':[{'id': 'text_column_01', 'title': 'Text Column 01', 'type': 'text'}]}]
    client = e.client.MondayClient(USERNAME, '', '')
    board = client.create_board('Test Board 1', BoardKind.public)

    # Act 
    column_value = board.get_column_value(id='text_column_01')

    # Assert
    ok_(column_value != None)
    eq_(column_value.id, 'text_column_01')
    eq_(column_value.title, 'Text Column 01')
    eq_(type(column_value), cv.TextValue)


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.create_board')
@patch.object(e.board.Board, 'get_columns')
def test_should_get_column_value_by_title(get_columns, create_board, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    create_board.return_value = {'id': '1', 'name': 'Test Board 1'}
    get_columns.return_value = [e.objects.Column(**{'id': 'text_column_01', 'title': 'Text Column 01', 'type': 'text'})]
    client = e.client.MondayClient(USERNAME, '', '')
    board = client.create_board('Test Board 1', BoardKind.public)

    # Act 
    column_value = board.get_column_value(title='Text Column 01')

    # Assert
    ok_(column_value != None)
    eq_(column_value.id, 'text_column_01')
    eq_(column_value.title, 'Text Column 01')
    eq_(type(column_value), cv.TextValue)