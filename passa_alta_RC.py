import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lti, freqresp, lfilter

# PARÂMETROS DO FILTRO
R = 3.3e3   # 3.3 kΩ
C = 47e-9  # 47 nF

# Frequência de corte
omega_c = 1/(R*C)
f_c = omega_c/(2*np.pi)

print(f"Filtro passa-alta RC")
print(f"R = {R} Ω, C = {C} F")
print(f"Frequência de corte: {f_c:.2f} Hz")

# CRIAÇÃO DO MODELO DO FILTRO
numerator = [R*C, 0]
denominator = [R*C, 1]

# Cria objeto LTI
system = lti(numerator, denominator)

# Pontos de avaliação: Astop em 0.1*fc, Apass em 10*fc
f_stop = 0.1 * f_c
f_pass = 10.0 * f_c

def _mag_db_at(f_hz):
    w = 2*np.pi*f_hz
    _, H = freqresp(system, [w])
    return 20*np.log10(np.abs(H[0]))

A_stop = _mag_db_at(f_stop)
A_pass = _mag_db_at(f_pass)

print(f"Astop @ {f_stop:.2f} Hz: {A_stop:.2f} dB")
print(f"Apass @ {f_pass:.2f} Hz: {A_pass:.2f} dB")

# RESPOSTA EM FREQUÊNCIA
w = np.logspace(1, 5, 1000)
w, h = freqresp(system, w)

plt.figure(figsize=(8,4))
plt.semilogx(w/(2*np.pi), 20*np.log10(abs(h)))
plt.title("Resposta em frequência - Filtro Passa-Alta RC")
plt.xlabel("Frequência [Hz]")
plt.ylabel("Magnitude [dB]")
plt.grid(True, which='both', ls='--')
plt.axvline(f_c, color='red', linestyle='--', label=f'F_c = {f_c:.2f} Hz')

plt.axvline(f_stop, linestyle=':', label=f'f_stop = {f_stop:.2f} Hz | Astop = {A_stop:.2f} dB')
plt.axvline(f_pass, linestyle=':', label=f'f_pass = {f_pass:.2f} Hz | Apass = {A_pass:.2f} dB')

plt.legend()
plt.show()