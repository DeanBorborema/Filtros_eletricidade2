import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lti, freqresp, lfilter, lsim

# PARÂMETROS DO FILTRO
R = 100     # Ω
L = 1e-3    # H
C = 10e-6   # F

# Frequência central (rad/s) e em Hz
omega_0 = 1/np.sqrt(L*C)
f_0 = omega_0/(2*np.pi)

# Fator de qualidade e largura de banda
Q = omega_0*L/R
B = omega_0/Q

print(f"Filtro Rejeita-Faixa RLC (Notch)")
print(f"R = {R} Ω, L = {L} H, C = {C} F")
print(f"Frequência central: {f_0:.2f} Hz")
print(f"Fator de qualidade Q: {Q:.2f}")
print(f"Largura de banda B: {B:.2f} rad/s")

# CRIAÇÃO DO MODELO DO FILTRO
numerator = [1, 0, omega_0**2]
denominator = [1, omega_0/Q, omega_0**2]

system = lti(numerator, denominator)

# CÁLCULO DAS FREQUÊNCIAS DE CORTE
f_c_low = f_0 * (-1/(2*Q) + np.sqrt(1/(4*Q**2) + 1))
f_c_high = f_0 * (1/(2*Q) + np.sqrt(1/(4*Q**2) + 1))

# Função para magnitude em dB
def _mag_db_at(f_hz):
    w = 2*np.pi*f_hz
    _, H = freqresp(system, [w])
    return 20*np.log10(np.abs(H[0]))

A_rejection = _mag_db_at(f_0) 
A_pass_low = _mag_db_at(f_c_low) 
A_pass_high = _mag_db_at(f_c_high) 

# RESPOSTA EM FREQUÊNCIA
w = np.logspace(2, 6, 1000) 
w, h = freqresp(system, w)

plt.figure(figsize=(8,4))
plt.semilogx(w/(2*np.pi), 20*np.log10(abs(h)))
plt.title("Resposta em frequência - Filtro Rejeita-Faixa RLC (Notch)")
plt.xlabel("Frequência [Hz]")
plt.ylabel("Magnitude [dB]")
plt.grid(True, which='both', ls='--')
plt.axvline(f_0, color='red', linestyle='--', label=f'f_0 = {f_0:.2f} Hz | Rejeição = {A_rejection:.2f} dB')
plt.axvline(f_c_low, linestyle=':', label=f'f_c_low = {f_c_low:.2f} Hz | Ganho = {A_pass_low:.2f} dB')
plt.axvline(f_c_high, linestyle=':', label=f'f_c_high = {f_c_high:.2f} Hz | Ganho = {A_pass_high:.2f} dB')
plt.legend()
plt.show()