
from util.run_closed_loop import run_single
from simulation_parameters import SimulationParameters
import os
import farms_pylog as pylog
import matplotlib.pyplot as plt
from plotting_common import plot_time_histories, plot_time_histories_multiple_windows, save_figures
import numpy as np


def exercise3():

    pylog.info("Ex 3")
    pylog.info("Implement exercise 3")
    log_path = './logs/exercise3/'  # path for logging the simulation data
    os.makedirs(log_path, exist_ok=True)

    all_pars = SimulationParameters(
        n_iterations=5001,
        controller="abstract oscillator",   
        log_path=log_path,
        compute_metrics='all',
        print_metrics= False,
        return_network=True,
        video_record = False,
        video_name = "simulation3",
        headless = False,
    )

    pylog.info("Running the simulation")
    controller = run_single(
        all_pars
    )

    # Hint: Optionally you can use some helper function to generate the plots
    # such as (plot_time_histories)

    #Plot the oscillator phases evolution
    plt.figure('Phase Evolution', figsize=[10, 8])
    plot_time_histories(controller.times,controller.state[:, :controller.n_oscillators], xlabel = "Time [s]", ylabel = "Phase [rad]")
    plt.title("Oscillator Phase Evolution")
    
    plt.figure('Amplitude Evolution', figsize=[10, 8])
    plot_time_histories(controller.times,controller.state[:,controller.n_oscillators:],xlabel = "Time [s]", ylabel = "Amplitude [m]")
    plt.title("Oscillator Amplitude Evolution")
    
    plt.figure('Motor Output', figsize=[10, 8])
    plot_time_histories(controller.times, controller.motor_out, xlabel = "Time [s]", ylabel = "Motor Output")
    plt.title("Motor Output") 
              
   
    plt.figure('Joint Angle Evolution', figsize=[10, 8])
    plot_time_histories(controller.times,controller.joints_positions, xlabel = "Time [s]", ylabel = "Angles [rad]")
    plt.title("Zebrafish Joint Angles")
    
    dmotor = controller.motor_out
    for i in range(np.size(controller.n_iterations)-1) :
        dmotor[i,:] = controller.motor_out[i+1,:]- controller.motor_output[i,:]
        
     
    plt.figure('Motor Output Difference', figsize=[10, 8])
    plot_time_histories(controller.times, dmotor, xlabel = "Time [s]", ylabel = "Motor Output Difference")
    plt.title("Motor Output Difference")  
    plt.show()    
    
    #save_figures()
    
if __name__ == '__main__':

    exercise3()

