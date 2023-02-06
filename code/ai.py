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
        #     # self.minimax(depth=d)
        #     f.write(str(time.time()-t_start)+'\n')
        # f.close()
        # print(r)
        # res = r[random.randint(0, len(r)-1)]
        # print(res)
        # return res

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
        d = 2
        f.write('depth = '+str(d)+'\n')
        t_start = time.time()
        a = self.minimax(depth=d)
        f.write(str(time.time()-t_start)+'\n')
        f.close()
        print(f"a: {a} r: {r}")
        res = a

        return res

    # calling function

    def minimax(self, depth):
        # example: doing nothing but wait 0.1*depth sec
        a, v = self.Max_Value(self.head, -math.inf, math.inf, depth)
        # print(f"v: {v}")
        return a

    def successorForA(self, state: state):
        r = []
        for i in range(6):
            if state.a[i] != 0:
                r.append(i)

        states = []
        for i in r:
            newState, isKalah = self.step(state, i)
            states.append((i, isKalah, newState))

        return states

    def successorForB(self, state: state):
        r = []
        for i in range(6):
            if state.b[::-1][i] != 0:
                r.append(i)

        states = []
        for i in r:
            newState, isKalah = self.step(self.state(
                state.b[::-1], state.a[::-1], state.b_fin, state.a_fin), i)
            states.append((i, isKalah, self.state(
                newState.b[::-1], newState.a[::-1], newState.b_fin, newState.a_fin)))

        return states

    def step(self, oldState: state, i):
        oldN = oldState.a[i]
        n = oldN
        res = self.state(oldState.a.copy(), oldState.b.copy(),
                         oldState.a_fin, oldState.b_fin)

        # print(f"i: {i} n: {n}")
        res.a[i] = 0
        i += 1
        mod = -1

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

        if mod == 6:
            return res, True

        print(f"mod {mod}")
        if mod < 6 and oldN < 13 and oldState.a[mod] == 0 and oldState.b[mod] != 0 or oldN == 13:
            # print(
            #     f"oldState.a: {oldState.a}  oldState.b: {oldState.b}  mod: {mod}  oldN: {oldN}")

            sum = oldState.a[mod] + oldState.b[mod]
            res.a_fin += sum
            res.a[mod] = 0
            res.b[mod] = 0

        # print(f"res: {res}")

        return res, False

    def Max_Value(self, state, alpha, beta, depth):
        print(
            f"Max_Value: a: {state.a} b:{state.b} alpha: {alpha} beta: {beta} depth:{depth}")
        if (self.Terminal_Test(state, depth)):
            # print(
            #     f"Max: a: {state.a} b:{state.b} utility: {self.utility(state, True)}")
            return -1, self.utility(state, True)
        v = -math.inf
        maxA = -1

        for a, isKalah, s in self.successorForA(state):
            if not isKalah:
                act, val = self.Min_Value(s, alpha, beta, depth - 1)
                # if val > v:
                #     v = val
                #     maxA = a
                v = max(v, val)
            else:
                act, val = self.Max_Value(s, alpha, beta, depth - 1)
                v = max(v, val)

            if v >= beta:
                # print(f"Max a: {a} v:{v} beta:{beta}")
                return a, v

            alpha = max(alpha, v)
        # print("return -1")
        return -1, v

    def Min_Value(self, state, alpha, beta, depth):
        print(
            f"Min_Value: a: {state.a} b:{state.b} alpha: {alpha} beta: {beta} depth:{depth}")
        if (self.Terminal_Test(state, depth)):
            # print(
            #     f"Min: a: {state.a} b:{state.b} utility: {self.utility(state, False)}")
            return -1, self.utility(state, False)
        v = math.inf

        for a, isKalah, s in self.successorForB(state):
            if not isKalah:
                act, val = self.Max_Value(s, alpha, beta, depth - 1)
                v = max(v, val)
            else:
                act, val = self.Min_Value(s, alpha, beta, depth - 1)
                v = max(v, val)

            if v <= alpha:
                # print(f"Min a: {a} v:{v}")
                return a, v

            beta = min(beta, v)
        # print("return -1")
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
        # if (state == None):
        #     if isMax:
        #         return -math.inf
        #     else:
        #         return math.inf

        if (state.a_fin > 36):
            return math.inf

        if (state.b_fin > 36):
            return -math.inf

        res = sum(state.a) - sum(state.b) + state.a_fin * 2 - state.b_fin * 2

        return res


if __name__ == "__main__":
    myAI = ai()
    # print(myAI.move([0, 1, 0, 2, 12, 11], [1, 0, 2, 0, 13, 0], 16, 14, 1))
    # myState = myAI.state([11, 0, 0, 1, 16, 1], [11, 0, 1, 3, 3, 1], 16, 8)

    # successor = myAI.successor(myState)
    # for s in successor:
    #     print(s[2])

    # myState = myAI.state([0, 13, 0, 0, 0, 0], [11, 12, 2, 0, 0, 0], 17, 17)
    # print(myAI.successorForA(myState)[0][2].a,
    #       myAI.successorForA(myState)[0][2].b)

    #  print(myAI.Min_Value([0, 0, 0, 2, 12, 11], [1, 0, 0, 0, 13, 0], 16, 17))

    print(myAI.move([0, 13, 0, 0, 0, 0], [11, 12, 2, 0, 0, 0], 17, 17, 1))
