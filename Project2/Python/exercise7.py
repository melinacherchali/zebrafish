
import os
import numpy as np
import matplotlib.pyplot as plt
import farms_pylog as pylog

from simulation_parameters import SimulationParameters
from util.run_open_loop import run_single
from util.entraining_signals import define_entraining_signals
from plotting_common import plot_time_histories

from util.zebrafish_hyperparameters import define_hyperparameters
hyperparameters = define_hyperparameters()
REF_JOINT_AMP = hyperparameters["REF_JOINT_AMP"]
ws_ref = hyperparameters["ws_ref"]


def exercise7():

    pylog.info("Ex 7")
    # pylog.info("Implement exercise 7")
    log_path = './logs/exercise7/'  # path for logging the simulation data
    os.makedirs(log_path, exist_ok=True)

    motor_output_gains = np.array(
        [
            0.00824, 0.00328, 0.00328, 0.00370, 0.00451,
            0.00534, 0.00628, 0.00680, 0.00803, 0.01084,
            0.01115, 0.01149, 0.01655,
        ]
    )

    entraining_signals = define_entraining_signals(5001, 8, plot_signals=True)

    all_pars = SimulationParameters(
        n_iterations       = 5001,
        controller         = "abstract oscillator",
        log_path           = log_path,
        compute_metrics    = 'all',
        print_metrics      = True,
        return_network     = True,
        drive              = 10,
        video_name         = "simulation7",
        video_record       = False,
        headless           = True,
        cpg_amplitude_gain = motor_output_gains,
        entraining_signals = entraining_signals,
        feedback_weights_contra = -0.25,
        feedback_weights_ipsi = 0.25,
    )

    pylog.info("Running the simulation")
    controller = run_single(
        all_pars
    )


if __name__ == '__main__':

    exercise7()

