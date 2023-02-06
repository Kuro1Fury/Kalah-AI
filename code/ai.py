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
        self.head = self.state(a, b, a_fin, b_fin)

        # # For test only: return a random move
        # r = []
        # for i in range(6):
        #     if a[i] != 0:
        #         r.append(i)
        # # To test the execution time, use time and file modules
        # # In your experiments, you can try different depth, for example:
        # # append to time.txt so that you can see running time for all moves.
        # f = open('time.txt', 'a')
        # # Make sure to clean the file before each of your experiment
        # for d in [3, 5, 7]:  # You should try more
        #     f.write('depth = '+str(d)+'\n')
        #     t_start = time.time()
        #     self.minimax(depth=d)
        #     f.write(str(time.time()-t_start)+'\n')
        # f.close()
        # print(r)
        # res = r[random.randint(0, len(r)-1)]
        # print(res)
        # # return res
        # # return r[random.randint(0, len(r)-1)]
        # # But remember in your final version you should choose only one depth according to your CPU speed (TA's is 3.4GHz)
        # # and remove timing code.

        # Comment all the code above and start your code here

        # For test only: return a random move
        r = []
        for i in range(6):
            if a[i] != 0:
                r.append(i)
        # To test the execution time, use time and file modules
        # In your experiments, you can try different depth, for example:
        # append to time.txt so that you can see running time for all moves.
        f = open('time.txt', 'a')
        # Make sure to clean the file before each of your experiment
        d = 10
        f.write('depth = '+str(d)+'\n')
        t_start = time.time()
        a = self.minimax(depth=d)
        f.write(str(time.time()-t_start)+'\n')
        f.close()
        res = r[a]
        print(f"a: {a} r[a]: {r[a]} r: {r}")
        return res
        # return res
        # return r[random.randint(0, len(r)-1)]
        # But remember in your final version you should choose only one depth according to your CPU speed (TA's is 3.4GHz)
        # and remove timing code.

    # calling function

    def minimax(self, depth):
        # example: doing nothing but wait 0.1*depth sec
        a, v = self.Max_Value(self.head, -math.inf, math.inf, depth)
        return a

    def successor(self, state: state) -> tuple:
        r = []
        for i in range(6):
            if state.a[i] != 0:
                r.append(i)

        states = []
        for i in range(len(r)):
            newState, isKalah = self.step(state, i)
            states.append((i, isKalah, newState))

        return states

    def step(self, oldState: state, i):
        oldN = oldState.a[i]
        n = oldN
        res = self.state(oldState.a, oldState.b,
                         oldState.a_fin, oldState.b_fin)

        mod = i % 13

        while n > 0:
            if mod == 6:
                res.a_fin += 1
            elif i % 13 < 6:
                res.a[mod] += 1
            else:
                res.b[12 - (mod)] += 1
            n -= 1
            i += 1
            mod = i % 13

        isKalah = False
        if mod == 6:
            isKalah = True

        if mod < 6 and oldN < 13 and oldState.a[mod] == 0 or oldN == 13:
            if (oldState.b[mod]) != 0:
                sum = oldState.a[mod] + oldState.b[mod]
                res.a_fin += sum
                res.a[mod] = 0
                res.b[mod] = 0

        return res, isKalah

    def Max_Value(self, state, alpha, beta, depth) -> tuple:
        if (self.Terminal_Test(state, depth)):
            return -1, self.utility(state, True)
        v = -math.inf

        for a, isKalah, s in self.successor(state):
            if not isKalah:
                act, val = self.Min_Value(s, alpha, beta, depth - 1)
                v = max(v, val)
            else:
                act, val = self.Max_Value(s, alpha, beta, depth - 1)
                v = max(v, val)

            if v >= beta:
                return a, v

            alpha = max(alpha, v)

        return -1, v

    def Min_Value(self, state, alpha, beta, depth) -> tuple:
        if (self.Terminal_Test(state, depth)):
            return -1, self.utility(state, False)
        v = math.inf

        for a, isKalah, s in self.successor(state):
            if not isKalah:
                act, val = self.Max_Value(s, alpha, beta, depth - 1)
                v = max(v, val)
            else:
                act, val = self.Min_Value(s, alpha, beta, depth - 1)
                v = max(v, val)

            if v <= alpha:
                return a, v

            beta = min(beta, v)

        return -1, v

    def Terminal_Test(self, state: state, depth):
        if (depth == 0):
            return True

        if all(v == 0 for v in state.a) or all(v == 0 for v in state.b):
            return True

        if (state.a_fin > 36 or state.b_fin > 36):
            return True

        return False

    def utility(self, state: state, isMax):
        if (state == None):
            if isMax:
                return -math.inf
            else:
                return math.inf

        if (state.a_fin > 36):
            return math.inf

        if (state.b_fin > 36):
            return -math.inf

        return sum(state.a) - sum(state.b) + state.a_fin * 2 - state.b_fin * 2
