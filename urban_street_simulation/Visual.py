import ipywidgets
from ipywidgets import interact, IntSlider
from IPython.display import display
import tqdm.auto as tqdm
import matplotlib.pyplot as plt
import os
from tqdm.auto import tqdm as tqdm
import multiprocessing
from matplotlib import animation


# @profile
def save_pic(tuple_of_arguments):
    segments, vertices, folder, name, title = tuple_of_arguments
    if folder is not None:
        os.makedirs(folder, exist_ok=True)

    fig, ax = plt.subplots(figsize=(15, 15))
    plt.ylim(-1, 1)
    ax.cla()
    ax.axis('equal')
    if title is not None:
        ax.set_title(title)
    ax.scatter(segments.T[0], segments.T[1], 0.5, 'k')
    if vertices.size > 0:
        ax.scatter(vertices[:, 0], vertices[:, 1], s=200)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    plt.yticks(fontsize=0)
    plt.xticks(fontsize=0)
    plt.tick_params(axis="both", which="both", bottom=False, top=False,
                    labelbottom=True, left=False, right=False, labelleft=True)
    if folder is not None and name is not None:
        fig.savefig(os.path.join(folder, name), dpi=300)
        plt.close()


# @profile
def save_pics(segments, indexes, vertices, F=0, folder=None, name=None, title=None,
              animation_interval=30, border_offset=0.1):
    if folder is not None:
        os.makedirs(folder, exist_ok=True)
    arguments = []
    for f in range(F, len(vertices)):
        arguments.append((segments[:indexes[f]], vertices[f], folder, f"{name}_{f:04}.png", title))

        # with multiprocessing.Pool(2) as p:
        #     outs = list(p.imap(save_pic, arguments), total=len(arguments))
        #     for f in tqdm(range(F,len(segments))):
        #         save_pic(segments[f],vertices[f],folder,f"{name}_{f:04}.png",title)

    fig, ax = plt.subplots(figsize=(15, 15))
    if title is None:
        title = 'Jednorodny kwadrat'
    ax.set_title(title)
    ax.cla()

    segments_plot = ax.scatter([], [], 4, 'k')
    # if vertices.size > 0:
    vertices_plot = ax.scatter([], [], s=200)

    def init():
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.set_xlim(segments[:, 0].min() - border_offset, segments[:, 0].max() + border_offset)
        ax.set_ylim(segments[:, 1].min() - border_offset, segments[:, 1].max() + border_offset)
        ax.axis('equal')
        plt.yticks(fontsize=0)
        plt.xticks(fontsize=0)
        plt.tick_params(axis="both", which="both", bottom=False, top=False,
                        labelbottom=True, left=False, right=False, labelleft=True)
        return ax,

    def update(argument):
        segments, vertices, folder, name, title = argument
        segments_plot.set_offsets(segments)
        if vertices.size > 0:
            vertices_plot.set_offsets(vertices)
        return segments_plot, vertices_plot

    anim = animation.FuncAnimation(fig, update, frames=tqdm(arguments), init_func=init, blit=False,
                                   interval=animation_interval)
    anim.save(f'{folder}/{name}.mp4')
    plt.show()


# @profile
def animated_frames(animation_segments, animation_index, animation_vertices):

    plt.close()
    fig, ax = plt.subplots()
    ax.set_title("Iteration 0")

    def update(f: int = 0):
        ax.cla()
        frame_segments = animation_segments[:animation_index[f]].T
        frame_vertices = animation_vertices[f]
        if frame_vertices.size > 0:
            ax.scatter(frame_vertices[:, 0], frame_vertices[:, 1])
        # TODO optimize the line below - done?
        ax.scatter(frame_segments[0], frame_segments[1], 0.5, 'k')

        #         [ax.plot(segment[:, 0], segment[:, 1]) for segment in frame_segments]
        ax.axis('equal')
        # ax.set_ylim(-1,1)

        ax.set_title(f"Iteration {f}/{len(animation_index) - 1}")
        fig.canvas.draw()
    plt.show()

    play = ipywidgets.Play(
        interval=200,
        value=0,
        min=0,
        max=len(animation_index) - 1,
        step=1,
        description="Press play",
        disabled=False
    )

    slider = IntSlider(min=0, max=len(animation_index) - 1, step=1)
    ipywidgets.jslink((play, 'value'), (slider, 'value'))
    display(slider)
    return interact(update, f=play)
