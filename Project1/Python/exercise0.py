
import plotting_common
from util.run_closed_loop import run_single
from simulation_parameters import SimulationParameters
import matplotlib.pyplot as plt
import os
import farms_pylog as pylog
import numpy as np
import matplotlib
matplotlib.rc('font', **{"size": 15})


def exercise0():

    pylog.info("Implement ex 0")
    log_path = './logs/exercise0/'
    os.makedirs(log_path, exist_ok=True)

    pars = SimulationParameters(
        n_iterations=5001,
        controller="sine",
        amp=0.3,
        twl=1,
        freq=3,
        compute_metrics="all",
        headless=True,
        video_record=False,
        log_path=log_path,
        return_network=True,
    )

    controller = run_single(
        pars
    )

    save_path = "./results/exercise0/" + str(pars.amp) + "_" + str(pars.twl) + "_" + str(pars.freq)
    os.makedirs(save_path, exist_ok=True)

    plt.figure('joint_angle_evolution', figsize=[8, 8])
    plotting_common.plot_time_histories_multiple_windows(controller.times, controller.joints[:,:,0], ylabel=None, xlabel=None, 
                                                         colors = plt.cm.jet(np.linspace(0, 1, controller.joints[:,:,0].shape[1])).tolist())
    plt.gcf().text(0.04, 0.5, 'Joint angles [rad]', va='center', rotation='vertical')
    plt.gcf().text(0.5, 0.04, 'Time [s]', ha='center')
    # plt.gcf().text(0.5, 0.9, 'Joint angles evolution (A = ' + str(pars.amp) + ', TWL = ' + str(pars.twl) + ', freq = ' + str(pars.freq) + ')', ha='center')
    for ax in plt.gcf().get_axes()[1:]:
        ax.set_yticklabels([])
    for ax in plt.gcf().get_axes()[:-1]:
        ax.set_xticklabels([])

    plt.figure('left_right_motor_out', figsize=[8, 8])
    plotting_common.plot_left_right(controller.times, controller.motor_out, controller.motor_l, controller.motor_r)
    # plt.gcf().text(0.5, 0.92, 'Left and right motor outputs (A = ' + str(pars.amp) + ', TWL = ' + str(pars.twl) + ', freq = ' + str(pars.freq) + ')', ha='center')
    
    plt.figure('trajectory', figsize=[8, 8])
    plotting_common.plot_trajectory(controller)
    # plt.gcf().text(0.5, 0.9, 'Center of mass trajectory (A = ' + str(pars.amp) + ', TWL = ' + str(pars.twl) + ', freq = ' + str(pars.freq) + ')', ha='center')

    plotting_common.save_figures(folder=save_path)

if __name__ == '__main__':

    exercise0()