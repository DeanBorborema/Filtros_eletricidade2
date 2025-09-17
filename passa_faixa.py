import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lti, freqresp, lfilter

# ================================
# PARÂMETROS DO FILTRO
# ================================
R = 100     # Ω
L = 1e-3    # H
C = 10e-6   # F

# Frequência central (rad/s) e em Hz
omega_0 = 1/np.sqrt(L*C)
f_0 = omega_0/(2*np.pi)

# Fator de qualidade e largura de banda
Q = omega_0*L/R
B = omega_0/Q

print(f"Filtro Passa-Faixa RLC")
print(f"R = {R} Ω, L = {L} H, C = {C} F")
print(f"Frequência central: {f_0:.2f} Hz")
print(f"Fator de qualidade Q: {Q:.2f}")
print(f"Largura de banda B: {B:.2f} rad/s")

# ================================
# CRIAÇÃO DO MODELO DO FILTRO
# ================================
# H(s) = (s/(Q*omega_0)) / (s^2 + s/(Q) + 1)
numerator = [0, 1/(Q*omega_0), 0]  # s/(Q*omega_0)
denominator = [1, 1/(Q*omega_0), 1]  # s^2 + s/(Q*omega_0) + 1

system = lti(numerator, denominator)

# ================================
# RESPOSTA EM FREQUÊNCIA
# ================================
w = np.logspace(2, 6, 1000)  # frequência em rad/s
w, h = freqresp(system, w)

plt.figure(figsize=(8,4))
plt.semilogx(w/(2*np.pi), 20*np.log10(abs(h)))
plt.title("Resposta em frequência - Filtro Passa-Faixa RLC")
plt.xlabel("Frequência [Hz]")
plt.ylabel("Magnitude [dB]")
plt.grid(True, which='both', ls='--')
plt.axvline(f_0, color='red', linestyle='--', label=f'f_0 = {f_0:.2f} Hz')
plt.legend()
plt.show()

# ================================
# SIMULAÇÃO COM SINAL DE TESTE
# ================================
fs = 100000  # Hz, taxa de amostragem
t = np.linspace(0, 0.01, int(fs*0.01), endpoint=False)

# Sinal: soma de três senos em frequências diferentes
x = np.sin(2*np.pi*500*t) + np.sin(2*np.pi*2000*t) + np.sin(2*np.pi*10000*t)

# Filtra o sinal
y = lfilter(numerator, denominator, x)

plt.figure(figsize=(10,4))
plt.plot(t, x, label="Sinal original")
plt.plot(t, y, color='red', label="Sinal filtrado")
plt.title("Filtro Passa-Faixa RLC - Aplicação prática")
plt.xlabel("Tempo [s]")
plt.ylabel("Amplitude")
plt.legend()
plt.grid()
plt.show()
