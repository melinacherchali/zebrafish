
from util.run_closed_loop import run_single
from simulation_parameters import SimulationParameters
import matplotlib.pyplot as plt
import os
import farms_pylog as pylog
from util.rw import load_object
import numpy as np
import plotting_common

REF_JOINT_AMP = np.array([
    0.06580,
    0.02810,
    0.02781,
    0.03047,
    0.03623,
    0.04127,
    0.04864,
    0.05398,
    0.06508,
    0.08945,
    0.10271,
    0.11789,
    0.14929,
    0.0,      # Note: Tail moves passively,
    0.0,      # Note: Tail moves passively,
])  # type: ignore unit:radian


def plot_time_histories_multiple_windows_yaxisfixed(
    time: np.array,
    state: np.array,
    **kwargs,
):
    """
    Plot time histories of a vector of states on multiple subplots
    time: array of times
    state: array of states with shape (niterations,nvar)
    kwargs: optional plotting properties (see below)
    """

    xlabel = kwargs.pop('xlabel', "Time [s]")
    ylabel = kwargs.pop('ylabel', "Activity [-]")
    title = kwargs.pop('title', None)
    labels = kwargs.pop('labels', None)
    colors = kwargs.pop('colors', None)
    xlim = kwargs.pop('xlim', [0, time[-1]])
    ylim = kwargs.pop('ylim', None)
    savepath = kwargs.pop('savepath', None)
    lw = kwargs.pop('lw', 1.0)
    xticks = kwargs.pop('xticks', None)
    yticks = kwargs.pop('yticks', None)
    xticks_labels = kwargs.pop('xticks_labels', None)
    yticks_labels = kwargs.pop('yticks_labels', None)
    closefig = kwargs.pop('closefig', True)
    reference_values = kwargs.pop('reference_values', None)

    # Compute shared ylim if not provided
    if ylim is None:
        ymin = np.min(state)
        ymax = np.max(state)
        ylim = [ymin, ymax]

    if isinstance(colors, list) and len(colors) == state.shape[1]:
        colors = colors
    elif not isinstance(colors, list):
        colors = [colors for _ in range(state.shape[1])]
    else:
        raise Exception("Color list not a vecotor of the correct size!")

    n = state.shape[1]
    if title:
        plt.figure(title)
    for (idx, vector) in enumerate(state.transpose()):
        if not labels:
            label = None
        else:
            label = labels[idx]
        plt.subplot(n, 1, idx+1)
        plt.plot(time, vector, label=label, color=colors[idx], linewidth=lw)
        plt.ylabel(ylabel)
        plt.xlim(xlim)
        plt.ylim(ylim)

        if reference_values is not None:
            plt.axhline(y=reference_values[idx], color='gray', linestyle='--', linewidth=1)
        
    if labels:
        plt.legend()
    plt.xlabel(xlabel)
    plt.grid(False)
    if xticks:
        plt.xticks(xticks, labels=xticks_labels)
    if yticks:
        plt.yticks(yticks, labels=yticks_labels)
    if savepath:
        plt.savefig(savepath)
        if closefig:
            plt.close()


def exercise4():

    pylog.info("Implement ex 4")
    log_path = './logs/exercise4/'
    ex3_path = './logs/exercise3/'
    import shutil
    shutil.rmtree(log_path, ignore_errors=True)  # remove old logs
    os.makedirs(log_path, exist_ok=True)

    unoptimized_controller = load_object('{}controller{}'.format(ex3_path, 0))
    error_joint_amp = unoptimized_controller.metrics["mech_joint_amplitudes"] - REF_JOINT_AMP
    cpg_amplitude_gain = np.ones(REF_JOINT_AMP.shape) * 0.5  # initial guess
    cpg_amplitude_gain[-2:] = 0.0  # tail joints are not actuated

    trial = 1
    iter_max = 10

    while((np.abs(error_joint_amp) > 0.01).any() and (trial <= iter_max)):
        pylog.info(f"Trial {trial}")
        cpg_amplitude_gain *= (1 + 1.0 * (-1 + REF_JOINT_AMP / (error_joint_amp + REF_JOINT_AMP)))
        simulate(trial=trial, cpg_amplitude_gain=cpg_amplitude_gain[:-2], log_path=log_path)
        controller = load_object('{}controller{}'.format(log_path, trial))
        error_joint_amp = controller.metrics["mech_joint_amplitudes"] - REF_JOINT_AMP
        # print(error_joint_amp)
        trial += 1

    save_path = "./results/exercise4/"
    os.makedirs(save_path, exist_ok=True)

    # controller = load_object('{}controller{}'.format(log_path, 6))

    plt.figure('joint_angles_evolution_optimized', figsize=[8, 8])
    plot_time_histories_multiple_windows_yaxisfixed(controller.times, controller.joints[:,:,0], ylabel=None, xlabel=None, 
                                                         colors = plt.cm.jet(np.linspace(0, 1, controller.joints[:,:,0].shape[1])).tolist(),
                                                         reference_values=REF_JOINT_AMP.tolist())
    plt.gcf().text(0.04, 0.5, 'Joint angles [rad]', va='center', rotation='vertical')
    plt.gcf().text(0.5, 0.04, 'Time [s]', ha='center')
    for ax in plt.gcf().get_axes()[1:]:
        ax.set_yticklabels([])
    for ax in plt.gcf().get_axes()[:-1]:
        ax.set_xticklabels([])

    plt.figure('joint_amplitudes', figsize=[8, 8])
    plt.plot(np.linspace(0,15,15), controller.metrics["mech_joint_amplitudes"], label='Optimized joint amplitudes', color='green', ls='--', marker='o')
    plt.plot(np.linspace(0,15,15), REF_JOINT_AMP, label='Reference joint amplitudes', color='blue', ls='--', marker='D')
    plt.title("Joint Amplitudes")
    plt.xlabel("Joint position")
    plt.ylabel("Amplitude [rad]")
    plt.legend() 
    plt.grid()

    plotting_common.save_figures(folder=save_path)

    
    print("Unoptimized controller metrics:")
    print(unoptimized_controller.metrics)
    print()
    print("Optimized controller metrics:")
    print(controller.metrics)


def simulate(trial, cpg_amplitude_gain, log_path):
    '''
    Here is a template function which you can use for single trial of simulation

    trial: <int>
        number of optimization iteration
    mo_gains_axial_old: <np.array> of shape n_active_joints
        nominal amplitude gain of the network that you have to optimize so that
        the resulting joint kinematics match the reference data
    '''

    all_pars = SimulationParameters(
        log_path=log_path,
        simulation_i=trial,
        headless=True,
        compute_metrics="all",
        print_metrics=False,
        controller="abstract oscillator",  # abstract oscillator
        n_iterations=5001,
        drive=10,
        cpg_amplitude_gain=cpg_amplitude_gain,
        video_record=True,
        video_name="video_{}".format(trial),
        camera_id=1
    )

    _ = run_single(
        all_pars
    )

# Hint: to load a controller from simulation result, use:
# controller = load_object('{}controller{}'.format(log_path, trial))


if __name__ == '__main__':
    exercise4()

