import math
import time
import random
import io


class key:
    def key(self):
        return "10jifn2eonvgp1o2ornfdlf-1230"


class ai:
    def __init__(self):
        self.head = None

    class state:
        def __init__(self, a, b, a_fin, b_fin):
            self.a = a
            self.b = b
            self.a_fin = a_fin
            self.b_fin = b_fin

        def __str__(self):
            print(f"a: {self.a}")
            print(f"b: {self.b}")
            print(f"afin: {self.a_fin}")
            print(f"bfin: {self.b_fin}")
            return ""

    # Kalah:
    #         b[5]  b[4]  b[3]  b[2]  b[1]  b[0]
    # b_fin                                         a_fin
    #         a[0]  a[1]  a[2]  a[3]  a[4]  a[5]
    # Main function call:
    # Input:
    # a: a[5] array storing the stones in your holes
    # b: b[5] array storing the stones in opponent's holes
    # a_fin: Your scoring hole (Kalah)
    # b_fin: Opponent's scoring hole (Kalah)
    # t: search time limit (ms)
    # a always moves first
    #
    # Return:
    # You should return a value 0-5 number indicating your move, with search time limitation given as parameter
    # If you are eligible for a second move, just neglect. The framework will call this function again
    # You need to design your heuristics.
    # You must use minimax search with alpha-beta pruning as the basic algorithm
    # use timer to limit search, for example:
    # start = time.time()
    # end = time.time()
    # elapsed_time = end - start
    # if elapsed_time * 1000 >= t:
    #    return result immediately
    def move(self, a, b, a_fin, b_fin, t):
        """
        Decide which step AI should take and return the index
        """
        self.head = self.state(a, b, a_fin, b_fin)

        f = open('time.txt', 'a')
        d = 6
        res = -1
        # Try depth of 6, 7, 8, and 9
        for d in [6, 7, 8, 9]:
            f.write('depth = '+str(d)+'\n')
            t_start = time.time()
            res = self.minimax(depth=d)
            f.write(str(time.time()-t_start)+'\n')
        f.close()

        return res

    def minimax(self, depth):
        """
        Minmax Algorithm that decide action based on the depth

        Args:
            depth (int): Recursion depth

        Returns:
            int: the action AI should take, i.e. the index of field AI take
        """
        a, v = self.Max_Value(self.head, -math.inf, math.inf, depth)
        if a == -1:
            return self.successorForA(self.head)[0][0]
        return a

    def successorForA(self, state: state):
        """
        Returns the successor of the current state for AI's side

        Args:
            state (state): Current Kalah state

        Returns:
            list: a list of current state's successors, which include
            the successors' action index and if it is allowed to take the 
            next step (for AI side)
        """
        # Construct a list of movable steps
        r = []
        for i in range(6):
            if state.a[i] != 0:
                r.append(i)

        # Traverse through all the moveable steps and generate successors as list
        states = []
        for i in r:
            newState, isKalah = self.step(state, i)
            states.append((i, isKalah, newState))

        return states

    def successorForB(self, state: state):
        """
        Returns the successor of the current state for opponent's side

        Args:
            state (state): Current Kalah state

        Returns:
            list: a list of current state's successors, which include
            the successors' action index and if it is allowed to take the 
            next step (for opponent side)
        """
        # Construct a list of movable steps
        r = []
        for i in range(6):
            if state.b[::-1][i] != 0:
                r.append(i)

        # Traverse through all the moveable steps and generate successors as list
        states = []
        for i in r:
            newState, isKalah = self.step(self.state(
                state.b[::-1], state.a[::-1], state.b_fin, state.a_fin), i)
            states.append((i, isKalah, self.state(
                newState.b[::-1], newState.a[::-1], newState.b_fin, newState.a_fin)))

        return states

    def step(self, oldState: state, i):
        """
        Calculate the next state by the given action

        Args:
            oldState (state): original state
            i (int): the action index

        Returns:
            list, bool: the next state taken by the next step
        """
        oldN = oldState.a[i]
        n = oldN
        res = self.state(oldState.a.copy(), oldState.b.copy(),
                         oldState.a_fin, oldState.b_fin)

        res.a[i] = 0
        i += 1
        mod = -1

        # Traverse through the new state and take steps
        while n > 0:
            mod = i % 13
            if mod == 6:
                res.a_fin += 1
            elif i % 13 < 6:
                res.a[mod] += 1
            else:
                res.b[12 - (mod)] += 1
            n -= 1
            i += 1

        # Calculate situation if it is landed on a empty spot and take the
        # opponent's point
        if mod < 6 and oldN < 13 and oldState.a[mod] == 0 and oldState.b[mod] != 0\
                or mod != 6 and oldN == 13:
            total = oldState.a[mod] + oldState.b[mod]
            res.a_fin += total
            res.a[mod] = 0
            res.b[mod] = 0

        # Calculate situation if one side does not have available action
        if all(v == 0 for v in res.a):
            bSum = sum(res.b)
            res.b = [0, 0, 0, 0, 0, 0]
            res.b_fin += bSum

        # Return true if landed on the kalah
        if mod == 6:
            return res, True

        # Otherwise return false
        return res, False

    def Max_Value(self, state, alpha, beta, depth):
        """
        Calculate max-value in the minimax algorithm with alpha-beta
        pruning

        Args:
            state (state): current state
            alpha (int): lower bound
            beta (int): upper bound_
            depth (int): remaining depth

        Returns:
            int, int: action index and calculated value
        """
        # Base case: Return the utility if it is a terminal
        if (self.Terminal_Test(state, depth)):
            return -1, self.utility(state)
        v = -math.inf
        maxA = -1

        for a, isKalah, s in self.successorForA(state):
            if not isKalah:
                # If not hit kalah, call min value and decrease the value
                act, val = self.Min_Value(s, alpha, beta, depth - 1)
                # Update value and action
                if val > v:
                    v = val
                    maxA = a
            else:
                # If hit kalah, call the max value again
                act, val = self.Max_Value(s, alpha, beta, depth)
                # Update value and action
                if val > v:
                    v = val
                    maxA = a

            # return the current action and value if v is not smaller than alpha
            if v >= beta:
                return a, v

            # Update alpha
            alpha = max(alpha, v)

        # Return the action and value
        return maxA, v

    def Min_Value(self, state, alpha, beta, depth):
        """
        Calculate max-value in the minimax algorithm with alpha-beta
        pruning

        Args:
            state (state): current state
            alpha (int): lower bound
            beta (int): upper bound_
            depth (int): remaining depth

        Returns:
            int, int: action index and calculated value
        """
        # Base case: Return the utility if it is a terminal
        if (self.Terminal_Test(state, depth)):
            return -1, self.utility(state)
        v = math.inf
        maxA = -1

        for a, isKalah, s in self.successorForB(state):
            if not isKalah:
                # If not hit kalah, call min value and decrease the value
                act, val = self.Max_Value(s, alpha, beta, depth - 1)
                # Update value and action
                if val < v:
                    v = val
                    maxA = a
            else:
                # If hit kalah, call the max value again
                act, val = self.Min_Value(s, alpha, beta, depth)
                # Update value and action
                if val < v:
                    v = val
                    maxA = a

            # return the current action and value if v is not smaller than alpha
            if v <= alpha:
                return a, v

            # Update alpha
            beta = min(beta, v)

        # Return the action and value
        return maxA, v

    def Terminal_Test(self, state: state, depth):
        """
        Return if the current state is a terminal

        Args:
            state (state): current state
            depth (int): remaining depth

        Returns:
            bool: If the current state is a terminal
        """
        # If the remaining depth is zero, return true
        if (depth == 0):
            return True

        # If there is no available action for either side, return true
        if all(v == 0 for v in state.a) or all(v == 0 for v in state.b):
            return True

        # If the game is over, return true
        if (state.a_fin > 36 or state.b_fin > 36
                or (state.a_fin == 36 and state.b_fin == 36)):
            return True

        # Otherwise, return false
        return False

    def utility(self, state: state):
        """
        Heuristic function for states

        Args:
            state (state): current state

        Returns:
            _type_: _description_
        """
        # If a wins, return infinity
        if (state.a_fin > 36):
            return math.inf

        # If b wins, return -infinity
        if (state.b_fin > 36):
            return -math.inf

        # Heuristic function
        res = sum(state.a) - sum(state.b) + \
            state.a_fin * 100 - state.b_fin * 100

        return res
