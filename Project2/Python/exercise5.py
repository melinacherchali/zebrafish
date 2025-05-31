from util.run_closed_loop import run_single
from simulation_parameters import SimulationParameters
import os
import farms_pylog as pylog
import numpy as np
import matplotlib.pyplot as plt
from plotting_common import plot_time_histories
import plotting_common
from util.rw import load_object

from util.zebrafish_hyperparameters import define_hyperparameters
hyperparameters = define_hyperparameters()
REF_JOINT_AMP = hyperparameters["REF_JOINT_AMP"]
ws_ref = hyperparameters["ws_ref"]


def exercise5():
    pylog.info("Ex 5")
    pylog.info("Implement exercise 5")
    log_path = './logs/exercise5/'  # path for logging the simulation data
    os.makedirs(log_path, exist_ok=True)

    motor_output_gains = np.array(
        [
            0.00824, 0.00328, 0.00328, 0.00370, 0.00451,
            0.00534, 0.00628, 0.00680, 0.00803, 0.01084,
            0.01115, 0.01149, 0.01655,
        ]
    )
    
    # Create new parameters using all parameters from the saved controller
    all_pars = SimulationParameters(
        n_iterations       = 5001,
        controller         = "abstract oscillator",
        log_path           = log_path,
        compute_metrics    = 'all',
        print_metrics      = True,
        return_network     = True,
        drive              = 10,
        video_name         = "simulation5",
        video_record       = False,
        headless           = True,
        cpg_amplitude_gain = motor_output_gains,
        feedback_weights_contra = -0.25,
        feedback_weights_ipsi = 0.25,
    )

    pylog.info("Running the simulation")
    controller = run_single(
        all_pars
    )
    plt.figure('Phase Evolution', figsize=[10, 8])
    plot_time_histories(controller.times,controller.state[:, :controller.n_oscillators], xlabel = "Time [s]", ylabel = "Phase [rad]")
    plt.title("Oscillator Phase Evolution")
    
    plt.figure('Amplitude Evolution', figsize=[10, 8])
    plot_time_histories(controller.times,controller.state[:,controller.n_oscillators:],xlabel = "Time [s]", ylabel = "Amplitude [m]")
    plt.title("Oscillator Amplitude Evolution")
    
    plt.figure('Motor Output', figsize=[10, 8])
    plot_time_histories(controller.times, controller.motor_out, xlabel = "Time [s]", ylabel = "Motor Output")
    plt.title("Motor Output") 
    
    dmotor = controller.motor_out
    for i in range(np.size(controller.n_iterations)-1) :
        dmotor[i,:] = controller.motor_out[i+1,:]- controller.motor_output[i,:]
    
    plt.figure('Motor Output Difference', figsize=[10, 8])
    plot_time_histories(controller.times, dmotor, xlabel = "Time [s]", ylabel = "Motor Output Difference")
    plt.title("Motor Output Difference")  
    
    plt.figure('Joint Angle Evolution', figsize=[8, 8])
    plotting_common.plot_time_histories_multiple_windows(controller.times, controller.joints[:,:,0], ylabel=None, xlabel=None, 
                                                         colors = plt.cm.jet(np.linspace(0, 1, controller.joints[:,:,0].shape[1])).tolist())
    plt.gcf().text(0.04, 0.5, 'Joint angles [rad]', va='center', rotation='vertical')
    plt.gcf().text(0.5, 0.04, 'Time [s]', ha='center')
    # plt.gcf().text(0.5, 0.9, 'Joint angles evolution (A = ' + str(pars.amp) + ', TWL = ' + str(pars.twl) + ', freq = ' + str(pars.freq) + ')', ha='center')
    for ax in plt.gcf().get_axes()[1:]:
        ax.set_yticklabels([])
    for ax in plt.gcf().get_axes()[:-1]:
        ax.set_xticklabels([])
    plt.title("Joint Angle Evolution", y = 18)
    plt.show()
    


if __name__ == '__main__':
    exercise5()



#controller.metrics["mech_joint_amplitudes"]