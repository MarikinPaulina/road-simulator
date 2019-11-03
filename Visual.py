import ipywidgets
from ipywidgets import interact, IntSlider
from IPython.display import display
import tqdm.autonotebook as tqdm
import matplotlib.pyplot as plt
import os
from tqdm.auto import tqdm as tqdm
import multiprocessing


def save_pic(tuple_of_arguments):
    segments, vertices, folder, name, title = tuple_of_arguments
    if folder is not None:
        os.makedirs(folder, exist_ok=True)

    fig, ax = plt.subplots(figsize=(15, 15))
    plt.ylim(-1, 1)
    ax.cla()
    ax.axis('equal')
    if title is not None:
        ax.set_title('Jednorodny kwadrat')
    ax.scatter(segments.T[0], segments.T[1], 4, 'k')
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


def save_pics(segments, indexes, vertices, F=0, folder=None, name=None, title=None):
    if folder is not None:
        os.makedirs(folder, exist_ok=True)
        arguments = []
        for f in range(F, len(vertices)):
            arguments.append((segments[f], vertices[f], folder, f"{name}_{f:04}.png", title))

        # with multiprocessing.Pool(2) as p:
        #     outs = list(p.imap(save_pic, arguments), total=len(arguments))
        #     for f in tqdm(range(F,len(segments))):
        #         save_pic(segments[f],vertices[f],folder,f"{name}_{f:04}.png",title)
        for f in tqdm(range(F, len(vertices))):
            arguments = (segments[:indexes[f]], vertices[f], folder, f"{name}_{f:04}.png", title)
            save_pic(arguments)


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
        ax.scatter(frame_segments[0], frame_segments[1], 0.05, 'k')

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


# def make_frame(f, animation_segments_f, animation_vertices_f, folder, len_animation_segments):
def make_frame(tuple_of_arguments):
    f, animation_segments_f, animation_vertices_f, folder, len_animation_segments = tuple_of_arguments
    fig, ax = plt.subplots()
    frame_segments = animation_segments_f.T
    frame_vertices = animation_vertices_f
    if frame_vertices.size > 0:
        ax.scatter(frame_vertices[:, 0], frame_vertices[:, 1])
    ax.scatter(frame_segments[0], frame_segments[1], 0.25, 'k')
    ax.set_title(f"Iteration {f}/{len_animation_segments - 1}")
    fig.savefig(os.path.join(folder, f"{f:06}.png"), dpi=400)
    plt.close(fig)


def save_frames(animation_segments, animation_vertices, folder, processes):
    os.makedirs(folder, exist_ok=True)

    arguments = []
    for f in range(len(animation_segments)):
        arguments.append((f, animation_segments[f], animation_vertices[f], folder, len(animation_segments)))

    with multiprocessing.Pool(processes) as p:
        list(tqdm(p.imap(make_frame, arguments), total=len(arguments)))
