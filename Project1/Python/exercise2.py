
import os
import numpy as np
import matplotlib.pyplot as plt
import farms_pylog as pylog
from util.run_closed_loop import run_multiple
from util.rw import load_object
from simulation_parameters import SimulationParameters
from plotting_common import plot_1d, plot_2d, save_figures


def exercise2():

    pylog.info("Implement ex 2")
    log_path = './logs/exercise2/'
    os.makedirs(log_path, exist_ok=True)



    all_pars = SimulationParameters(
        # controller="abstract oscillator",
        # amp=0.3,
        # twl=1,
        # freq=3,
        n_iterations=5001,
        log_path=prepath,
        compute_metrics=None,
        print_metrics=False,
        return_network=True, 
        headless=False, # if True, no GUI will be displayed
        gravity = np.array([0, 0, 0]),  # no gravity mode
        joint_poses = 0.3 * np.ones(15), # 0.3 because we want to start from a bent position
        animal_pose = [0.0, 0.0, 0.01, 0.0, 0, -1.570796327], # 10m above the ground (x,y,z,roll,pitch,yaw)
        damping_factor = 3, # damping factor for the joints
    )

    pylog.info("Running the simulation")
    controller = run_single(
        all_pars
    )

    # Time portrait with improved aesthetics
    plt.figure('Joint Angle Evolution', figsize=[10, 8])
    
    # Plot joint angle evolution with a colormap
    plot_time_histories(
        controller.times, 
        controller.joints[:, :, 0], 
        ylabel='Joint Angles [rad]', 
        xlabel='Time [s]',
        colors = plt.cm.jet(np.linspace(0, 1, controller.joints[:,:,0].shape[1])).tolist()
    )
    
    # Add title and adjust layout
    plt.title('Joint Angles Evolution Over Time (Damping Factor = 3)', fontsize=18, pad=20)
    # add grid
    plt.grid()
    # add legend
    # plt.legend(['Joint ' + str(i) for i in range(15)], loc='upper right')
    plt.tight_layout(pad=2.0)
    
    # Customize axis labels and ticks
    for ax in plt.gcf().get_axes()[1:]:
        ax.set_yticklabels([])
    for ax in plt.gcf().get_axes()[:-1]:
        ax.set_xticklabels([])
    
    save_figures()
    
    
    # phase portrait
    plt.figure('Phase Portrait', figsize=[10, 8])
    
    
    # Display the plot
    plt.show()

if __name__ == '__main__':

    exercise2()

