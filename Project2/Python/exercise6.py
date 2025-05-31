
import os
import farms_pylog as pylog
import numpy as np
import matplotlib.pyplot as plt

from util.rw import load_object
from util.run_closed_loop import run_multiple, run_single
from simulation_parameters import SimulationParameters
from plotting_common import plot_1d, save_figures, plot_2d

from util.zebrafish_hyperparameters import define_hyperparameters
hyperparameters = define_hyperparameters()
REF_JOINT_AMP = hyperparameters["REF_JOINT_AMP"]
ws_ref = hyperparameters["ws_ref"]


def exercise6():

    pylog.info("Ex 6")
    pylog.info("Implement exercise 6")
    log_path = './logs/exercise6/'  # path for logging the simulation data
    os.makedirs(log_path, exist_ok=True)
    
    motor_output_gains = np.array(
        [
            0.00824, 0.00328, 0.00328, 0.00370, 0.00451,
            0.00534, 0.00628, 0.00680, 0.00803, 0.01084,
            0.01115, 0.01149, 0.01655,
        ]
    )
    
    
    # Varying contralateral feedback weights
    
    
    all_pars = [SimulationParameters(
        n_iterations       = 5001,
        controller         = "abstract oscillator",
        log_path           = log_path,
        compute_metrics    = 'all',
        print_metrics      = True,
        return_network     = True,
        drive              = 10,
        video_name         = "simulation6",
        video_record       = False,
        headless           = True,
        cpg_amplitude_gain = motor_output_gains,
        feedback_weights_contra = contra,
        feedback_weights_ipsi = 0,
    )
        for i, contra  in enumerate(np.linspace(-1,1,1))     
    ]
    pylog.info("Running the simulation")
    controllers = run_multiple(
    all_pars
    )
    
    #retrieving data for plots
    feedback_contra = [controller.pars.feedback_weights_contra for i,controller in enumerate(controllers)]
    twl =  [controller.metrics["neur_twl"] for i,controller in enumerate(controllers)]
    freq = [controller. metrics["neur_frequency"] for i,controller in enumerate(controllers)]
    
    
    #neural parameters plot
    fig, axs = plt.subplots(2)
    fig.suptitle('Neural parameters')
    fig.set_size_inches(10, 8)
    
    axs[0].plot(feedback_contra,twl)
    axs[0].set_title('Neural TWL vs $w_{contra}$')
    axs[0].set_ylabel('Neural TWL')
    axs[0].set_xlabel('$w_{contra}$')
    
    axs[1].plot(feedback_contra,freq)
    axs[1].set_title('Neural frequency vs $w_{contra}$')
    axs[1].set_ylabel('Neural frequency')
    axs[1].set_xlabel('$w_{contra}$')
    
    plt.tight_layout()
    
    
    #mechanical metrics
    CoT = [controller.metrics["mech_cot"] for i,controller in enumerate(controllers)]
    energy = [controller.metrics["mech_energy"] for i,controller in enumerate(controllers)]
    speed_fwd = [controller.metrics["mech_speed_fwd"] for i,controller in enumerate(controllers)]
    joint_amp = [controller.metrics["mech_joint_amplitudes"] for i,controller in enumerate(controllers)]
    torque = [controller.metrics["mech_torque"] for i,controller in enumerate(controllers)]
    
    fig, axs = plt.subplots(4)
    fig.suptitle('Mechanical parameters')
    fig.set_size_inches(10, 8)
    
    axs[0].plot(feedback_contra,CoT)
    axs[0].set_ylabel('CoT')
    
    
    axs[1].plot(feedback_contra,energy)
    axs[1].set_ylabel('Energy')
    
    
    axs[2].plot(feedback_contra,speed_fwd)
    axs[2].set_ylabel('Speed')
    
    
    axs[3].plot(feedback_contra,torque) 
    axs[3].set_ylabel('Torque')
    axs[3].set_xlabel('$w_{contra}$')
    
    plt.tight_layout()
    
    
    plt.figure(figsize = [10,8])
    plt.plot(feedback_contra, joint_amp)
    plt.xlabel('$w_{contra}$')
    plt.ylabel('Joint Amplitudes')
    plt.title('Joint Ampltitudes with varying $w_{contra}$')
    
    plt.tight_layout()
    
     
    
    
    # Varying ipsilateral feedback weight
    
    
    all_pars = [SimulationParameters(
        n_iterations       = 5001,
        controller         = "abstract oscillator",
        log_path           = log_path,
        compute_metrics    = 'all',
        print_metrics      = True,
        return_network     = True,
        drive              = 10,
        video_name         = "simulation6",
        video_record       = False,
        headless           = True,
        cpg_amplitude_gain = motor_output_gains,
        feedback_weights_contra = 0,
        feedback_weights_ipsi = ipsi,
    )
        for i, ipsi  in enumerate(np.linspace(-1,1,19))     
    ]
    pylog.info("Running the simulation")
    controllers = run_multiple(
    all_pars
    )
    
    #retrieving data for plots
    feedback_ipsi = [controller.pars.feedback_weights_ipsi for i,controller in enumerate(controllers)]
    twl =  [controller.metrics["neur_twl"] for i,controller in enumerate(controllers)]
    freq = [controller. metrics["neur_frequency"] for i,controller in enumerate(controllers)]
    

    #neural parameters plot
    fig, axs = plt.subplots(2)
    fig.suptitle('Neural parameters ')
    fig.set_size_inches(10, 8)
    
    axs[0].plot(feedback_ipsi,twl)
    axs[0].set_title('Neural TWL vs $w_{ipsi}$')
    axs[0].set_ylabel('Neural TWL')
    axs[0].set_xlabel('$w_{ipsi}$')
    
    axs[1].plot(feedback_ipsi,freq)
    axs[1].set_title('Neural frequency vs $w_{ipsi}$')
    axs[1].set_ylabel('Neural frequency')
    axs[1].set_xlabel('$w_{ipsi}$')
    
    plt.tight_layout()
    
    
    #mechanical metrics
    CoT = [controller.metrics["mech_cot"] for i,controller in enumerate(controllers)]
    energy = [controller.metrics["mech_energy"] for i,controller in enumerate(controllers)]
    speed_fwd = [controller.metrics["mech_speed_fwd"] for i,controller in enumerate(controllers)]
    joint_amp = [controller.metrics["mech_joint_amplitudes"] for i,controller in enumerate(controllers)]
    torque = [controller.metrics["mech_torque"] for i,controller in enumerate(controllers)]
    
    fig, axs = plt.subplots(4)
    fig.suptitle('Mechanical parameters')
    fig.set_size_inches(10, 8)
    
    axs[0].plot(feedback_ipsi,CoT)
    axs[0].set_ylabel('CoT')
    
    
    axs[1].plot(feedback_ipsi,energy)
    axs[1].set_ylabel('Energy')
    
    
    axs[2].plot(feedback_ipsi,speed_fwd)
    axs[2].set_ylabel('Speed')
    
    
    axs[3].plot(feedback_ipsi,torque) 
    axs[3].set_ylabel('Torque')
    axs[3].set_xlabel('$w_{ipsi}$')
    
    plt.tight_layout()
    
    
    plt.figure(figsize = [10,8])
    plt.plot(feedback_ipsi, joint_amp)
    plt.xlabel('$w_{ipsi}$')
    plt.ylabel('Joint Amplitudes')
    plt.title('Joint Ampltitudes with varying $w_{ipsi}$')
    
    plt.tight_layout()
    plt.show()
    
if __name__ == '__main__':

    exercise6()

