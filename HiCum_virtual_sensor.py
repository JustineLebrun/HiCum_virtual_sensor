# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 09:42:00 2024
MAIN _ VIRTUAL SENSOR
@author: lebrunjus
"""

import tkinter as tk
import tkinter.ttk as ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, datetime, timedelta
import random
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

#####################
"""
    Note
        
    Premier fichier test pour François:
        somme de 3 signaux :
            base_sin_1 : A = 100, f = 0.01 Hz, phase = 0, step = 1, duration = 100 000
            base_sin_2 : A = 100, f = 0.011 Hz, phase = 0, step = 1, duration = 100 000
            base_sin_3 : A = 1, f = 0.01030927835 Hz, phase = 0, step = 1, duration = 100 000
            
       avec plusieurs niveaux de bruit
            
            noise 0
            noise 1
            noise 10
            noise 100
            noise 1000       
            
    
    
    python to exe file
-------------------------

pip install pyinstaller
cd path\to\your\script
pyinstaller --onefile your_script.py
            
"""

##############################################################################
""" TIDES """
# List of Doodson tidal wave components
# Each row contains: speed (cycle/day), wave symbol, wave name
# ww = np.array([
#         [055.565, 'N', 'Lunar Saros'],
#         [056.554, 'Sa', 'Solar annual'],
#         [057.555, 'Ssa', 'Solar semiannual'],
#         [063.655, 'MSm', ''],
#         [065.455, 'Mm', 'Lunar monthly'],
#         [073.555, 'MSf', 'Lunisolar synodic fortnightly'],
#         [075.555, 'Mf', 'Lunisolar fortnightly'],
#         [085.455, 'Mtm', ''],
#         [125.755, '2Q1', 'Larger elliptic diurnal'],
#         [135.655, 'Q1', 'Larger lunar elliptic diurnal'],
#         [137.455, 'rho1', 'Larger lunar evectional diurnal'],
#         [145.555, 'O1', 'Principal lunar declinational'],
#         [155.555, 'M1', 'Smaller lunar elliptic diurnal'],
#         [155.655, 'NO1', ''],
#         [162.556, 'pi1', ''],
#         [163.555, 'P1', 'Principal solar declination'],
#         [164.556, 'S1', 'Solar diurnal'],
#         [165.555, 'K1', 'Lunisolar diurnal'],
#         [166.554, 'psi1', ''],
#         [167.555, 'phi1', ''],
#         [175.455, 'J1', 'Smaller lunar elliptic diurnal'],
#         [185.555, 'OO1', 'Lunar diurnal'],
#         [235.755, '2N2', 'Lunar elliptical semidiurnal second-order'],
#         [237.555, 'MU2', 'Variational'],
#         [245.655, 'N2', 'Larger lunar elliptic semidiurnal'],
#         [247.455, 'nu2', 'Larger lunar evectional'],
#         [255.555, 'M2', 'Principal lunar semidiurnal'],
#         [263.655, 'lam2', 'Smaller lunar evectional'],
#         [265.455, 'L2', 'Smaller lunar elliptic semidiurnal'],
#         [272.555, 'T2', 'Larger solar elliptic'],
#         [273.555, 'S2', 'Principal solar semidiurnal'],
#         [274.555, 'R2', 'Smaller solar elliptic'],
#         [275.555, 'K2', 'Lunisolar semidiurnal'],
#         [291.555, '2SM2', 'Shallow water semidiurnal'],
#         [355.555, 'M3', 'Lunar terdiurnal'],
#         [345.555, '2MK3', 'Shallow water terdiurnal'],
#         [365.555, 'MK3', 'Shallow water terdiurnal'],
#         [445.655, 'MN4', 'Shallow water quarter diurnal'],
#         [455.555, 'M4', 'Shallow water overtides of principal lunar'],
#         [473.555, 'MS4', 'Shallow water quarter diurnal'],
#         [491.555, 'S4', 'Shallow water overtides of principal solar'],
#         [655.555, 'M6', 'Shallow water overtides of principal lunar'],
#         [855.555, 'M8', 'Shallow water eighth diurnal']
# ])

# # Earth-Moon-Sun astronomical attributes (cycle/day)
# ems = np.array([
#     1.03505,   # T: Lunar day
#     27.3217,   # s: Moon's longitude: tropical month
#     365.2422,  # h: Sun's longitude: solar year
#     365.25 * 8.847,    # p: Lunar perigee
#     365.25 * 18.613,   # N: Lunar node
#     365.25 * 20941     # pp: Lunar perigee (precession of the perihelion)
# ])

##############################################################################
""" FUNCTIONS """

def layout(ax):
    ax.xaxis.grid(True, which="both", color="#cccccc", alpha=0.8, lw=0.5)
    ax.yaxis.grid(True, which="both", color="#cccccc", alpha=0.8, lw=0.5)
    ax.patch.set_visible(False)
    ax.tick_params( length=0, pad=8.0)
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    ax.spines['bottom'].set_color('gray')

    handles, labels = ax.get_legend_handles_labels()
    if labels:
        common_legend_params = {
            'bbox_to_anchor': (1.0, 1.15),
            'loc' : 'upper right',
            'ncol': 1,
            'frameon': True,
            'fontsize': 13,
            'borderpad': 0.5
        }
        ax.legend(handles, labels, **common_legend_params)
         
### button
def handle_ok(event):
    global base_sin, x
    amp = float(entry_amp.get()) if entry_amp.get() else default_amp
    freq = float(entry_freq.get()) if entry_freq.get() else default_freq
    phase = float(entry_phase.get()) if entry_phase.get() else default_phase
    dur = float(entry_dur.get()) if entry_dur.get() else default_dur
    step = float(entry_step.get()) if entry_step.get() else default_step
    
    x = np.arange(0, dur, step)
    base_sin = amp * np.sin(2 * np.pi * freq * x + np.radians(phase))
    
    # Update plot
    ax_s.clear()
    layout(ax_s)
    ax_s.plot(x, base_sin, '-', color='crimson', label='Base Signal')
    ax_s.legend()
    canvas_s.draw()

def generate_noise(event):
    global noise

    seed = float(entry_seed.get()) if entry_seed.get() else def_seed
    random.seed(seed)
    np.random.seed(int(seed))
    
    dur = float(entry_dur.get()) if entry_dur.get() else default_dur
    step = float(entry_step.get()) if entry_step.get() else default_step
    time = np.arange(0, dur, step)
    A_max = float(entry_A_max.get()) if entry_A_max.get() else def_A_max
    
    noise = np.random.uniform(0, A_max, len(time))  
    #center noise around mean 
    noise = noise - np.mean(noise)
    
    ax_n.clear()
    layout(ax_n)
    ax_n.plot(time, noise, '-', color='blue', label='Noise')
    ax_n.legend()
    canvas_n.draw()
    
def add_noise_to_signal():
    if base_sin is None or noise is None:
        print("Error: Generate the base signal and noise first!")
        return
    
    global combined_signal 
    combined_signal = base_sin + noise
    
    # Update main plot with combined signal
    ax_t.clear()
    layout(ax_t)
    ax_t.plot(x, base_sin, '-', color='crimson', label='Base Signal')
    ax_t.plot(x, combined_signal, '-', color='green', label='Signal with Noise')
    ax_t.legend()
    canvas_t.draw()
    
def save_in_file():
    global combined_signal

    if combined_signal is None:
        print("Error: Generate the signal with noise before saving!")
        return

    now = datetime.now()
    now_format = now.strftime("%Y__%m__%d__%H__%M") ### Format YYYY__MM__DD__HH__MM__SS__xxxxx
    first_second = now.second
    step = float(entry_step.get()) if entry_step.get() else default_step

    # Create the filename with timestamp
    filename = f"virtual_sensor_data_{now_format}.txt"

    try:
        with open(filename, "w") as file:
            # Write header
            file.write(f"# Virtual Sensor Data Export\n")
            file.write(f"# Date: {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write("# YYYY__MM__DD__HH__MM__SS__Signal Value\n")

            # Write signal data
            for i, value in enumerate(combined_signal):
                #timestamp = int(first_second + i * step)
                new_time = now + timedelta(seconds=i * step)
                new_time_format = new_time.strftime("%Y__%m__%d__%H__%M__%S")
                #file.write(f"{now_format}{timestamp:.3f}__{value:.6f}\n")
                file.write(f"{new_time_format}__{value:.6f}\n")

        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"Error while saving file: {e}")

def update_base_signal(*args):
    return
#     selected_tide = value_inside.get()
#     #params = tidal_wave_params.get(selected_tide, {'amp': default_amp, 'freq': default_freq, 'phase': default_phase})
    
#     for wave in ww:
#         if wave[1] == selected_tide:
#             freq_cpd = float(wave[0])  # Frequency in cycles per day
#             freq_hz = freq_cpd / 86400  # Convert cycles per day to Hz (since 1 day = 86400 seconds)
#             amp = 1.0  # You can modify this or add specific amplitudes as needed
#             phase = 0.0  # Default phase; you can customize it too
            
#             # Update the entry fields with the new parameters
#             entry_amp.delete(0, tk.END)
#             entry_amp.insert(0, str(amp))

#             entry_freq.delete(0, tk.END)
#             entry_freq.insert(0, str(freq_hz))

#             entry_phase.delete(0, tk.END)
#             entry_phase.insert(0, str(phase))
            
#             # Generate the base signal with the new parameters
#             handle_ok(None)
#             break

    
##############################################################################

""" FILE """

# file = open("virtual_sensor_data.txt", "w")

""" DATA """

# Default parameters
default_amp = 1
default_freq = 0.001
default_phase = 90
default_dur = 1000
default_step = 1

def_A_max = 1
def_seed = 42

base_sin = None
noise = None
x = np.arange(0, default_dur, default_step)

""" WINODW """

### create a window
window = tk.Tk()
window.title("Virtual Sensor")

### frames
frame_data = tk.Frame(master=window, bg="white")
frame_data.pack(fill=tk.BOTH, side=tk.LEFT) #fills automatically in both directions

frame_plot = tk.Frame(master=window)
frame_plot.pack(fill=tk.BOTH, expand=True)

color_bg_entries = "antiquewhite"

label_amp = tk.Label(text="Wave Parameters", fg="black", bg="white", master=frame_data, font = ("Arial",15), padx=5, pady=5)
label_amp.pack()

### base sine amplitude
label_amp = tk.Label(text="Amplitude", fg="black", bg="white",master=frame_data, font = ("Arial",12), padx=2, pady=2)
label_amp.pack()
entry_amp = tk.Entry(fg="black", bg=color_bg_entries, master=frame_data, font = ("Arial",12))
entry_amp.pack()
entry_amp.insert(0, str(default_amp))

### base sin freq
label_freq = tk.Label(text="Frequency", fg="black", bg="white", master=frame_data, font = ("Arial",12), padx=2, pady=2)
label_freq.pack()
entry_freq = tk.Entry(fg="black", bg=color_bg_entries, master=frame_data, font = ("Arial",12))
entry_freq.pack()
entry_freq.insert(0, str(default_freq))

### base sin phase
label_phase = tk.Label(text="Phase", fg="black", bg="white", master=frame_data, font = ("Arial",12), padx=2, pady=2)
label_phase.pack()
entry_phase = tk.Entry(fg="black", bg=color_bg_entries, master=frame_data, font = ("Arial",12))
entry_phase.pack()
entry_phase.insert(0, str(default_phase))

### base sin step
label_step = tk.Label(text="Step", fg="black", bg="white", master=frame_data, font = ("Arial",12), padx=2, pady=2)
label_step.pack()
entry_step = tk.Entry(fg="black", bg=color_bg_entries, master=frame_data, font = ("Arial",12))
entry_step.pack()
entry_step.insert(0, str(default_step))

### base sin step
label_dur = tk.Label(text="Duration", fg="black", bg="white", master=frame_data, font = ("Arial",12), padx=2, pady=2)
label_dur.pack()
entry_dur = tk.Entry(fg="black", bg=color_bg_entries, master=frame_data, font = ("Arial",12))
entry_dur.pack()
entry_dur.insert(0, str(default_dur))

# Plot for base signal
fig_s, ax_s = plt.subplots(figsize=(10, 3))
layout(ax_s)
canvas_s = FigureCanvasTkAgg(fig_s, master=frame_plot)
canvas_s.get_tk_widget().pack(fill=tk.BOTH, expand=True)

frame_toolbar_s = tk.Frame(master=frame_plot)
frame_toolbar_s.pack(fill=tk.X)
toolbar_s = NavigationToolbar2Tk(canvas_s, frame_toolbar_s)
toolbar_s.update()

### compute button
button_ok = tk.Button(frame_data, text="Generate Signal", command=lambda: handle_ok(None), font = ("Arial",13), fg="black", bg="lightsalmon", padx=1, pady=1)
button_ok.pack(pady=5)


# Default base signal parameters
# default_tide = 'N'
# value_inside = tk.StringVar(frame_data)  # Set the parent to frame_data
# value_inside.set(default_tide)

# # Label for the dropdown menu
# label_tide = tk.Label(master=frame_data, text="Tide wave as Signal", fg="black", bg="white", font=("Arial", 13), padx=5, pady=5)
# label_tide.pack()

# style = ttk.Style()
# style.theme_use('clam')  # Choose a theme (options: 'clam', 'alt', 'default', 'classic')
# style.configure("TCombobox",
#                 fieldbackground="white",
#                 background="lightblue",
#                 borderwidth=2,
#                 relief="solid")

# # Apply the styled combobox
# drop_tide = ttk.Combobox(frame_data, textvariable=value_inside, values=tides, state="readonly", style="TCombobox")
# drop_tide.pack(pady=5)
# drop_tide.current(0)  # Set the default selection

# drop_tide.bind("<<ComboboxSelected>>", lambda event: update_base_signal(value_inside.get()))


# Plot for noise
fig_n, ax_n = plt.subplots(figsize=(10, 3))
layout(ax_n)
canvas_n = FigureCanvasTkAgg(fig_n, master=frame_plot)
canvas_n.get_tk_widget().pack(fill=tk.BOTH, expand=True)

frame_toolbar_n = tk.Frame(master=frame_plot)
frame_toolbar_n.pack(fill=tk.X)
toolbar_n = NavigationToolbar2Tk(canvas_n, frame_toolbar_n)
toolbar_n.update()

# Plot for total
fig_t, ax_t = plt.subplots(figsize=(10, 3))
layout(ax_t)
canvas_t = FigureCanvasTkAgg(fig_t, master=frame_plot)
canvas_t.get_tk_widget().pack(fill=tk.BOTH, expand=True)

frame_toolbar_t = tk.Frame(master=frame_plot)
frame_toolbar_t.pack(fill=tk.X)
toolbar_t = NavigationToolbar2Tk(canvas_t, frame_toolbar_t)
toolbar_t.update()

label_amp = tk.Label(text="Noise Parameters", bg="white", fg="black", master=frame_data, font = ("Arial",15), padx=5, pady=10)
label_amp.pack()

label_seed = tk.Label(text="Seed for random library", bg="white", fg="black", master=frame_data, font = ("Arial",12), padx=2, pady=5)
label_seed.pack()
entry_seed = tk.Entry(fg="black", bg=color_bg_entries, master=frame_data, font = ("Arial",12))
entry_seed.pack()
entry_seed.insert(0, str(def_seed))

label_A_max = tk.Label(text="Maximum amplitude of noise", fg="black", bg="white", master=frame_data, font = ("Arial",12), padx=2, pady=5)
label_A_max.pack()
entry_A_max = tk.Entry(fg="black", bg=color_bg_entries, master=frame_data, font = ("Arial",12))
entry_A_max.pack()
entry_A_max.insert(0, str(def_A_max))

button_generate_noise = tk.Button(frame_data, text="Generate Noise", command=lambda:generate_noise(None), font = ("Arial",13), fg="black", bg="lightsalmon")
button_generate_noise.pack(pady=5)

label_final = tk.Label(text="Final Signal", bg="white", fg="black", master=frame_data, font = ("Arial",15), padx=5, pady=10)
label_final.pack()

button_add_noise = tk.Button(frame_data, text="Add Noise", command=add_noise_to_signal, font = ("Arial",13), fg="black", bg="lightsalmon")
button_add_noise.pack(pady=5)

handle_ok(None)
generate_noise(None)

""" EXPORT FILE """

label_export = tk.Label(text="Export data", fg="black", master=frame_data, font = ("Arial",15), padx=5, pady=10, bg="white")
label_export.pack()

button_save = tk.Button(frame_data, text="Export data to file", command=save_in_file, font = ("Arial",13), fg="black", bg="lightsalmon")
button_save.pack(pady=5)

window.mainloop()
