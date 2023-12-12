from scipy.io import wavfile
import noisereduce as nr
# load data
rate, data = wavfile.read("./yash/Dr_aza.wav")
# perform noise reduction
reduced_noise = nr.reduce_noise(y=data, sr=rate)
wavfile.write("./yash/Dr_aza_nr.wav", rate, reduced_noise)