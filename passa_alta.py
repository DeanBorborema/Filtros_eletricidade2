import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lti, freqresp, lfilter

# ================================
# PARÂMETROS DO FILTRO
# ================================
R = 1e3   # 1 kΩ
C = 1e-6  # 1 uF

# Frequência de corte
omega_c = 1/(R*C)
f_c = omega_c/(2*np.pi)

print(f"Filtro passa-alta RC")
print(f"R = {R} Ω, C = {C} F")
print(f"Frequência de corte: {f_c:.2f} Hz")

# ================================
# CRIAÇÃO DO MODELO DO FILTRO
# ================================
# H(s) = sRC / (1 + sRC)
numerator = [R*C, 0]  # sRC
denominator = [R*C, 1]  # sRC + 1

# Cria objeto LTI
system = lti(numerator, denominator)

# ================================
# RESPOSTA EM FREQUÊNCIA
# ================================
w = np.logspace(1, 5, 1000)  # frequência em rad/s
w, h = freqresp(system, w)

plt.figure(figsize=(8,4))
plt.semilogx(w/(2*np.pi), 20*np.log10(abs(h)))
plt.title("Resposta em frequência - Filtro Passa-Alta RC")
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
plt.title("Filtro Passa-Alta RC - Aplicação prática")
plt.xlabel("Tempo [s]")
plt.ylabel("Amplitude")
plt.legend()
plt.grid()
plt.show()
