import sympy as sp
import numpy as np
import control

# Define the symbolic variables
x1, x2, u = sp.symbols('x1 x2 u')

# Define the differential equations
x1_dot = -x1 + 2*x1**3 + x2 + 4*u
x2_dot = -x1 - x2 + 2*u

def find_equilibrium_points():
    '''Find equilibrium points where the derivatives are zero.'''
    x1_dot_sub = x1_dot.subs(u, 0)
    x2_dot_sub = x2_dot.subs(u, 0)
    
    eq1 = sp.Eq(x1_dot_sub, 0)
    eq2 = sp.Eq(x2_dot_sub, 0)
    
    equi_points = sp.solve((eq1, eq2), (x1, x2))
    
    return equi_points

def find_A_B_matrices(eq_points):
    '''
    Compute Jacobian A and B matrices and substitute equilibrium points.
    '''
    A_matrix = sp.Matrix([
        [sp.diff(x1_dot, x1), sp.diff(x1_dot, x2)],
        [sp.diff(x2_dot, x1), sp.diff(x2_dot, x2)]
    ])
    
    B_matrix = sp.Matrix([
        [sp.diff(x1_dot, u)],
        [sp.diff(x2_dot, u)]
    ])
    
    A_matrices = []
    B_matrices = []
    
    for point in eq_points:
        A_matrices.append(A_matrix.subs({x1: point[0], x2: point[1]}))
        B_matrices.append(B_matrix.subs({x1: point[0], x2: point[1]}))
    
    return A_matrices, B_matrices

def find_eigen_values(A_matrices):
    '''
    Compute eigenvalues of the Jacobian matrices and determine stability.
    '''
    eigen_values = []
    stability = []
    
    for A in A_matrices:
        eig_vals = A.eigenvals()
        eigen_values.append(eig_vals)
        
        is_stable = all(val.as_real_imag()[0] < 0 for val in eig_vals)
        stability.append('Stable' if is_stable else 'Unstable')
    
    return eigen_values, stability

def compute_lqr_gain(A, B):
    '''
    Compute LQR gain using the Jacobian A and B matrices.
    '''
    # Define the Q and R matrices
    Q = np.eye(2)  # State weighting matrix
    R = np.array([[1]])  # Control weighting matrix
    
    # Compute the LQR gain
    K, _, _ = control.lqr(A, B, Q, R)
    
    return K

def main_function():
    # Find equilibrium points
    eq_points = find_equilibrium_points()
    
    if not eq_points:
        print("No equilibrium points found.")
        return None, None, None, None, None, None
    
    # Find Jacobian matrices
    jacobians_A, jacobians_B = find_A_B_matrices(eq_points)
    
    # Find eigenvalues and stability
    eigen_values, stability = find_eigen_values(jacobians_A)
    
    # Find the first unstable equilibrium point
    unstable_index = next((i for i, s in enumerate(stability) if s == 'Unstable'), None)
    
    if unstable_index is not None:
        # Compute the LQR gain matrix K for the first unstable point
        A = np.array(jacobians_A[unstable_index], dtype=np.float64)
        B = np.array(jacobians_B[unstable_index], dtype=np.float64)
        K = compute_lqr_gain(A, B)
    else:
        K = None
    
    return eq_points, jacobians_A, eigen_values, stability, K

def task1a_output():
    '''
    Print the results obtained from the main function.
    '''
    eq_points, jacobians_A, eigen_values, stability, K = main_function()
    
    if eq_points is None:
        return
    
    print("Equilibrium Points:")
    for i, point in enumerate(eq_points):
        print(f"  Point {i + 1}: x1 = {point[0]}, x2 = {point[1]}")
    
    print("\nJacobian Matrices at Equilibrium Points:")
    for i, matrix in enumerate(jacobians_A):
        print(f"  At Point {i + 1}:")
        print(sp.pretty(matrix, use_unicode=True))
    
    print("\nEigenvalues at Equilibrium Points:")
    for i, eigvals in enumerate(eigen_values):
        eigvals_str = ', '.join([f"{val}: {count}" for val, count in eigvals.items()])
        print(f"  At Point {i + 1}: {eigvals_str}")
    
    print("\nStability of Equilibrium Points:")
    for i, status in enumerate(stability):
        print(f"  At Point {i + 1}: {status}")
    
    print("\nLQR Gain Matrix K at the selected Equilibrium Point:")
    if K is not None:
        print(K)
    else:
        print("No unstable equilibrium point found for LQR gain computation.")

if __name__ == "__main__":
    # Print the results
    task1a_output()
