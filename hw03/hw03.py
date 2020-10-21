HW_SOURCE_FILE=__file__


def mobile(left, right):
    """Construct a mobile from a left arm and a right arm."""
    assert is_arm(left), "left must be a arm"
    assert is_arm(right), "right must be a arm"
    return ['mobile', left, right]

def is_mobile(m):
    """Return whether m is a mobile."""
    return type(m) == list and len(m) == 3 and m[0] == 'mobile'

def left(m):
    """Select the left arm of a mobile."""
    assert is_mobile(m), "must call left on a mobile"
    return m[1]

def right(m):
    """Select the right arm of a mobile."""
    assert is_mobile(m), "must call right on a mobile"
    return m[2]

def arm(length, mobile_or_planet):
    """Construct a arm: a length of rod with a mobile or planet at the end."""
    assert is_mobile(mobile_or_planet) or is_planet(mobile_or_planet)
    return ['arm', length, mobile_or_planet]

def is_arm(s):
    """Return whether s is a arm."""
    return type(s) == list and len(s) == 3 and s[0] == 'arm'

def length(s):
    """Select the length of a arm."""
    assert is_arm(s), "must call length on a arm"
    return s[1]

def end(s):
    """Select the mobile or planet hanging at the end of a arm."""
    assert is_arm(s), "must call end on a arm"
    return s[2]

def planet(size):
    """Construct a planet of some size."""
    assert size > 0
    "*** YOUR CODE HERE ***"
    return ['planet', size]

def size(w):
    """Select the size of a planet."""
    assert is_planet(w), 'must call size on a planet'
    "*** YOUR CODE HERE ***"
    return w[1]

def is_planet(w):
    """Whether w is a planet."""
    return type(w) == list and len(w) == 2 and w[0] == 'planet'

def examples():
    t = mobile(arm(1, planet(2)),
               arm(2, planet(1)))
    u = mobile(arm(5, planet(1)),
               arm(1, mobile(arm(2, planet(3)),
                              arm(3, planet(2)))))
    v = mobile(arm(4, t), arm(2, u))
    return (t, u, v)

def total_weight(m):
    """Return the total weight of m, a planet or mobile.

    >>> t, u, v = examples()
    >>> total_weight(t)
    3
    >>> total_weight(u)
    6
    >>> total_weight(v)
    9
    >>> from construct_check import check
    >>> # checking for abstraction barrier violations by banning indexing
    >>> check(HW_SOURCE_FILE, 'total_weight', ['Index'])
    True
    """
    if is_planet(m):
        return size(m)
    else:
        assert is_mobile(m), "must get total weight of a mobile or a planet"
        return total_weight(end(left(m))) + total_weight(end(right(m)))

def balanced(m):
    """Return whether m is balanced.

    >>> t, u, v = examples()
    >>> balanced(t)
    True
    >>> balanced(v)
    True
    >>> w = mobile(arm(3, t), arm(2, u))
    >>> balanced(w)
    False
    >>> balanced(mobile(arm(1, v), arm(1, w)))
    False
    >>> balanced(mobile(arm(1, w), arm(1, v)))
    False
    >>> from construct_check import check
    >>> # checking for abstraction barrier violations by banning indexing
    >>> check(HW_SOURCE_FILE, 'balanced', ['Index'])
    True
    """
    "*** YOUR CODE HERE ***"
    # if is_planet(end(left(m))) and is_planet(end(right(m))):
    #     return length(left(m)) * size(end(left(m))) == length(right(m)) * size(end(right(m)))
    # elif is_mobile(end(left(m))) and is_planet(end(right(m))):
    #     return balanced(end(left(m))) \
    #            and total_weight(end(left(m))) * length(left(m)) == size(end(right(m))) * length(right(m))
    # elif is_planet(end(left(m))) and is_mobile(end(right(m))):
    #     return balanced(end(right(m))) \
    #            and total_weight((end(right(m)))) * length(right(m)) == size(end(left(m))) * length(left(m))
    # else:
    #     return balanced(end(left(m))) and balanced(end(right(m))) \
    #            and total_weight((end(left(m)))) * length(left(m)) == total_weight((end(right(m)))) * length(right(m))
    ###################################################################################################################
    # OK，so the above code is correct, but redundant, it didn't use the fact that planet is itself balanced
    #
    ###################################################################################################################
    if is_planet(m):
        return True
    left_end, right_end = end(left(m)), end(right(m))
    left_torque = total_weight(left_end) * length(left(m))
    right_torque = total_weight(right_end) * length(right(m))
    return balanced(left_end) and balanced(right_end) and left_torque == right_torque



def totals_tree(m):
    """Return a tree representing the mobile with its total weight at the root.

    >>> t, u, v = examples()
    >>> print_tree(totals_tree(t))
    3
      2
      1
    >>> print_tree(totals_tree(u))
    6
      1
      5
        3
        2
    >>> print_tree(totals_tree(v))
    9
      3
        2
        1
      6
        1
        5
          3
          2
    >>> from construct_check import check
    >>> # checking for abstraction barrier violations by banning indexing
    >>> check(HW_SOURCE_FILE, 'totals_tree', ['Index'])
    True
    """
    "*** YOUR CODE HERE ***"
    if is_planet(m):
        return tree(size(m))
    else:
        return tree(total_weight(m), [totals_tree(end(left(m))), totals_tree(end(right(m)))])
        #  for the brances part, we can also do [totals_tree(end(f(m))) for f in [left, right]]


def replace_leaf(t, find_value, replace_value):
    """Returns a new tree where every leaf value equal to find_value has
    been replaced with replace_value.

    >>> yggdrasil = tree('odin',
    ...                  [tree('balder',
    ...                        [tree('thor'),
    ...                         tree('freya')]),
    ...                   tree('frigg',
    ...                        [tree('thor')]),
    ...                   tree('thor',
    ...                        [tree('sif'),
    ...                         tree('thor')]),
    ...                   tree('thor')])
    >>> laerad = copy_tree(yggdrasil) # copy yggdrasil for testing purposes
    >>> print_tree(replace_leaf(yggdrasil, 'thor', 'freya'))
    odin
      balder
        freya
        freya
      frigg
        freya
      thor
        sif
        freya
      freya
    >>> laerad == yggdrasil # Make sure original tree is unmodified
    True
    """
    "*** YOUR CODE HERE ***"
    if is_leaf(t) and label(t) == find_value:
        return tree(replace_value)
    else:
        return tree(label(t), [replace_leaf(b, find_value, replace_value) for b in branches(t)])


from functools import reduce
def preorder(t):
    """Return a list of the entries in this tree in the order that they
    would be visited by a preorder traversal (see problem description).

    >>> numbers = tree(1, [tree(2), tree(3, [tree(4), tree(5)]), tree(6, [tree(7)])])
    >>> preorder(numbers)
    [1, 2, 3, 4, 5, 6, 7]
    >>> preorder(tree(2, [tree(4, [tree(6)])]))
    [2, 4, 6]
    """
    "*** YOUR CODE HERE ***"
    # if is_leaf(t):
    #     return [label(t)]
    # else:
    #     temp = []
    #     for b in branches(t):
    #         temp += preorder(b)
    #     return [label(t)] + temp
    #######################################
    # A more advanced way is to use reduce function
    #
    ######################################
    return reduce(lambda x, y: x + y, [preorder(b) for b in branches(t)], [label(t)])


def has_path(t, word):
    """Return whether there is a path in a tree where the entries along the path
    spell out a particular word.

    >>> greetings = tree('h', [tree('i'),
    ...                        tree('e', [tree('l', [tree('l', [tree('o')])]),
    ...                                   tree('y')])])
    >>> print_tree(greetings)
    h
      i
      e
        l
          l
            o
        y
    >>> has_path(greetings, 'h')
    True
    >>> has_path(greetings, 'i')
    False
    >>> has_path(greetings, 'hi')
    True
    >>> has_path(greetings, 'hello')
    True
    >>> has_path(greetings, 'hey')
    True
    >>> has_path(greetings, 'bye')
    False
    """
    assert len(word) > 0, 'no path for empty word.'
    "*** YOUR CODE HERE ***"
    if len(word) == 1:
        if label(t) != word[0]:
            return False
        else:
            return True
    else:
        ind = False
        for b in branches(t):
            ind = ind or has_path(b, word[1:])
        return label(t) == word[0] and ind



def interval(a, b):
    """Construct an interval from a to b."""
    assert a <= b, 'Lower bound cannot be greater than upper bound'
    # assert is a great tool for sanity check
    return [a, b]

def lower_bound(x):
    """Return the lower bound of interval x."""
    "*** YOUR CODE HERE ***"
    return x[0]

def upper_bound(x):
    """Return the upper bound of interval x."""
    "*** YOUR CODE HERE ***"
    return x[1]

def str_interval(x):
    """Return a string representation of interval x.
    """
    return '{0} to {1}'.format(lower_bound(x), upper_bound(x))

def add_interval(x, y):
    """Return an interval that contains the sum of any value in interval x and
    any value in interval y."""
    lower = lower_bound(x) + lower_bound(y)
    upper = upper_bound(x) + upper_bound(y)
    return interval(lower, upper)

def mul_interval(x, y):
    """Return the interval that contains the product of any value in x and any
    value in y."""
    p1 = lower_bound(x) * lower_bound(y)
    p2 = lower_bound(x) * upper_bound(y)
    p3 = upper_bound(x) * lower_bound(y)
    p4 = upper_bound(x) * upper_bound(y)
    return interval(min(p1, p2, p3, p4), max(p1, p2, p3, p4))


def sub_interval(x, y):
    """Return the interval that contains the difference between any value in x
    and any value in y."""
    # 1. warning, must use value in x MINUS value in y, cannot use
    #                   value in y MINUS value in x.
    # 2. There is a hint in the problem: "Try to reuse functions that have already been implemented
    # if you find yourself repeating code." But I don't know how to reuse code on this problem.
    # 3. OK, I now know when I see the problem description of div_interval.
    "*** YOUR CODE HERE ***"
    # lower = lower_bound(x) - upper_bound(y)
    # upper = upper_bound(x) - lower_bound(y)
    # return interval(lower, upper)
    return add_interval(x, interval(-upper_bound(y), -lower_bound(y)))  # well this solution is complicated?

def div_interval(x, y):
    """Return the interval that contains the quotient of any value in x divided by
    any value in y. Division is implemented as the multiplication of x by the
    reciprocal of y."""
    "*** YOUR CODE HERE ***"
    assert lower_bound(y) > 0 or upper_bound(y) < 0, "Divide by zero" # well, another way to write this is based on
                                                                      # the solution of hw3 assert not (lower_bound(y)
                                                                      # <= 0 <= upper_bound(y)), 'Divide by zero'
    reciprocal_y = interval(1/upper_bound(y), 1/lower_bound(y))
    return mul_interval(x, reciprocal_y)


def multiple_references_explanation():
    return """The multiple reference problem..."""


def quadratic(x, a, b, c):
    """Return the interval that is the range of the quadratic defined by
    coefficients a, b, and c, for domain interval x.

    >>> str_interval(quadratic(interval(0, 2), -2, 3, -1))
    '-3 to 0.125'
    >>> str_interval(quadratic(interval(1, 3), 2, -3, 1))
    '0 to 10'
    """
    "*** YOUR CODE HERE ***"
    # step1: check to see if a > 0
    # min_i = 0
    # max_i = 0
    # def quad(x):
    #     return a*x**2 + b*x + c
    # if a > 0:
    #     # step2: check to see if interval x contains point -b/2a
    #     if lower_bound(x) <= -b/(2*a) <= upper_bound(x):
    #         # then the minimum value is f(-b/2a), maximum is max(f(x.lower), f(x.upper))
    #         min_i = quad(-b/(2*a))
    #         max_i = max(quad(lower_bound(x)), quad(upper_bound(x)))
    #         return interval(min_i, max_i)
    #     elif lower_bound(x) > -b/(2*a): # straight increasing
    #         min_i = quad(lower_bound(x))
    #         max_i = quad(upper_bound(x))
    #         return interval(min_i, max_i)
    #     elif upper_bound(x) < -b/(2*a): # straight decreasing
    #         min_i = quad(upper_bound(x))
    #         max_i = quad(lower_bound(x))
    #         return interval(min_i, max_i)
    # elif a < 0:
    #     # same as step2
    #     if lower_bound(x) <= -b/(2*a) <= upper_bound(x):
    #         # then the maximum value is f(-b/2a) and minimum is min(f(x.lower), f(x.upper))
    #         max_i = quad(-b/(2*a))
    #         min_i = min(quad(lower_bound(x)), quad(upper_bound(x)))
    #         return interval(min_i, max_i)
    #     elif upper_bound(x) < -b/(2*a): # straight increasing
    #         min_i = quad(lower_bound(x))
    #         max_i = quad(upper_bound(x))
    #         return interval(min_i, max_i)
    #     elif lower_bound(x) > -b/(2*a):  # straight decreasing
    #         min_i = quad(upper_bound(x))
    #         max_i = quad(lower_bound(x))
    #         return interval(min_i, max_i)
    ####################################################################################################
    # well, below is a much clever way to deal with the problem, as we only need to use the min and max
    # fucniton to select which of the three points has the lowest and highest value and assign them to
    # the final interval. We don't need to deal with every condition verbosely above.
    ####################################################################################################
    extremum = -b / (2 * a)
    f = lambda x: a * x * x + b * x + c
    l, u, e = map(f, (lower_bound(x), upper_bound(x), extremum))
    if extremum >= lower_bound(x) and extremum <= upper_bound(x):
        return interval(min(l, u, e), max(l, u, e))
    else:
        return interval(min(l, u), max(l, u))


def par1(r1, r2):
    return div_interval(mul_interval(r1, r2), add_interval(r1, r2))

def par2(r1, r2):
    one = interval(1, 1)
    rep_r1 = div_interval(one, r1)
    rep_r2 = div_interval(one, r2)
    return div_interval(one, add_interval(rep_r1, rep_r2))
def check_par():
    """Return two intervals that give different results for parallel resistors.

    >>> r1, r2 = check_par()
    >>> x = par1(r1, r2)
    >>> y = par2(r1, r2)
    >>> lower_bound(x) != lower_bound(y) or upper_bound(x) != upper_bound(y)
    True
    """
    r1 = interval(1, 2) # Replace this line!
    r2 = interval(2, 1) # Replace this line!
    return r1, r2



# Tree ADT

def tree(label, branches=[]):
    """Construct a tree with the given label value and a list of branches."""
    for branch in branches:
        assert is_tree(branch), 'branches must be trees'
    return [label] + list(branches)

def label(tree):
    """Return the label value of a tree."""
    return tree[0]

def branches(tree):
    """Return the list of branches of the given tree."""
    return tree[1:]

def is_tree(tree):
    """Returns True if the given tree is a tree, and False otherwise."""
    if type(tree) != list or len(tree) < 1:
        return False
    for branch in branches(tree):
        if not is_tree(branch):
            return False
    return True

def is_leaf(tree):
    """Returns True if the given tree's list of branches is empty, and False
    otherwise.
    """
    return not branches(tree)

def print_tree(t, indent=0):
    """Print a representation of this tree in which each node is
    indented by two spaces times its depth from the root.

    >>> print_tree(tree(1))
    1
    >>> print_tree(tree(1, [tree(2)]))
    1
      2
    >>> numbers = tree(1, [tree(2), tree(3, [tree(4), tree(5)]), tree(6, [tree(7)])])
    >>> print_tree(numbers)
    1
      2
      3
        4
        5
      6
        7
    """
    print('  ' * indent + str(label(t)))
    for b in branches(t):
        print_tree(b, indent + 1)

def copy_tree(t):
    """Returns a copy of t. Only for testing purposes.

    >>> t = tree(5)
    >>> copy = copy_tree(t)
    >>> t = tree(6)
    >>> print_tree(copy)
    5
    """
    return tree(label(t), [copy_tree(b) for b in branches(t)])

