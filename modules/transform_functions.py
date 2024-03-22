import numpy as np
import cvxopt

def ttof_transform(t, data, data_type):

    N_t = t.size

    out_A = np.zeros((N_t, N_t+1))
    out_A[:,-1] = 1

    for p in range(0, N_t):
        for q in range(0, N_t):
            out_A[p, q] = np.exp(-t[p]/t[q])

    if data_type == 'Electric Modulus' or data_type == 'Admittance':
        for p in range(0, N_t):
            for q in range(0, N_t):
                out_A[p, q] = -out_A[p, q]


    lb = np.zeros([data.shape[0]+1])
    bound_mat = np.eye(lb.shape[0])

    # quadratic program
    H = 2*out_A.T@out_A
    H = (H.T+H)/2
    c = -2*(data.T@out_A)

    # DRT
    xm = cvxopt_solve_qpr(H, c, -bound_mat, lb)

    # frequency domain
    N_freq = N_t
    freq = 1/(t*2*np.pi)
    oA1 = np.zeros((N_freq,N_freq+1))
    oA2 = np.zeros((N_freq,N_freq+1))
    oA1[:,-1] = 1.
    oA2[:,-1] = 0

    for p in range(0, N_freq):
        for q in range(0, N_freq):
            oA1[p, q] = 1 /(1 +  (freq[p] / freq[q])**2)
            oA2[p, q] = (freq[p] / freq[q]) /(1 +  (freq[p] / freq[q])**2)

    if data_type == 'Electric Modulus' or data_type == 'Admittance':
        for p in range(0, N_freq):
            for q in range(0, N_freq):
                oA1[p, q] = -oA1[p, q]
                oA2[p, q] = -oA2[p, q]

    out_re = oA1@xm
    out_im = oA2@xm

    output = out_re + 1j*out_im

    return xm, output

def ftot_transform(freq, data, data_type, data_used):

    N_freq = freq.size
    data_re = data.real
    data_imag = data.imag

    oA1 = np.zeros((N_freq,N_freq+1))
    oA2 = np.zeros((N_freq,N_freq+1))
    oA1[:,-1] = 1
    oA2[:,-1] = 0

    if data_used == 'Complex Frequency to Time':
        for p in range(0, N_freq):
            for q in range(0, N_freq):
                oA1[p, q] = 1 /(1 +  (freq[p] / freq[q])**2)
                oA2[p, q] = (freq[p] / freq[q]) /(1 +  (freq[p] / freq[q])**2)

        if data_type == 'Electric Modulus' or data_type == 'Admittance':
            for p in range(0, N_freq):
                for q in range(0, N_freq):
                    oA1[p, q] = -oA1[p, q]
                    oA2[p, q] = -oA2[p, q]

        # quadratic program
        H = 2*(oA1.T@oA1 + oA2.T@oA2)
        H = (H.T+H)/2
        c = -2*(data_re.T@oA1 + data_imag.T@oA2)

        lb = np.zeros([data.shape[0]+1])

    bound_mat = np.eye(lb.shape[0])

    # DRT
    xm = cvxopt_solve_qpr(H, c, -bound_mat, lb)

    # time domain
    N_t = N_freq
    t = 1/(freq*2*np.pi)

    out_A = np.zeros((N_t, N_t+1))
    for p in range(0, N_t):
        for q in range(0, N_t):
            out_A[p, q] = np.exp(-t[p]/t[q])

    if data_type == 'Electric Modulus' or data_type == 'Admittance':
        for p in range(0, N_t):
            for q in range(0, N_t):
                out_A[p, q] = -out_A[p, q]
    
    out_A[:,-1] = 1.
    output = out_A@xm

    return xm, output

def cvxopt_solve_qpr(P, q, G=None, h=None, A=None, b=None):
    
    """
       This function uses cvxopt to minimize the quadratic problem 0.5*x^T*P*x + q^T*x under the constraints that G*x <= h (element-wise) and A*x = b. 
       Inputs: 
           P: matrix
           q: vector
           G: matrix
           h: vector
           A: matrix
           B: vector
       Output: 
           Vector solution of the aforementioned poblem
    """
    
    args = [cvxopt.matrix(P), cvxopt.matrix(q)]
    
    if G is not None: # in case the element-wise inequality constraint G*x <= b is included
    
        args.extend([cvxopt.matrix(G), cvxopt.matrix(h)])
        
    if A is not None: # in case the equality constraint A*x = b is included
    
         args.extend([cvxopt.matrix(A), cvxopt.matrix(b)])
        
    cvxopt.solvers.options['abstol'] = 1e-15
    cvxopt.solvers.options['reltol'] = 1e-15 ## could be 1e-15
    sol = cvxopt.solvers.qp(*args)
    
    if 'optimal' not in sol['status']:
        
        return None
    
    return np.array(sol['x']).reshape((P.shape[1],))
