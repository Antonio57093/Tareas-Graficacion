import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt


MU = 255  # Parámetro para Mu-law
A = 87.6  # Parámetro para A-law

def mu_law_compression(x, mu=MU):
    return np.sign(x) * np.log(1 + mu * np.abs(x)) / np.log(1 + mu)

def mu_law_expansion(y, mu=MU):
    return np.sign(y) * (1/mu) * ((1 + mu) ** np.abs(y) - 1)

# Función de compresión A-law
def a_law_compression(x, A=A):
    return np.where(np.abs(x) < (1/A),
                    (A * np.abs(x)) / (1 + np.log(A)),
                    (1 + np.log(A * np.abs(x))) / (1 + np.log(A))) * np.sign(x)

# Función de expansión A-law
def a_law_expansion(y, A=A):
    return np.where(np.abs(y) < (1 / (1 + np.log(A))),
                    (np.abs(y) * (1 + np.log(A))) / A,
                    np.exp(np.abs(y) * (1 + np.log(A)) - 1) / A) * np.sign(y)

file_path = "lol.wav"  # Cambia esto por el nombre de tu archivo
audio, samplerate = sf.read(file_path)

audio = audio / np.max(np.abs(audio))

mu_compressed = mu_law_compression(audio)
mu_expanded = mu_law_expansion(mu_compressed)

a_compressed = a_law_compression(audio)
a_expanded = a_law_expansion(a_compressed)

sf.write("leymu.wav", mu_expanded, samplerate)
sf.write("leya.wav", a_expanded, samplerate)

plt.figure(figsize=(12, 6))

plt.subplot(3, 1, 1)
plt.plot(audio[:50000], label="Audio Original", color='black')
plt.title("Audio Original")
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(mu_expanded[:50000], label="Mu-law Expandida", color='blue')
plt.title("Audio Procesado con Mu-law")
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(a_expanded[:50000], label="A-law Expandida", color='red')
plt.title("Audio Procesado con A-law")
plt.legend()

plt.tight_layout()
plt.show()

print(" Procesamiento completado. Se generaron los archivos:")
print("- mu_law_audio.wav")
print("- a_law_audio.wav")
print("\n🔊 ¡Ahora puedes reproducirlos y comparar cómo suenan!")



