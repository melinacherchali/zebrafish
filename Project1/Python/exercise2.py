
import os
import numpy as np
import matplotlib.pyplot as plt
import farms_pylog as pylog
from util.run_closed_loop import run_multiple
from util.rw import load_object
from simulation_parameters import SimulationParameters
from plotting_common import plot_1d, plot_2d, save_figures, plot_time_histories



def exercise2_2(plot=False, single_plot=True):
    pylog.info("Implement ex 2.2")
    log_path = './logs/exercise2/'
    os.makedirs(log_path, exist_ok=True)


    all_pars = [SimulationParameters(
        simulation_i=i,
        n_iterations=5001,
        log_path=log_path,
        compute_metrics=None,
        print_metrics=False,
        return_network=True, 
        headless=True, # if True, no GUI will be displayed
        gravity = np.array([0, 0, 0]),  # no gravity mode
        joint_poses = 0.3 * np.ones(15), # 0.3 because we want to start from a bent position
        animal_pose = [0.0, 0.0, 0.01, 0.0, 0, -1.570796327], # 10m above the ground (x,y,z,roll,pitch,yaw)
        damping_factor = damp, # damping factor for the joints
    )
        for i, damp in enumerate([0.1, 1, 3])
                
    ]               

    pylog.info("Running the simulation")

    controllers = run_multiple(all_pars, num_process=1)
    
    
    ## --------- PLOTS FOR 2.2 --------- ###
    
    if plot:
        
        if single_plot:
            plt.figure('Joint Angle Evolution - plot_1d', figsize=[12, 8])
            colors = plt.cm.viridis(np.linspace(0, 1, len(controllers)))

            for i, controller in enumerate(controllers):
                joint_mean = controller.joints[:, :, 0].mean(axis=1)
                result = np.stack([controller.times, joint_mean, np.zeros_like(joint_mean)], axis=1)
                
                plot_1d(
                    results=result, 
                    labels=['Time [s]', 'Mean Joint Angle [rad]', 'ignored'],
                    # cmap=colors[i]
                )

            # Add legend manually
            damping_labels = [f'Damping = {p.damping_factor}' for p in all_pars]
            for i in range(len(all_pars)):
                plt.plot([], [], '--', color=colors[i], label=damping_labels[i])  # dummy lines for legend

            plt.title('Mean Joint Angle Over Time for Different Damping Factors')
            plt.legend() 
            plt.grid()
            plt.tight_layout()
            plt.show()
            # save_figures()
        else:
            for i, controller in enumerate(controllers):
                # Time portrait with improved aesthetics
                plt.figure(f'Joint Angle Evolution - Damping = {all_pars[i].damping_factor}', figsize=[10, 8])
                
                plot_time_histories(
                    controller.times, 
                    controller.joints[:, :, 0], 
                    ylabel='Joint Angles [rad]', 
                    xlabel='Time [s]',
                    colors=plt.cm.jet(np.linspace(0, 1, controller.joints[:, :, 0].shape[1])).tolist()
                )
                
                plt.title(f'Joint Angles Evolution Over Time (Damping = {all_pars[i].damping_factor})', fontsize=18, pad=20)
                plt.grid()
                plt.tight_layout(pad=2.0)

                # Customize axis labels and ticks (make subplots cleaner)
                for ax in plt.gcf().get_axes()[1:]:
                    ax.set_yticklabels([])
                for ax in plt.gcf().get_axes()[:-1]:
                    ax.set_xticklabels([])

                # save_figures()
            plt.show()
            
    
def exercise2_3(drag=False, twl_value=0, n_points=5):
    
    
    
    pylog.info("Implement ex 2.3")
    log_path = './logs/exercise2/'
    os.makedirs(log_path, exist_ok=True)
    
    
    # Multiple simulations of the controller with fixed amplitude amp=0.01 
    # vary the controller frequency ∈ (0, 20) for TWL=0 (0 total wave lag)

    if drag:
        pose = [0.0, 0.0, -0.01, 0.0, 0, -1.570796327] # in water
    else:
        pose = [0.0, 0.0, 0.01, 0.0, 0, -1.570796327] # above ground
        
    damping_values = [0.1, 1, 3]
    freq_values = np.linspace(0, 20, 5) 
    nsim = len(freq_values) * len(damping_values)

    # === Generate parameter combinations ===
    all_pars = [SimulationParameters(
            controller="sine",
            amp=0.01,
            twl=twl_value,
            freq=F,
            simulation_i=i * nsim + j,
            n_iterations=5001,
            log_path=log_path,
            compute_metrics='all',
            print_metrics=False,
            return_network=True,
            headless=True,
            gravity=np.array([0, 0, 0]),
            joint_poses=0.3 * np.ones(15),
            animal_pose=pose,
            damping_factor=damp
        )
        for i, damp in enumerate(damping_values)
        for j, F in enumerate(freq_values)
    ]

    # === Run the simulations ===
    pylog.info("Running the simulation")
    controllers = run_multiple(all_pars, num_process=1)

    # === Group results by damping factor ===
    results_by_damping = {d: [] for d in damping_values}

    for i, controller in enumerate(controllers):
        damping = all_pars[i].damping_factor
        freq = all_pars[i].freq
        joint_amplitudes = controller.metrics["mech_joint_amplitudes"]
        mean_amplitude = np.mean(joint_amplitudes)
        results_by_damping[damping].append((freq, mean_amplitude))

    # === Plotting: One figure per (twl_value, drag) combo ===
    fig_name = f'Mean_Joint_Amplitude_vs_Freq_TWL_{twl_value}_Drag_{"On" if drag else "Off"}'
    plt.figure(fig_name, figsize=[10, 8])
    plt.suptitle(f'TWL = {twl_value}, Drag = {"On" if drag else "Off"}', fontsize=14, fontweight='bold')

    for damping, freq_amp_list in results_by_damping.items():
        freq_amp_list.sort()
        freqs, amplitudes = zip(*freq_amp_list)
        plt.plot(freqs, amplitudes, '-o', label=f'Damping = {damping}')

    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Mean Joint Amplitude')
    plt.title('Mean Joint Amplitude vs Frequency')
    plt.legend(fontsize='small')
    plt.grid(True)
    plt.tight_layout()
    
    # plt.show()

    # === Save all figures ===
    save_figures(folder='results', extensions=['png'])



    
    

def exercise2():

    pylog.info("Implement ex 2")
    log_path = './logs/exercise2/'
    os.makedirs(log_path, exist_ok=True)
    
    exercise2_3(drag=False, twl_value=0)
    exercise2_3(drag=True, twl_value=0)
    exercise2_3(drag=False, twl_value=0.5)
    exercise2_3(drag=True, twl_value=0.5)

    

    




if __name__ == '__main__':

    exercise2()

