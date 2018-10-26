import numpy as np


class HmmMethods:

    @staticmethod
    def viterbi(pi, a, b, obs):
        nStates = np.shape(b)[0]
        T = np.shape(obs)[0]

        path = np.zeros(T)
        delta = np.zeros((nStates, T))
        phi = np.zeros((nStates, T))

        delta[:, 0] = pi * b[:, obs[0]]
        phi[:, 0] = 0

        for t in range(1, T):
            for s in range(nStates):
                delta[s, t] = np.max(delta[:, t - 1] * a[:, s]) * b[s, obs[t]]
                phi[s, t] = np.argmax(delta[:, t - 1] * a[:, s])

        path[T - 1] = np.argmax(delta[:, T - 1])
        for t in range(T - 2, -1, -1):
            # path[t] = phi[int(path[t+1]): int(t+1) , int(t+1)]
            path[t] = phi[int(path[t + 1]), int(t + 1)]

        return path, delta, phi

    @staticmethod
    def viterbi_log(pi, a, b, obs):

        a_log = np.log2(a)
        b_log = np.log2(b)
        pi_log = np.log2(pi)

        nStates = np.shape(b)[0]
        T = np.shape(obs)[0]

        path = np.zeros(T)
        delta = np.zeros((nStates, T))
        phi = np.zeros((nStates, T))

        delta[:, 0] = pi_log + b_log[:, obs[0]]
        phi[:, 0] = 0

        for t in range(1, T):
            for s in range(nStates):
                delta[s, t] = np.max(delta[:, t - 1] + a_log[:, s]) + b_log[s, obs[t]]
                phi[s, t] = np.argmax(delta[:, t - 1] + a_log[:, s])

        path[T - 1] = np.argmax(delta[:, T - 1])
        for t in range(T - 2, -1, -1):
            # path[t] = phi[int(path[t+1]): int(t+1) , int(t+1)]
            path[t] = phi[int(path[t + 1]), int(t + 1)]

        return path, delta, phi

    @staticmethod
    def baumWelch(o, N, dirichlet=False, verbose=False, rand_seed=1):
        # Implements HMM Baum-Welch algorithm

        # Params to change
        tolerance = 1e-6
        max_iter = 10000

        T = np.shape(o)[0]

        M = int(
            max(o)) + 1  # now all hist time-series will contain all observation vals, but we have to provide for all

        digamma = np.zeros((N, N, T))

        # Initialise A, B and pi randomly, but so that they sum to one
        np.random.seed(rand_seed)

        # Initialisation can be done either using dirichlet distribution (all randoms sum to one)
        # or using approximates uniforms from matrix sizes
        if dirichlet:
            pi = np.ndarray.flatten(np.random.dirichlet(np.ones(N), size=1))

            a = np.random.dirichlet(np.ones(N), size=N)

            b = np.random.dirichlet(np.ones(M), size=N)
        else:

            pi_randomizer = np.ndarray.flatten(np.random.dirichlet(np.ones(N), size=1)) / 100
            pi = 1.0 / N * np.ones(N) - pi_randomizer

            a_randomizer = np.random.dirichlet(np.ones(N), size=N) / 100
            a = 1.0 / N * np.ones([N, N]) - a_randomizer

            b_randomizer = np.random.dirichlet(np.ones(M), size=N) / 100
            b = 1.0 / M * np.ones([N, M]) - b_randomizer

        error = tolerance + 10
        itter = 0
        while (error > tolerance) & (itter < max_iter):

            prev_a = a.copy()
            prev_b = b.copy()

            # Estimate model parameters
            alpha, c = HmmMethods.forward(a, b, o, pi)
            beta = HmmMethods.backward(a, b, o, c)

            for t in range(T - 1):
                for i in range(N):
                    for j in range(N):
                        digamma[i, j, t] = alpha[i, t] * a[i, j] * b[j, o[t + 1]] * beta[j, t + 1]
                digamma[:, :, t] /= np.sum(digamma[:, :, t])

            for i in range(N):
                for j in range(N):
                    digamma[i, j, T - 1] = alpha[i, T - 1] * a[i, j]
            digamma[:, :, T - 1] /= np.sum(digamma[:, :, T - 1])

            # Maximize parameter expectation
            for i in range(N):
                pi[i] = np.sum(digamma[i, :, 0])
                for j in range(N):
                    a[i, j] = np.sum(digamma[i, j, :T - 1]) / np.sum(digamma[i, :, :T - 1])

                for k in range(M):
                    filter_vals = (o == k).nonzero()
                    b[i, k] = np.sum(digamma[i, :, filter_vals]) / np.sum(digamma[i, :, :])

            error = (np.abs(a - prev_a)).max() + (np.abs(b - prev_b)).max()
            itter += 1

            if verbose:
                print("Iteration: ", itter, " error: ", error, "P(O|lambda): ", np.sum(alpha[:, T - 1]))

        return a, b, pi, alpha

    @staticmethod
    def forward(a, b, o, pi):
        # Implements HMM Forward algorithm

        # Params to change
        scaling = True

        N = np.shape(b)[0]
        T = np.shape(o)[0]

        alpha = np.zeros((N, T))
        # initialise first column with observation values
        alpha[:, 0] = pi * b[:, o[0]]
        c = np.ones((T))

        if scaling:

            c[0] = 1.0 / np.sum(alpha[:, 0])
            alpha[:, 0] = alpha[:, 0] * c[0]

            for t in range(1, T):
                c[t] = 0
                for i in range(N):
                    alpha[i, t] = b[i, o[t]] * np.sum(alpha[:, t - 1] * a[:, i])
                c[t] = 1.0 / np.sum(alpha[:, t])
                alpha[:, t] = alpha[:, t] * c[t]

        else:
            for t in range(1, T):
                for i in range(N):
                    alpha[i, t] = b[i, o[t]] * np.sum(alpha[:, t - 1] * a[:, i])

        return alpha, c

    @staticmethod
    def backward(a, b, o, c):
        # Implements HMM Backward algorithm

        N = np.shape(b)[0]
        T = np.shape(o)[0]

        beta = np.zeros((N, T))
        # initialise last row with scaling c
        beta[:, T - 1] = c[T - 1]

        for t in range(T - 2, -1, -1):
            for i in range(N):
                beta[i, t] = np.sum(b[:, o[t + 1]] * beta[:, t + 1] * a[i, :])
            # scale beta by the same value as a
            beta[:, t] = beta[:, t] * c[t]

        return beta
