import numpy as np
from numpy import exp
from math import pi, log, sqrt
from scipy import integrate
from scipy.optimize import fsolve
from scipy.linalg import toeplitz
import cvxpy as cp
import cvxopt

def simple_run(entry, rbf_type = 'Gaussian', data_used = 'Complex Data', induct_used = 1, der_used = '1st order', shape_control = 'FWHM Coefficient', coeff = 0.5, lambda_0=0.001, data_type=None):
    
    """
    This function enables to compute the DRT using ridge regression (also known as Tikhonov regression)
    Inputs:
        entry: an EIS spectrum
        rbf_type: discretization function
        data_used: part of the EIS spectrum used for regularization
        induct_used: treatment of the inductance part
        der_used: order of the derivative considered for the M matrix
        shape_control: option for controlling the shape of the radial basis function (RBF) 
        coeff: magnitude of the shape control
    """
    
    # Step 1: define the matrices
    
    # Step 1.1: define the optimization bounds
    N_freqs = entry.freq.shape[0]
    N_taus = entry.tau.shape[0]

    entry.b_re = entry.Z_exp.real
    entry.b_im = entry.Z_exp.imag
    
    # Step 1.2: compute epsilon
    entry.epsilon = compute_epsilon(entry.freq, coeff, rbf_type, shape_control)
    
    # Step 1.3: compute A matrix
    entry.A_re_temp = assemble_A_re(entry.freq, entry.tau, entry.epsilon, rbf_type, flag1='simple', flag2='impedance', data_type=data_type)
    entry.A_im_temp = assemble_A_im(entry.freq, entry.tau, entry.epsilon, rbf_type, flag1='simple', flag2='impedance', data_type=data_type)
    
    # Step 1.4: compute M matrix
    if der_used == '1st order':
        entry.M_temp = assemble_M_1(entry.tau, entry.epsilon, rbf_type, flag='simple')
    elif der_used == '2nd order':
        entry.M_temp = assemble_M_2(entry.tau, entry.epsilon, rbf_type, flag='simple')
    
    # Step 2: conduct ridge regularization
    if data_used == 'Complex Data': # select both parts of the impedance for the simple run

        if induct_used == 0 or induct_used == 3 or induct_used == 4: # without considering the inductance
            
            N_RL = 1 # N_RL length of resistance plus inductance
            entry.A_re = np.zeros((N_freqs, N_taus+N_RL))
            entry.A_re[:,N_RL:] = entry.A_re_temp
            if induct_used == 0:
                entry.A_re[:,0] = 1
            elif induct_used == 3:
                entry.A_re[:,0] = -(2*pi*entry.freq)**2
            elif induct_used == 4:
                entry.A_re[:,0] = -(2*pi*entry.freq)**-2
            
            entry.A_im = np.zeros((N_freqs, N_taus+N_RL))
            entry.A_im[:,N_RL:] = entry.A_im_temp
            
            entry.M = np.zeros((N_taus+N_RL, N_taus+N_RL))
            entry.M[N_RL:,N_RL:] = entry.M_temp
            lb = np.zeros([entry.b_re.shape[0]+1])

        elif induct_used == 1 or induct_used == 2: #considering the inductance/capacitance
            N_RL = 2
            entry.A_re = np.zeros((N_freqs, N_taus+N_RL))
            entry.A_re[:, N_RL:] = entry.A_re_temp
            entry.A_re[:,1] = 1
            
            entry.A_im = np.zeros((N_freqs, N_taus+N_RL))
            entry.A_im[:, N_RL:] = entry.A_im_temp
            if induct_used == 1:
                entry.A_im[:,0] = 2*pi*entry.freq
            elif induct_used ==2:
                entry.A_im[:,0] = (2*pi*entry.freq)**-1

            entry.M = np.zeros((N_taus+N_RL, N_taus+N_RL))
            entry.M[N_RL:,N_RL:] = entry.M_temp
            lb = np.zeros([entry.b_re.shape[0]+2])
        
        # optimally select the regularization level
        #log_lambda_0 = log(lambda_0) # initial guess for lambda
        #lambda_value = optimal_lambda(entry.A_re, entry.A_im, entry.b_re, entry.b_im, entry.M, log_lambda_0, cv_type) 
        lambda_value = lambda_0
        print(lambda_value)
        # non-negativity constraint on the DRT gmma
        bound_mat = np.eye(lb.shape[0])
        print(bound_mat)

        # recover the DRT using cvxpy or cvxopt if cvxpy fails
        H_combined,c_combined = quad_format_combined(entry.A_re, entry.A_im, entry.b_re, entry.b_im, entry.M, lambda_value)
        try:
            x = cvxpy_solve_qp(H_combined, c_combined, -bound_mat, lb) # using cvxpy
        except:
            x = cvxopt_solve_qpr(H_combined, c_combined, -bound_mat, lb) # using cvxopt
    
        # prepare for output
        entry.mu_Z_re = entry.A_re@x
        entry.mu_Z_im = entry.A_im@x
        entry.res_re = entry.mu_Z_re-entry.b_re
        entry.res_im = entry.mu_Z_im-entry.b_im
        
    elif data_used == 'Imaginary Part Data': # select the imaginary part of the impedance for the simple run
        
        if induct_used == 0 or induct_used == 3 or induct_used == 4: # without considering the inductance
            N_RL = 0 # N_RL length of resistance plus inductance
            entry.A_re = np.zeros((N_freqs, N_taus+N_RL))
            entry.A_re[:, N_RL:] = entry.A_re_temp
            
            entry.A_im = np.zeros((N_freqs, N_taus+N_RL))
            entry.A_im[:, N_RL:] = entry.A_im_temp
            
            entry.M = np.zeros((N_taus+N_RL, N_taus+N_RL))
            entry.M[N_RL:,N_RL:] = entry.M_temp
            lb = np.zeros([entry.b_re.shape[0]])        
        
        elif induct_used == 1 or induct_used ==2: # considering the inductance
            N_RL = 1
            entry.A_re = np.zeros((N_freqs, N_taus+N_RL))
            entry.A_re[:, N_RL:] = entry.A_re_temp
            
            entry.A_im = np.zeros((N_freqs, N_taus+N_RL))
            entry.A_im[:, N_RL:] = entry.A_im_temp
            if induct_used == 1:
                entry.A_im[:,0] = 2*pi*entry.freq
            elif induct_used == 2:
                entry.A_im[:,0] = (2*pi*entry.freq)**-1
            
            entry.M = np.zeros((N_taus+N_RL, N_taus+N_RL))
            entry.M[N_RL:,N_RL:] = entry.M_temp
            lb = np.zeros([entry.b_re.shape[0]+1])

        # optimally select the regularization level
        #log_lambda_0 = log(lambda_0) # initial guess for lambda
        #lambda_value = optimal_lambda(entry.A_re, entry.A_im, entry.b_re, entry.b_im, entry.M, log_lambda_0, cv_type) 
        lambda_value = lambda_0
        # non-negativity constraint on the DRT gmma
        # + 1 if a resistor or an inductor is included in the DRT model
        bound_mat = np.eye(lb.shape[0])

        # recover the DRT using cvxpy or cvxopt if cvxpy fails
        H_im, c_im = quad_format_separate(entry.A_im, entry.b_im, entry.M, lambda_value)
        try:
            x = cvxpy_solve_qp(H_im, c_im) # using cvxpy
        except:
            x = cvxopt_solve_qpr(H_im, c_im, -bound_mat, lb) # using cvxopt
        
        # prepare for HMC sampler
        entry.mu_Z_re = entry.A_re@x
        entry.mu_Z_im = entry.A_im@x
        entry.res_re = entry.mu_Z_re-entry.b_re
        entry.res_im = entry.mu_Z_im-entry.b_im
    
    elif data_used == 'Real Part Data': # select the real part of the impedance for the simple run

        N_RL = 1
        entry.A_re = np.zeros((N_freqs, N_taus+N_RL))
        entry.A_re[:, N_RL:] = entry.A_re_temp
        if induct_used == 0:
            entry.A_re[:,0] = 1
        elif induct_used == 3:
            entry.A_re[:,0] = -(2*pi*entry.freq)**2
        elif induct_used == 4:
            entry.A_re[:,0] = -(2*pi*entry.freq)**-2
        
        entry.A_im = np.zeros((N_freqs, N_taus+N_RL))
        entry.A_im[:, N_RL:] = entry.A_im_temp

        entry.M = np.zeros((N_taus+N_RL, N_taus+N_RL))
        entry.M[N_RL:,N_RL:] = entry.M_temp
        
        # optimally select the regularization level
        log_lambda_0 = log(lambda_0) # initial guess for lambda
        #lambda_value = optimal_lambda(entry.A_re, entry.A_im, entry.b_re, entry.b_im, entry.M, log_lambda_0, cv_type) 
        lambda_value = lambda_0
        # non-negativity constraint on the DRT gmma
        lb = np.zeros([entry.b_re.shape[0]+1]) # + 1 if a resistor or an inductor is included in the DRT model
        bound_mat = np.eye(lb.shape[0])

        # recover the DRT using cvxpy or cvxopt if cvxpy fails
        H_re,c_re = quad_format_separate(entry.A_re, entry.b_re, entry.M, lambda_value)
        try:
            x = cvxpy_solve_qp(H_re, c_re) # using cvxpy
        except:
            x = cvxopt_solve_qpr(H_re, c_re, -bound_mat, lb) # using cvxopt
        
        # prepare for output
        entry.mu_Z_re = entry.A_re@x
        entry.mu_Z_im = entry.A_im@x
        entry.res_re = entry.mu_Z_re-entry.b_re
        entry.res_im = entry.mu_Z_im-entry.b_im
    
    # Step 3: obtaining the result of inductance, resistance, and gamma  
    if N_RL == 0: 
        entry.L, entry.R = 0, 0        
    elif N_RL == 1 and data_used == 'Imaginary Part Data':
        entry.L, entry.R = x[0], 0    
    elif N_RL == 1 and data_used != 'Imaginary Part Data':
        entry.L, entry.R = 0, x[0]
    elif N_RL == 2:
        entry.L, entry.R = x[0:2]
    
    entry.x = x[N_RL:]
    entry.out_tau_vec, entry.gamma = x_to_gamma(x[N_RL:], entry.tau_fine, entry.tau, entry.epsilon, rbf_type)
    entry.N_RL = N_RL 
    entry.method = 'simple'
    
    return entry

class EIS_object(object):
    
    # The EIS_object class stores the input data and the DRT result.
      
    def __init__(self, freq, Z_prime, Z_double_prime):
        
        """
        This function define an EIS_object.
        Inputs:
            freq: frequency of the EIS measurement
            Z_prime: real part of the impedance
            Z_double_prime: imaginery part of the impedance
        """
        
        # define an EIS_object
        self.freq = freq
        self.Z_prime = Z_prime
        self.Z_double_prime = Z_double_prime
        self.Z_exp = Z_prime + 1j*Z_double_prime
        
        # keep a copy of the original data
        self.freq_0 = freq
        self.Z_prime_0 = Z_prime
        self.Z_double_prime_0 = Z_double_prime
        self.Z_exp_0 = Z_prime + 1j*Z_double_prime
        
        self.tau = 1/freq # we assume that the collocation points equal to 1/freq as default
        self.tau_fine  = np.logspace(np.log10(self.tau.min())-0.5,np.log10(self.tau.max())+0.5,10*freq.shape[0])            
        print(self.tau)
        print(self.tau_fine)
        print(self.tau.size)
        print(self.tau_fine.size)
        self.method = 'none'

def g_i(freq_n, tau_m, epsilon):
    
    """ 
       This function generates the elements of A_re for the radial-basis-function (RBF) expansion
       Inputs: 
            freq_n: frequency
            tau_m: log timescale (log(1/freq_m))
            epsilon : shape factor of radial basis functions used for discretization
            rbf_type: selected RBF type
       Outputs:
            Elements of A_re for the RBF expansion
    """
    
    alpha = 2*pi*freq_n*tau_m  

    rbf = lambda x: exp(-(epsilon*x)**2)
    integrand_g_i = lambda x: 1./(1.+(alpha**2)*exp(2.*x))*rbf(x) # see equation (32) in [1]
    out_val = integrate.quad(integrand_g_i, -50, 50, epsabs=1E-9, epsrel=1E-9)
    
    return out_val[0]


def g_ii(freq_n, tau_m, epsilon):
    
    """
       This function generates the elements of A_im for RBF expansion
       Inputs:
           freq_n :frequency
           tau_m : log timescale (log(1/freq_m))
           epsilon  : shape factor of radial basis functions used for discretization
           rbf_type : selected RBF type    
       Outputs:
           Elements of A_im for the RBF expansion
    """ 
    
    alpha = 2*pi*freq_n*tau_m  

    rbf = lambda x: exp(-(epsilon*x)**2)

    integrand_g_ii = lambda x: alpha/(1./exp(x)+(alpha**2)*exp(x))*rbf(x) # see (33) in [1]
    out_val = integrate.quad(integrand_g_ii, -50, 50, epsabs=1E-9, epsrel=1E-9)
    
    return out_val[0]

def compute_epsilon(freq, coeff, rbf_type, shape_control): 
    
    """
       This function is used to compute epsilon, i.e., the shape factor of the radial basis functions used for discretization. 
       Inputs:
            freq: frequency
            coeff: scalar such that the full width at half maximum (FWHM) of the RBF is equal to 1/coeff times the average relaxation time spacing in logarithm scale
            rbf_type: selected RBF type 
            shape_control: shape of the RBF, which is set with either the coefficient, or with the option "shape factor" through the shape factor 𝜇
       Output: 
           epsilon (shape factor of radial basis functions used for discretization)
    """ 
    
    N_freq = freq.shape[0]
    
    if rbf_type == 'Piecewise Linear':
        return 0

    rbf = lambda x: exp(-(x)**2)-0.5
    
    if shape_control == 'FWHM Coefficient': # equivalent as the 'FWHM Coefficient' option in the Matlab code
    
        FWHM_coeff = 2*fsolve(rbf,1)[0]
        delta = np.mean(np.diff(np.log(1/freq.reshape(N_freq)))) # see (13) in [1]
        epsilon = coeff*FWHM_coeff/delta
        
    else: # equivalent as the 'Shape Factor' option in the Matlab code
    
        epsilon = coeff
    
    return epsilon

# Approximation matrix of the DRT for the real and imaginary parts of the EIS data

def inner_prod_rbf_1(freq_n, freq_m, epsilon):
    
    """ 
       This function computes the inner product of the first derivatives of the RBFs with respect to tau_n=log(1/freq_n) and tau_m = log(1/freq_m)
       Inputs: 
           freq_n: frequency
           freq_m: frequency 
           epsilon: shape factor 
           rbf_type: selected RBF type
       Outputs: 
           norm of the first derivative of the RBFs with respect to log(1/freq_n) and log(1/freq_m)
    """  
    
    a = epsilon*np.log(freq_n/freq_m)


    out_val = -epsilon*(-1+a**2)*np.exp(-(a**2/2))*np.sqrt(np.pi/2)
        
    return out_val

def inner_prod_rbf_2(freq_n, freq_m, epsilon):
    
    """ 
       This function computes the inner product of the second derivatives of the RBFs with respect to tau_n=log(1/freq_n) and tau_m = log(1/freq_m)
       Inputs: 
           freq_n: frequency
           freq_m: frequency 
           epsilon: shape factor 
           rbf_type: selected RBF type
       Outputs: 
           norm of the second derivative of the RBFs with respect to log(1/freq_n) and log(1/freq_m)
    """    
    
    a = epsilon*np.log(freq_n/freq_m)

    out_val = epsilon**3*(3-6*a**2+a**4)*np.exp(-(a**2/2))*np.sqrt(np.pi/2)
        
    return out_val

def gamma_to_x(gamma_vec, tau_vec, epsilon, rbf_type):
    
    """  
       This function maps the gamma_vec back to the x vector (x = gamma for piecewise linear functions) 
       Inputs:
            gamma_vec : DRT vector
            tau_vec : vector of log timescales (tau = log(1/frequency))
            epsilon: shape factor 
            rbf_type: selected RBF type
       Outputs:
            x_vec obtained by mapping gamma_vec to x = gamma
    """  
    
    if rbf_type == 'Piecewise Linear':
        x_vec = gamma_vec
        
    elif rbf_type == 'Gaussian':
        rbf = lambda x: np.exp(-(epsilon*x)**2)

        N_taus = tau_vec.size
        B = np.zeros([N_taus, N_taus])
        
        for p in range(0, N_taus):
            for q in range(0, N_taus):
                delta_log_tau = np.log(tau_vec[p])-np.log(tau_vec[q])
                B[p,q] = rbf(delta_log_tau)
                
        B = 0.5*(B+B.T)
                
        x_vec = np.linalg.solve(B, gamma_vec)
            
    return x_vec

def x_to_gamma(x_vec, tau_map_vec, tau_vec, epsilon, rbf_type): 
    
    """  
       This function maps the x vector to the gamma_vec
       Inputs:
            x_vec : the DRT vector obtained by mapping gamma_vec to x
            tau_map_vec : log(1/frequency) vector mapping x_vec to gamma_vec
            tau_vec : log(1/frequency) vector
            epsilon: shape factor 
            rbf_type: selected RBF type
       Outputs: 
            tau_vec and gamma_vec obtained by mapping x to gamma
    """
    
    if rbf_type == 'Piecewise Linear':
        gamma_vec = x_vec
        out_tau_vec = tau_vec

    elif rbf_type == 'Guassian':
        
        rbf = lambda x: np.exp(-(epsilon*x)**2)
        
        N_taus = tau_vec.size
        N_tau_map = tau_map_vec.size
        gamma_vec = np.zeros([N_tau_map, 1])

        B = np.zeros([N_tau_map, N_taus])
        
        for p in range(0, N_tau_map):
            for q in range(0, N_taus):
                delta_log_tau = np.log(tau_map_vec[p])-np.log(tau_vec[q])
                B[p,q] = rbf(delta_log_tau)              
                
        gamma_vec = B@x_vec
        out_tau_vec = tau_map_vec 
        
    return out_tau_vec, gamma_vec

def assemble_A_re(freq_vec, tau_vec, epsilon, rbf_type, flag1='simple', flag2='impedance', data_type=None):
    
    """
       This function computes the discretization matrix, A_re, for the real part of the impedance
       Inputs:
            freq_vec: vector of frequencies
            tau_vec: vector of timescales
            epsilon: shape factor 
            rbf_type: selected RBF type
            flag1: nature of the run, i.e.i, Simple or BHT run
            flag2: nature of the data, i.e., impedance or admittance, for the BHT run
       Output: 
            Approximation matrix A_re
    """    
    
    # compute omega and the number of frequencies and timescales tau
    omega_vec = 2.*np.pi*freq_vec
    N_freqs = freq_vec.size
    N_taus = tau_vec.size
    
    if flag1 == 'simple':
        
        # define the A_re output matrix
        out_A_re = np.zeros((N_freqs, N_taus))
    
        # check if the frequencies are sufficiently log spaced
        std_diff_freq = np.std(np.diff(np.log(1/freq_vec)))
        mean_diff_freq = np.mean(np.diff(np.log(1/freq_vec)))
    
        # check if the frequencies are sufficiently log spaced and that N_freqs = N_taus
        toeplitz_trick = std_diff_freq/mean_diff_freq<0.01 and N_freqs == N_taus 

        if toeplitz_trick and rbf_type != 'Piecewise Linear': # use toeplitz trick
            
            R = np.zeros(N_taus)
            C = np.zeros(N_freqs)
        
            for p in range(0, N_freqs):
            
                C[p] = g_i(freq_vec[p], tau_vec[0], epsilon)
        
            for q in range(0, N_taus):
            
                R[q] = g_i(freq_vec[0], tau_vec[q], epsilon)
                        
            out_A_re= toeplitz(C,R) 

        else: # use brute force
            
            for p in range(0, N_freqs):
                for q in range(0, N_taus):
            
                    if rbf_type == 'Piecewise Linear':  # see (A.3a) and (A.4) in [2]              
                        if q == 0:
                            out_A_re[p, q] = 0.5/(1+(omega_vec[p]*tau_vec[q])**2)*np.log(tau_vec[q+1]/tau_vec[q])
                        elif q == N_taus-1:
                            out_A_re[p, q] = 0.5/(1+(omega_vec[p]*tau_vec[q])**2)*np.log(tau_vec[q]/tau_vec[q-1])
                        else:
                            out_A_re[p, q] = 0.5/(1+(omega_vec[p]*tau_vec[q])**2)*np.log(tau_vec[q+1]/tau_vec[q-1])           
                
                    else:
                        out_A_re[p, q]= g_i(freq_vec[p], tau_vec[q], epsilon)
    
    else: # BHT run
    
        out_A_re = np.zeros((N_freqs, N_taus+1))
        out_A_re[:,0] = 1.
        
        if flag2 == 'impedance': # for the impedance calculations
        
            for p in range(0, N_freqs):
                for q in range(0, N_taus): # see (11a) in [3]
                    if q == 0:
                        out_A_re[p, q+1] = 0.5/(1+(omega_vec[p]*tau_vec[q])**2)*np.log(tau_vec[q+1]/tau_vec[q])
                    elif q == N_taus-1:
                        out_A_re[p, q+1] = 0.5/(1+(omega_vec[p]*tau_vec[q])**2)*np.log(tau_vec[q]/tau_vec[q-1])
                    else:
                        out_A_re[p, q+1] = 0.5/(1+(omega_vec[p]*tau_vec[q])**2)*np.log(tau_vec[q+1]/tau_vec[q-1])
        
        else: # for the admittance calculations
        
            for p in range(0, N_freqs):
                for q in range(0, N_taus): # see (16a) in the supplementary information (SI) of [3]
                    if q == 0:
                        out_A_re[p, q+1] = 0.5*(omega_vec[p]**2*tau_vec[q])/(1+(omega_vec[p]*tau_vec[q])**2)*np.log(tau_vec[q+1]/tau_vec[q])
                    elif q == N_taus-1:
                        out_A_re[p, q+1] = 0.5*(omega_vec[p]**2*tau_vec[q])/(1+(omega_vec[p]*tau_vec[q])**2)*np.log(tau_vec[q]/tau_vec[q-1])
                    else:
                        out_A_re[p, q+1] = 0.5*(omega_vec[p]**2*tau_vec[q])/(1+(omega_vec[p]*tau_vec[q])**2)*np.log(tau_vec[q+1]/tau_vec[q-1])

    if data_type == 'Electric Modulus' or data_type == 'Admittance':
        for p in range(0, N_freqs):
            for q in range(0, N_taus):
                out_A_re[p, q] = -out_A_re[p, q]

    return out_A_re

def assemble_A_im(freq_vec, tau_vec, epsilon, rbf_type, flag1='simple', flag2='impedance', data_type=None):
    
    """
       This function computes the discretization matrix, A_im, for the imaginary part of the impedance
       Inputs:
            freq_vec: vector of frequencies
            tau_vec: vector of timescales
            epsilon: shape factor 
            rbf_type: selected RBF type
            flag1: nature of the run, i.e.i, simple or BHT run
            flag2: nature of the data, i.e., impedance or admittance, for the BHT run
       Output: 
            Approximation matrix A_im
    """

    # compute omega and the number of frequencies and timescales tau
    omega_vec = 2.*np.pi*freq_vec
    N_freqs = freq_vec.size
    N_taus = tau_vec.size
    
    if flag1 == 'simple':

        # define the A_re output matrix
        out_A_im = np.zeros((N_freqs, N_taus))
    
        # check if the frequencies are sufficiently log spaced
        std_diff_freq = np.std(np.diff(np.log(1/freq_vec)))
        mean_diff_freq = np.mean(np.diff(np.log(1/freq_vec)))
    
        # check if the frequencies are sufficiently log spaced and that N_freqs = N_taus
        toeplitz_trick = std_diff_freq/mean_diff_freq<0.01 and N_freqs == N_taus 
    
        if toeplitz_trick and rbf_type != 'Piecewise Linear': # use toeplitz trick
        
            R = np.zeros(N_taus)
            C = np.zeros(N_freqs)
        
            for p in range(0, N_freqs):
            
                C[p] = - g_ii(freq_vec[p], tau_vec[0], epsilon)
        
            for q in range(0, N_taus):
            
                R[q] = - g_ii(freq_vec[0], tau_vec[q], epsilon)
                        
            out_A_im = toeplitz(C,R) 

        else: # use brute force
        
            for p in range(0, N_freqs):
                for q in range(0, N_taus):
            
                    if rbf_type == 'Piecewise Linear': # see (A.3b) and (A.5) in [2]               
                        if q == 0:
                            out_A_im[p, q] = -0.5*(omega_vec[p]*tau_vec[q])/(1+(omega_vec[p]*tau_vec[q])**2)*np.log(tau_vec[q+1]/tau_vec[q])
                        elif q == N_taus-1:
                            out_A_im[p, q] = -0.5*(omega_vec[p]*tau_vec[q])/(1+(omega_vec[p]*tau_vec[q])**2)*np.log(tau_vec[q]/tau_vec[q-1])
                        else:
                            out_A_im[p, q] = -0.5*(omega_vec[p]*tau_vec[q])/(1+(omega_vec[p]*tau_vec[q])**2)*np.log(tau_vec[q+1]/tau_vec[q-1])             
                
                    else:
                        out_A_im[p, q]= - g_ii(freq_vec[p], tau_vec[q], epsilon)
    
    else: # BHT run
    
        out_A_im = np.zeros((N_freqs, N_taus+1))
        out_A_im[:,0] = omega_vec

        if flag2 == 'impedance': # for the impedance calculations
        
            for p in range(0, N_freqs):
                for q in range(0, N_taus): # see (11b) in [3]
                    if q == 0:
                        out_A_im[p, q+1] = -0.5*(omega_vec[p]*tau_vec[q])/(1+(omega_vec[p]*tau_vec[q])**2)*np.log(tau_vec[q+1]/tau_vec[q])
                    elif q == N_taus-1:
                        out_A_im[p, q+1] = -0.5*(omega_vec[p]*tau_vec[q])/(1+(omega_vec[p]*tau_vec[q])**2)*np.log(tau_vec[q]/tau_vec[q-1])
                    else:
                        out_A_im[p, q+1] = -0.5*(omega_vec[p]*tau_vec[q])/(1+(omega_vec[p]*tau_vec[q])**2)*np.log(tau_vec[q+1]/tau_vec[q-1])
        
        else:  # for the admittance calculations
        
            for p in range(0, N_freqs):
                for q in range(0, N_taus): # see (16b) in the SI of [3]
                    if q == 0:
                        out_A_im[p, q+1] = 0.5*(omega_vec[p])/(1+(omega_vec[p]*tau_vec[q])**2)*np.log(tau_vec[q+1]/tau_vec[q])
                    elif q == N_taus-1:
                        out_A_im[p, q+1] = 0.5*(omega_vec[p])/(1+(omega_vec[p]*tau_vec[q])**2)*np.log(tau_vec[q]/tau_vec[q-1])
                    else:
                        out_A_im[p, q+1] = 0.5*(omega_vec[p])/(1+(omega_vec[p]*tau_vec[q])**2)*np.log(tau_vec[q+1]/tau_vec[q-1])

    if data_type == 'Electric Modulus' or data_type == 'Admittance':
        for p in range(0, N_freqs):
            for q in range(0, N_taus):
                out_A_im[p, q] = -out_A_im[p,q]

    return out_A_im


def assemble_M_1(tau_vec, epsilon, rbf_type, flag='simple'): # see (38) in [1]
    
    """
       This function computes the matrix, M, of the inner products of the first derivatives of the RBF functions used in 
       the expansion. 
       Inputs:
            tau_vec: vector of timescales
            epsilon: shape factor 
            rbf_type: selected RBF type
            flag: nature of the run, i.e.i, simple or BHT run
       Output: 
            Matrix M
    """
    
    freq_vec = 1/tau_vec 
    
    # first get the number of collocation points
    N_taus = tau_vec.size
    N_freq = freq_vec.size
    
    if flag == 'simple': # simple run
    
        # define the M output matrix
        out_M = np.zeros([N_taus, N_taus])
    
        # check if the collocation points are sufficiently log spaced
        std_diff_freq = np.std(np.diff(np.log(tau_vec)))
        mean_diff_freq = np.mean(np.diff(np.log(tau_vec)))
    
        # if they are, we apply the toeplitz trick  
        toeplitz_trick = std_diff_freq/mean_diff_freq<0.01
    
        if toeplitz_trick and rbf_type != 'Piecewise Linear': # apply the toeplitz trick to compute the M matrix 
        
            R = np.zeros(N_taus)
            C = np.zeros(N_taus)
        
            for n in range(0,N_taus):
                C[n] = inner_prod_rbf_1(freq_vec[0], freq_vec[n], epsilon)
            
            for m in range(0,N_taus):
                R[m] = inner_prod_rbf_1(freq_vec[m], freq_vec[0], epsilon)    
        
            out_M = toeplitz(C,R) 
         
        elif rbf_type == 'Piecewise Linear': 
       
            out_L_temp = np.zeros([N_freq-1, N_freq])
        
            for iter_freq_n in range(0,N_freq-1):
                delta_loc = np.log((1/freq_vec[iter_freq_n+1])/(1/freq_vec[iter_freq_n]))
                out_L_temp[iter_freq_n,iter_freq_n] = -1/delta_loc
                out_L_temp[iter_freq_n,iter_freq_n+1] = 1/delta_loc

            out_M = out_L_temp.T@out_L_temp
    
        else: # compute rbf with brute force
    
            for n in range(0, N_taus):
                for m in range(0, N_taus):            
                    out_M[n,m] = inner_prod_rbf_1(freq_vec[n], freq_vec[m], epsilon)
    
    else: # BHT run ; see (18) in [3]
        
        out_M = np.zeros((N_taus-2, N_taus+1))
        
        for p in range(0, N_taus-2):

            delta_loc = np.log(tau_vec[p+1]/tau_vec[p])
            
            if p==0:
                out_M[p,p+1] = -3./(2*delta_loc)
                out_M[p,p+2] = 4./(2*delta_loc)
                out_M[p,p+3] = -1./(2*delta_loc)
                
            elif p == N_taus-2:
                out_M[p,p]   = 1./(2*delta_loc)
                out_M[p,p+1] = -4./(2*delta_loc)
                out_M[p,p+2] = 3./(2*delta_loc)
                
            else:
                out_M[p,p] = 1./(2*delta_loc)
                out_M[p,p+2] = -1./(2*delta_loc)
        
    return out_M


def assemble_M_2(tau_vec, epsilon, rbf_type, flag='simple'): # see (38) in [1]
    
    """
       This function computes the matrix, M, of the inner products of the second derivatives of the RBF functions used in 
       the expansion. 
       Inputs:
            tau_vec: vector of timescales
            epsilon: shape factor 
            rbf_type: selected RBF type
            flag: nature of the run, i.e.i, simple or BHT run
       Output: 
            Matrix M
    """ 
    
    freq_vec = 1/tau_vec            
    
    # first get number of collocation points
    N_taus = tau_vec.size
    
    if flag == 'simple': # simple run
    
        # define the M output matrix
        out_M = np.zeros([N_taus, N_taus])
    
        # check if the collocation points are sufficiently log spaced
        std_diff_freq = np.std(np.diff(np.log(tau_vec)));
        mean_diff_freq = np.mean(np.diff(np.log(tau_vec)));
    
        # if they are, we apply the toeplitz trick  
        toeplitz_trick = std_diff_freq/mean_diff_freq<0.01
    
        if toeplitz_trick and rbf_type != 'Piecewise Linear': # apply the toeplitz trick to compute the M matrix 
        
            R = np.zeros(N_taus)
            C = np.zeros(N_taus)
        
            for n in range(0,N_taus):
                C[n] = inner_prod_rbf_2(freq_vec[0], freq_vec[n], epsilon) # later, we shall use tau instead of freq
            
            for m in range(0,N_taus):
                R[m] = inner_prod_rbf_2(freq_vec[m], freq_vec[0], epsilon) # later, we shall use tau instead of freq
        
            out_M = toeplitz(C,R) 
         
        elif rbf_type == 'Piecewise Linear':
        
            out_L_temp = np.zeros((N_taus-2, N_taus))
    
            for p in range(0, N_taus-2):
                delta_loc = np.log(tau_vec[p+1]/tau_vec[p])
            
                if p == 0 or p == N_taus-3:
                    out_L_temp[p,p] = 2./(delta_loc**2)
                    out_L_temp[p,p+1] = -4./(delta_loc**2)
                    out_L_temp[p,p+2] = 2./(delta_loc**2)
                    
                else:
                    out_L_temp[p,p] = 1./(delta_loc**2)
                    out_L_temp[p,p+1] = -2./(delta_loc**2)
                    out_L_temp[p,p+2] = 1./(delta_loc**2)
                
            out_M = out_L_temp.T@out_L_temp
    
        else: # compute rbf with brute force
    
            for n in range(0, N_taus):
                for m in range(0, N_taus):            
                    out_M[n,m] = inner_prod_rbf_2(freq_vec[n], freq_vec[m], epsilon)
                    
    else: # BHT run
        
        out_M = np.zeros((N_taus-2, N_taus+1))
        
        for p in range(0, N_taus-2):

            delta_loc = np.log(tau_vec[p+1]/tau_vec[p])
            
            if p==0 or p == N_taus-3:
                out_M[p,p+1] = 2./(delta_loc**2)
                out_M[p,p+2] = -4./(delta_loc**2)
                out_M[p,p+3] = 2./(delta_loc**2)
                
            else:
                out_M[p,p+1] = 1./(delta_loc**2)
                out_M[p,p+2] = -2./(delta_loc**2)
                out_M[p,p+3] = 1./(delta_loc**2)
        
    return out_M


def quad_format_separate(A, b, M, lambda_value):
    
    """
       This function reformats the DRT regression as a quadratic program using either the real or imaginary part of the impedance as follows:
                min (x^T*H*x + c^T*x) under the constraint that x => 0 with H = 2*(A^T*A + lambda_value*M) and c = -2*b^T*A        
       Inputs: 
            A: discretization matrix
            b: vector of the real or imaginary part of the impedance
            M: differentiation matrix
            lambda_value: regularization parameter used in Tikhonov regularization
       Outputs: 
            Matrix H
            Vector c
    """
    
    H = 2*(A.T@A+lambda_value*M)
    H = (H.T+H)/2
    c = -2*b.T@A
    
    return H, c


def quad_format_combined(A_re, A_im, Z_re, Z_im, M, lambda_value):
    
    """
       This function reformats the DRT regression as a quadratic program using both real and imaginary parts of the impedance
       Inputs:
            A_re: discretization matrix for the real part of the impedance
            A_im: discretization matrix for the imaginary part of the impedance
            Z_re: vector of the real parts of the impedance
            Z_im: vector of the imaginary parts of the impedance
            M: differentiation matrix
            lambda_value: regularization parameter used in Tikhonov regularization
       Outputs: 
            Matrix H
            Vector c
    """
    
    H = 2*((A_re.T@A_re+A_im.T@A_im)+lambda_value*M)
    H = (H.T+H)/2
    c = -2*(Z_im.T@A_im+Z_re.T@A_re)

    return H, c


def cvxpy_solve_qp(H, c):

    """ 
       This function uses cvxpy to minimize the quadratic problem 0.5*x^T*H*x + c^T*x under the non-negativity constraint.
       Inputs: 
           H: matrix
           c: vector
        Output: 
           Vector solution of the aforementioned problem
    """
    
    N_out = c.shape[0]
    x = cp.Variable(shape = N_out, value = np.ones(N_out))
    h = np.zeros(N_out)
    
    prob = cp.Problem(cp.Minimize((1/2)*cp.quad_form(x, H) + c@x), [x >= h])
    prob.solve(verbose = True, eps_abs = 1E-10, eps_rel = 1E-10, sigma = 1.00e-08, 
               max_iter = 200000, eps_prim_inf = 1E-5, eps_dual_inf = 1E-5)

    gamma = x.value
    
    return gamma


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
