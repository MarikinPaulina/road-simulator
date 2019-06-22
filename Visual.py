def animated_frames(animation_segments, animation_vertices):
    import matplotlib.pyplot as plt
    import numpy as np
    import os
    import ipywidgets
    from ipywidgets import interact, IntSlider
    from IPython.display import display

    plt.close()
    fig, ax = plt.subplots()
    title = ax.set_title("Iteration 0")

    def update(f: int = 0):
        ax.cla()
        frame_segments = animation_segments[f].T
        #         frame_segments = animation_segments[f]
        frame_vertices = animation_vertices[f]
        if frame_vertices.size > 0:
            scatterplot = ax.scatter(frame_vertices[:, 0], frame_vertices[:, 1])
        # TODO optimize the line below - done?
        lines = ax.scatter(frame_segments[0], frame_segments[1],0.5,'k')

        #         lines = [ax.plot(segment[:, 0], segment[:, 1]) for segment in frame_segments]

        title = ax.set_title(f"Iteration {f}/{len(animation_segments) - 1}")
        fig.canvas.draw()

    #         fig.savefig(f"{folder}/{f:06}.png")
    plt.show()

    play = ipywidgets.Play(
        interval=200,
        value=0,
        min=0,
        max=len(animation_segments) - 1,
        step=1,
        description="Press play",
        disabled=False
    )

    slider = IntSlider(min=0, max=len(animation_segments) - 1, step=1)
    #     w = interactive()
    link = ipywidgets.jslink((play, 'value'), (slider, 'value'))
    display(slider)
    #     ipywidgets.HBox([play, slider])
    # 1.png
    return interact(update, f=play);


def save_frames(animation_segments, animation_vertices, folder):
    import matplotlib.pyplot as plt
    import numpy as np
    import os
    from tqdm.auto import tqdm as tqdm
    import os
    import psutil
    import multiprocessing
    process = psutil.Process(os.getpid())

    def make_frame(f, animation_segments_f, animation_vertices_f, folder, len_animation_segments):
        fig, ax = plt.subplots()
        frame_segments = animation_segments_f.T
        frame_vertices = animation_vertices_f
        if frame_vertices.size > 0:
            scatterplot = ax.scatter(frame_vertices[:, 0], frame_vertices[:, 1])
        lines = ax.scatter(frame_segments[0], frame_segments[1], 0.5, 'k')
        title = ax.set_title(f"Iteration {f}/{len_animation_segments - 1}")
        fig.savefig(os.path.join(folder, f"{f:06}.png"), dpi=400)

    os.makedirs(folder, exist_ok=True)

    for f in tqdm(range(len(animation_segments))):
        proc = multiprocessing.Process(target=make_frame, args=(f, animation_segments[f], animation_vertices[f], folder, len(animation_segments)))
        proc.daemon=True
        proc.start()
        proc.join()
