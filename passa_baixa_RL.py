import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lti, freqresp, lfilter

# ================================
# PARÂMETROS DO FILTRO
# ================================
# Valores de R (ohms) e L (henries) que definem o filtro
R = 1e3   # 1 kΩ
L = 0.1   # 100 mH

# Frequência de corte (rad/s)
omega_c = R/L
f_c = omega_c/(2*np.pi)  # Hz

print(f"Filtro passa-baixa RL")
print(f"R = {R} Ω, L = {L} H")
print(f"Frequência de corte: {f_c:.2f} Hz")

# ================================
# CRIAÇÃO DO MODELO DO FILTRO
# ================================
# H(s) = R / (sL + R) → transfer function
# Reorganizando: H(s) = (R/L) / (s + R/L)
numerator = [R/L]
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
plt.title("Resposta em frequência - Filtro Passa-Baixa RL")
plt.xlabel("Frequência [Hz]")
plt.ylabel("Magnitude [dB]")
plt.grid(True, which='both', ls='--')
plt.axvline(f_c, color='red', linestyle='--', label=f'F_c = {f_c:.2f} Hz')
plt.legend()
plt.show()

# ================================
# SIMULAÇÃO COM SINAL DE TESTE
# ================================
fs = 100000  # Hz, taxa de amostragem para simulação
t = np.linspace(0, 0.01, int(fs*0.01), endpoint=False)

# Sinal: soma de 50 Hz e 5 kHz (ruído de alta frequência)
x = np.sin(2*np.pi*50*t) + 0.5*np.sin(2*np.pi*5000*t)

# Filtra o sinal
y = lfilter(numerator, denominator, x)

plt.figure(figsize=(10,4))
plt.plot(t, x, label="Sinal original")
plt.plot(t, y, color='red', label="Sinal filtrado")
plt.title("Filtro Passa-Baixa RL - Aplicação prática")
plt.xlabel("Tempo [s]")
plt.ylabel("Amplitude")
plt.legend()
plt.grid()
plt.show()