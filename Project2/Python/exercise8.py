
import os
import numpy as np
import matplotlib.pyplot as plt
import farms_pylog as pylog

from util.rw import load_object
from util.run_open_loop import run_multiple
from util.entraining_signals import define_entraining_signals
from simulation_parameters import SimulationParameters
from plotting_common import plot_2d, save_figures

from util.zebrafish_hyperparameters import define_hyperparameters
hyperparameters = define_hyperparameters()
REF_JOINT_AMP = hyperparameters["REF_JOINT_AMP"]
ws_ref = hyperparameters["ws_ref"]


def exercise8():

    pylog.info("Ex 8")
    pylog.info("Implement exercise 8")
    log_path = './logs/exercise8/'  # path for logging the simulation data
    save_path = './results/exercise8/'  # path for saving the figures
    os.makedirs(log_path, exist_ok=True)
    os.makedirs(save_path, exist_ok=True)

    motor_output_gains = np.array(
        [
            0.00824, 0.00328, 0.00328, 0.00370, 0.00451,
            0.00534, 0.00628, 0.00680, 0.00803, 0.01084,
            0.01115, 0.01149, 0.01655,
        ]
    )

    entrainment_frequencies = np.linspace(3.5, 10, 19)
    feedback_gains = np.linspace(0, 2, 5) 
    diff_ent = np.zeros(len(entrainment_frequencies))
    diff_neur = np.zeros((len(entrainment_frequencies), len(feedback_gains)))

    entraining_signals = [define_entraining_signals(5001, j, plot_signals=True) 
                          for j in entrainment_frequencies]


    for i in range(len(entrainment_frequencies)):
        all_pars = [SimulationParameters(
            n_iterations       = 5001,
            controller         = "abstract oscillator",
            log_path           = log_path,
            compute_metrics    = 'all',
            print_metrics      = True,
            return_network     = True,
            drive              = 10,
            video_name         = "simulation8",
            video_record       = False,
            headless           = True,
            cpg_amplitude_gain = motor_output_gains,
            entraining_signals = entraining_signals[i],
            feedback_weights_contra = w,
            feedback_weights_ipsi = -w,
        )
            for w in feedback_gains
        ]
        pylog.info("Running the simulation")
        controllers = run_multiple(
        all_pars
        )

        ref_freq = controllers[0].metrics["neur_frequency"]
        diff_ent[i] = entrainment_frequencies[i] - ref_freq

        freq = [controller.metrics["neur_frequency"] for controller in controllers]
        diff_neur[i] = freq - np.ones(len(freq)) * ref_freq

        diff_neur = np.asmatrix(diff_neur)
        
    
    for i in range(len(feedback_gains)):
        plt.figure('entrainment_vs_neural_' + str(np.round(feedback_gains[i], 2)), figsize=[8, 8])
        plt.plot(diff_ent, diff_neur[:, i], label='Feedback Gain: {:.2f}'.format(feedback_gains[i]))
        plt.xlabel('Entrainment Frequency Difference [Hz]')
        plt.ylabel('Neural Frequency Difference [Hz]')
        plt.title('Feedback Gain = {:.2f}'.format(feedback_gains[i]))
        plt.grid()
        save_figures(folder=save_path)
    


if __name__ == '__main__':

    exercise8()

