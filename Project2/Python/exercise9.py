
from util.run_closed_loop import run_single
from simulation_parameters import SimulationParameters
import os
import farms_pylog as pylog
import numpy as np
import matplotlib.pyplot as plt
from plotting_common import plot_time_histories
import plotting_common

from util.zebrafish_hyperparameters import define_hyperparameters
hyperparameters = define_hyperparameters()
REF_JOINT_AMP = hyperparameters["REF_JOINT_AMP"]
ws_ref = hyperparameters["ws_ref"]

motor_output_gains = np.array(
        [
            0.00824, 0.00328, 0.00328, 0.00370, 0.00451,
            0.00534, 0.00628, 0.00680, 0.00803, 0.01084,
            0.01115, 0.01149, 0.01655,
        ]
    )


def exercise9_0(contra_CPG=True, no_video=True, plot=True):
    """
    Exercise 9.0: Run a single simulation for a single set of feedback weights.
    """
    
    if contra_CPG: # keep default parameters for contra CPG
        all_pars = SimulationParameters(
            n_iterations=15001,
            controller="abstract oscillator",
            headless=no_video,
            return_network=True,
            drive=10,
            weights_body2body=0,  # no ipsi CPG
            # weights_body2body_contralateral=0,  # no contra CPG
            feedback_weights_ipsi=0.25,
            feedback_weights_contra=-0.25,
            cpg_amplitude_gain=motor_output_gains,
            compute_metrics='all',
            print_metrics=True,
            initial_phases=np.random.rand(26) * 2 * np.pi, # random initial phases
        )
    else: # set contra CPG to zero
        all_pars = SimulationParameters(
            n_iterations=15001,
            controller="abstract oscillator",
            headless=no_video,
            return_network=True,
            drive=10,
            weights_body2body=0,  # no ipsi CPG
            weights_body2body_contralateral=0,  # no contra CPG
            feedback_weights_ipsi=0.25,
            feedback_weights_contra=-0.25,
            cpg_amplitude_gain=motor_output_gains,
            compute_metrics='all',
            print_metrics=True,
            initial_phases=np.random.rand(26) * 2 * np.pi, # random initial phases
        )
        
    pylog.info("Running the simulation")
    
    controller = run_single(all_pars)
    
    if plot:
        plt.figure('Phase Evolution', figsize=[10, 8])
        plot_time_histories(controller.times,controller.state[:, :controller.n_oscillators], xlabel = "Time [s]", ylabel = "Phase [rad]")
        plt.title("Oscillator Phase Evolution")
        
        plt.figure('Amplitude Evolution', figsize=[10, 8])
        plot_time_histories(controller.times,controller.state[:,controller.n_oscillators:],xlabel = "Time [s]", ylabel = "Amplitude [m]")
        plt.title("Oscillator Amplitude Evolution")
        
        plt.figure('Motor Output', figsize=[10, 8])
        plot_time_histories(controller.times, controller.motor_out, xlabel = "Time [s]", ylabel = "Motor Output")
        plt.title("Motor Output") 
        
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
    
def exercise9_1():
    pylog.info("Exercise 9 — Line plots from varying feedback weights")

    # Sweep over w values (you can decouple ipsi/contra if needed)
    w_vals = np.linspace(-1, 1, 15)

    results = {
        "w_ipsi": [],
        "w_contra": [],
        "speed": [],
        "freq": [],
        "joint_amp": [],
        "torque": [],
        "cot": [],
        "energy": []
    }

    for w in w_vals:
        pylog.info(f"Running sim for w_ipsi={w:.2f}, w_contra={-w:.2f}")

        sim_pars = SimulationParameters(
            n_iterations=5001,
            controller="abstract oscillator",
            headless=True,
            return_network=True,
            drive=10,
            
            weights_body2body=0,  # no ipsi CPG
            # weights_body2body_contralateral=0,  # no contra CPG
            
            feedback_weights_ipsi=w,
            feedback_weights_contra=-w,
            
            cpg_amplitude_gain=motor_output_gains,
            compute_metrics='all',
            print_metrics=False,
            initial_phases=np.random.rand(26) * 2 * np.pi,
        )

        controller = run_single(sim_pars)

        results["w_ipsi"].append(w)
        results["w_contra"].append(-w)
        results["speed"].append(controller.metrics["mech_speed_fwd"])
        results["freq"].append(controller.metrics["neur_frequency"])
        results["joint_amp"].append(controller.metrics["mech_joint_amplitudes"])
        results["torque"].append(controller.metrics["mech_torque"])
        results["cot"].append(controller.metrics["mech_cot"])
        results["energy"].append(controller.metrics["mech_energy"])

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(results["w_ipsi"], results["speed"], marker='o')
    plt.title("Forward Speed vs $w_{ipsi}$ (with $w_{contra} = -w_{ipsi}$)")
    plt.xlabel("$w_{ipsi}$")
    plt.ylabel("Speed [m/s]")
    plt.grid()

    plt.figure(figsize=(10, 6))
    plt.plot(results["w_ipsi"], results["freq"], marker='o')
    plt.title("Neural Frequency vs $w_{ipsi}$")
    plt.xlabel("$w_{ipsi}$")
    plt.ylabel("Frequency [Hz]")
    plt.grid()

    plt.figure(figsize=(10, 6))
    plt.plot(results["w_ipsi"], results["joint_amp"], marker='o')
    plt.title("Joint Amplitude vs $w_{ipsi}$")
    plt.xlabel("$w_{ipsi}$")
    plt.ylabel("Amplitude [rad]")
    plt.grid()

    plt.figure(figsize=(10, 6))
    plt.plot(results["w_ipsi"], results["torque"], marker='o')
    plt.title("Torque vs $w_{ipsi}$")
    plt.xlabel("$w_{ipsi}$")
    plt.ylabel("Torque")
    plt.grid()

    plt.figure(figsize=(10, 6))
    plt.plot(results["w_ipsi"], results["cot"], marker='o')
    plt.title("Cost of Transport vs $w_{ipsi}$")
    plt.xlabel("$w_{ipsi}$")
    plt.ylabel("CoT")
    plt.grid()

    plt.figure(figsize=(10, 6))
    plt.plot(results["w_ipsi"], results["energy"], marker='o')
    plt.title("Energy vs $w_{ipsi}$")
    plt.xlabel("$w_{ipsi}$")
    plt.ylabel("Energy")
    plt.grid()

    plt.tight_layout()
    plt.show()




    
    

def exercise9():

    pylog.info("Ex 9")
    pylog.info("Implement exercise 9")
    log_path = './logs/exercise9/'  # path for logging the simulation data
    os.makedirs(log_path, exist_ok=True)

    # Run a single simulation with specific feedback weights and no ipsi coupling
    # First using contra CPG, as well as stretch feedback
    exercise9_0(contra_CPG=True, no_video=False, plot=True)
    
    # Run multiple simulations with varying feedback weights
    exercise9_1()

    # Run a single simulation with specific feedback weights and no ipsi coupling
    # Now without contra CPG
    exercise9_0(contra_CPG=False, no_video=False, plot=True)


if __name__ == '__main__':

    exercise9()

