import matplotlib.pyplot as plt

def make_outside_legend(ax, vspace=-0.15, ncol=4):
    
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width, box.height * 0.9])

    # Put a legend to the bottom of the current axis
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, vspace),
      fancybox=False, shadow=False, ncol=ncol)
    
    plt.xlabel('')
    plt.ylabel('')
    
    return ax