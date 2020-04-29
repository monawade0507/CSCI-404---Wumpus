#!/usr/bin/env python

#-------------------------------------------------------------------------------
# Name:        logical_expression
# Purpose:     Contains logical_expression class, inference engine,
#              and assorted functions
#
# Created:     09/25/2011
# Last Edited: 07/22/2013
# Notes:       *This contains code ported by Christopher Conly from C++ code
#               provided by Dr. Vassilis Athitsos
#              *Several integer and string variables are put into lists. This is
#               to make them mutable so each recursive call to a function can
#               alter the same variable instead of a copy. Python won't let us
#               pass the address of the variables, so put it in a list which is
#               passed by reference. We can also now pass just one variable in
#               the class and the function will modify the class instead of a
#               copy of that variable. So, be sure to pass the entire list to a
#               function (i.e. if we have an instance of logical_expression
#               called le, we'd call foo(le.symbol,...). If foo needs to modify
#               le.symbol, it will need to index it (i.e. le.symbol[0]) so that
#               the change will persist.
#              *Written to be Python 2.4 compliant for omega.uta.edu
#-------------------------------------------------------------------------------

import sys
from copy import copy

#-------------------------------------------------------------------------------
# Begin code that is ported from code provided by Dr. Athitsos
class logical_expression:
    """A logical statement/sentence/expression class"""
    # All types need to be mutable, so we don't have to pass in the whole class.
    # We can just pass, for example, the symbol variable to a function, and the
    # function's changes will actually alter the class variable. Thus, lists.
    def __init__(self):
        self.symbol = ['']
        self.connective = ['']
        self.subexpressions = []


def print_expression(expression, separator):
    """Prints the given expression using the given separator"""
    if expression == 0 or expression == None or expression == '':
        print '\nINVALID\n'

    elif expression.symbol[0]: # If it is a base case (symbol)
        sys.stdout.write('%s' % expression.symbol[0])

    else: # Otherwise it is a subexpression
        sys.stdout.write('(%s' % expression.connective[0])
        for subexpression in expression.subexpressions:
            sys.stdout.write(' ')
            print_expression(subexpression, '')
            sys.stdout.write('%s' % separator)
        sys.stdout.write(')')


def read_expression(input_string, counter=[0]):
    """Reads the next logical expression in input_string"""
    # Note: counter is a list because it needs to be a mutable object so the
    # recursive calls can change it, since we can't pass the address in Python.
    result = logical_expression()
    length = len(input_string)
    while True:
        if counter[0] >= length:
            break

        if input_string[counter[0]] == ' ':    # Skip whitespace
            counter[0] += 1
            continue

        elif input_string[counter[0]] == '(':  # It's the beginning of a connective
            counter[0] += 1
            read_word(input_string, counter, result.connective)
            read_subexpressions(input_string, counter, result.subexpressions)
            break

        else:  # It is a word
            read_word(input_string, counter, result.symbol)
            break
    return result


def read_subexpressions(input_string, counter, subexpressions):
    """Reads a subexpression from input_string"""
    length = len(input_string)
    while True:
        if counter[0] >= length:
            print '\nUnexpected end of input.\n'
            return 0

        if input_string[counter[0]] == ' ':     # Skip whitespace
            counter[0] += 1
            continue

        if input_string[counter[0]] == ')':     # We are done
            counter[0] += 1
            return 1

        else:
            expression = read_expression(input_string, counter)
            subexpressions.append(expression)


def read_word(input_string, counter, target):
    """Reads the next word of an input string and stores it in target"""
    word = ''
    while True:
        if counter[0] >= len(input_string):
            break

        if input_string[counter[0]].isalnum() or input_string[counter[0]] == '_':
            target[0] += input_string[counter[0]]
            counter[0] += 1

        elif input_string[counter[0]] == ')' or input_string[counter[0]] == ' ':
            break

        else:
            print('Unexpected character %s.' % input_string[counter[0]])
            sys.exit(1)


def valid_expression(expression):
    """Determines if the given expression is valid according to our rules"""
    if expression.symbol[0]:
        return valid_symbol(expression.symbol[0])

    if expression.connective[0].lower() == 'if' or expression.connective[0].lower() == 'iff':
        if len(expression.subexpressions) != 2:
            print('Error: connective "%s" with %d arguments.' %
                        (expression.connective[0], len(expression.subexpressions)))
            return 0

    elif expression.connective[0].lower() == 'not':
        if len(expression.subexpressions) != 1:
            print('Error: connective "%s" with %d arguments.' %
                        (expression.connective[0], len(expression.subexpressions)))
            return 0

    elif expression.connective[0].lower() != 'and' and \
         expression.connective[0].lower() != 'or' and \
         expression.connective[0].lower() != 'xor':
        print('Error: unknown connective %s.' % expression.connective[0])
        return 0

    for subexpression in expression.subexpressions:
        if not valid_expression(subexpression):
            return 0
    return 1


def valid_symbol(symbol):
    """Returns whether the given symbol is valid according to our rules."""
    if not symbol:
        return 0

    for s in symbol:
        if not s.isalnum() and s != '_':
            return 0
    return 1

# End of ported code
#-------------------------------------------------------------------------------

# ADD ALL YOUR FUNCTIONS HERE

# Add all your functions here


def sym_no_repeat(expression):
# function that extracts, and stores in a list, the set of all symbols
#   used in the Wumpus rule, the KB, and the statement. list should contain
#   no repetitions
    list = []
    if expression.symbol[0]:
        list.append(expression.symbol[0])
    else:
        for i in expression.subexpressions:
            for j in sym_no_repeat(i):
                if j not in list:        # making sure no repetitions
                    list.append(j)


    return list
# ----------------------------------- DONE - sym_no_repeat ---------------------

# simplifies symbols in a statement to TRUE or FALSE
# updates the statement to only have TRUE or FALSE in the same place as the
#   orginal statement
def true_false_replacement(statement):

    list = {}
    for i in statement.subexpressions:
        if i.symbol[0]:
            list[i.symbol[0]] = True
        elif i.connective[0].upper() == 'NOT':
            if i.subexpressions[0].symbol[0]:
                list[i.subexpressions[0].symbol[0]] = False
    return list
# ------------------------------- DONE - ture_false_replacement ----------------

def link_model(model, symbol, value):
    model_new = copy(model)
    model_new[symbol] = value
    return model_new
# ------------------------------- DONE -----------------------------------------

def compare_statement_replacement(statement, replace):

    if statement.symbol[0]:
        return replace[statement.symbol[0]]

    elif statement.connective[0].upper() == 'AND':
        result = True

        for i in statement.subexpressions:
            result = result and compare_statement_replacement(i, replace)
        return result

    elif statement.connective[0].upper() == 'OR':
        result = False

        for i in statement.subexpressions:
            result = result or compare_statement_replacement(i, replace)
        return result

    elif statement.connective[0].upper() == 'XOR':
        result = False

        for i in statement.subexpressions:
            check_valid = compare_statement_replacement(i, replace)
            result = (result and not check_valid) or (not result and check_valid)
        return result

    elif statement.connective[0].upper() == 'IF':
        left = statement.subexpressions[0]
        right = statement.subexpressions[1]

        check_valid_left = compare_statement_replacement(left, replace)
        check_valid_right = compare_statement_replacement(right, replace)

        if (check_valid_left and not check_valid_right):
            return False
        else:
            return True

    elif statement.connective[0].upper() == 'IFF':
        left = statement.subexpressions[0]
        right = statement.subexpressions[1]

        check_valid_left = compare_statement_replacement(left, replace)
        check_valid_right = compare_statement_replacement(right, replace)

        if (check_valid_left == check_valid_right):
            return True
        else:
            return False

    elif statement.connective[0].upper() == 'NOT':
        check_valid = compare_statement_replacement(statement.subexpressions[0], replace)
        return not check_valid
# -------------------- DONE - compare_statement_replacement --------------------


def link_msv(model, symbol, value):
    model[symbol] = value
    return model
#--------------- DONE - link_msv -----------------------------------------------

def check_entail(knowledge_base, statement, symbols, model):
    if not symbols:
        if compare_statement_replacement(knowledge_base, model):
            return compare_statement_replacement(statement, model)
        else:
            return True
    else:
        _test = symbols.pop(0)
        check_total = check_entail(knowledge_base, statement, symbols, link_msv(model, _test, True)) \
            and check_entail(knowledge_base, statement, symbols, link_msv(model, _test, False))
        return check_total
# ------------------------------ DONE - check_entail ---------------------------


def check_true_false(knowledge_base, statement):


    KB_no_repeat = sym_no_repeat(knowledge_base)
    statement_no_repeat = sym_no_repeat(statement)
    true_false = true_false_replacement(knowledge_base)

    for i in statement_no_repeat:
        KB_no_repeat.append(i)

    for i in true_false:
        if i in KB_no_repeat:
            KB_no_repeat.remove(i)

    statement_check = check_entail(knowledge_base, statement, KB_no_repeat, true_false)
    print 'Check that KB entails statement'

    neg_val = logical_expression()
    neg_val.connective[0] = 'not'
    neg_val.subexpressions.append(statement)

    negation_check = check_entail(knowledge_base, neg_val, KB_no_repeat, true_false)
    print 'Check that KB entails negated statement'

    txt = open('result.txt', 'w')
    print 'Opened result.txt for write ...'
    if(statement_check == True and negation_check == False):
        txt.write('definitely true')
    elif(statement_check == False and negation_check == False):
            txt.write('possibly true, possibly false')
    elif(statement_check == True and negation_check == True):
        txt.write('both true and false')
    elif(statement_check == False and negation_check == True):
        txt.write('definitely false')
    else :
        txt.write('result unknow')
    print 'DONE'
    txt.close()
# ------------- DONE - check_true_false ----------------------------------------
