import numpy as np
from scipy.linalg import eig

def pid_controller(self, dt):
    # Konstanter og variabler for PID kontroller
    fault = self.setpoint - self.position

    W0 = 2.5
    d_m = (0.5 * (self.RO * self.CD0 * self.Area * 0.5))
    Kp = self.mass * (W0**2)
    Kd = 4 * 1 * W0 * self.mass - d_m
    Ki = Kp / 20

    # Rekner ut eigenverdier (ikke påvirker direkte påregning, kun for stabilitetsanalyse)
    A_BK = np.array([[0, 1],
                     [-Kp/self.mass, -Kd/self.mass]])
    
    eigenvalues = eig(A_BK)[0]
    print("Eigenverdier av det lukket sløyfesystemet:", eigenvalues)
    
    # Integral windup beskyttelse: Begrens feilen som integreres
    max_integral = 1  # Velg en passende verdi for maksimum integrert feil
    self.integral_error += dt * fault  # Oppdater den integrerte feilen
    
    # Begrens den integrerte feilen til en viss maksimal verdi
    if self.integral_error > max_integral:
        self.integral_error = max_integral
    elif self.integral_error < -max_integral:
        self.integral_error = -max_integral

    # Rekner ut pådraget
    U = Kp * fault + Kd * (-self.velocity) + Ki *self.integral_error

    # Begrenser Rps fra PID
    #if U > self.max_rps:
    #   U = self.max_rps
    #elif U < -self.max_rps:
    #    U = -self.max_rps

    #self.rps = np.sign(U)*np.sqrt(abs(U)/(1025*0.4*0.04**4)) #Rho * KT0 * propelldiameter^4
    self.rps = np.sign(U) * np.sqrt(abs(U) / (self.RO * self.KT0 * self.propellerDiameter**4))

    if self.rps > self.max_rps:
        self.rps = self.max_rps
    elif self.rps < -self.max_rps:
        self.rps = -self.max_rps


    
    
