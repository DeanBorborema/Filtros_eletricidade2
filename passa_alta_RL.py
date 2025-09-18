import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lti, freqresp, lfilter

# ================================
# PARÂMETROS DO FILTRO
# ================================
R = 1e3   # 1 kΩ
L = 0.1   # 100 mH

# Frequência de corte
omega_c = R/L
f_c = omega_c/(2*np.pi)

print(f"Filtro passa-alta RL")
print(f"R = {R} Ω, L = {L} H")
print(f"Frequência de corte: {f_c:.2f} Hz")

# ================================
# CRIAÇÃO DO MODELO DO FILTRO
# ================================
# H(s) = sL / (sL + R)
# Reorganizando: H(s) = s / (s + R/L)
numerator = [1, 0]    # s
denominator = [1, R/L]  # s + R/L

# Cria objeto LTI
system = lti(numerator, denominator)

# ================================
# RESPOSTA EM FREQUÊNCIA
# ================================
w = np.logspace(1, 5, 1000)  # frequência em rad/s
w, h = freqresp(system, w)

plt.figure(figsize=(8,4))
plt.semilogx(w/(2*np.pi), 20*np.log10(abs(h)))
plt.title("Resposta em frequência - Filtro Passa-Alta RL")
plt.xlabel("Frequência [Hz]")
plt.ylabel("Magnitude [dB]")
plt.grid(True, which='both', ls='--')
plt.axvline(f_c, color='red', linestyle='--', label=f'F_c = {f_c:.2f} Hz')
plt.legend()
plt.show()

# ================================
# SIMULAÇÃO COM SINAL DE TESTE
# ================================
fs = 100000  # Hz, taxa de amostragem
t = np.linspace(0, 0.01, int(fs*0.01), endpoint=False)

# Sinal: 50 Hz (baixo) + 5 kHz (alto)
x = np.sin(2*np.pi*50*t) + 0.5*np.sin(2*np.pi*5000*t)

# Filtra o sinal
y = lfilter(numerator, denominator, x)

plt.figure(figsize=(10,4))
plt.plot(t, x, label="Sinal original")
plt.plot(t, y, color='red', label="Sinal filtrado")
plt.title("Filtro Passa-Alta RL - Aplicação prática")
plt.xlabel("Tempo [s]")
plt.ylabel("Amplitude")
plt.legend()
plt.grid()
plt.show()