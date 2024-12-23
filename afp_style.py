# Assumes some styling is already handled by the stylesheet

def style_plot(plot,title,subtitle,source):
    plt = plot
    
    ## Set title and subtitle
    plt.suptitle(title,
                x=0.05,
                y=1.05,
                ha='left',
                fontsize=20,
                fontproperties={'family': 'Source Sans Pro'})
    
    plt.title(subtitle,
            x= -0.1,
            pad=5,
            fontsize=12,
            ha='left',
            fontproperties={'family': 'Source Sans Pro'})
    
    # Add source credit
    plt.figtext(0.05, 0.01, 
                f"Source: {source}", 
                ha="left", 
                fontsize=8)

    # Remove frame
    ax = plt.gca() # 'get current axes'
    ax.set_frame_on(False)

    # Set dashed grid lines
    ax.grid(axis="y", linestyle="--", color='black')

    # Make lowest Y tick a solid line
    baseline = ax.get_yticks()[0]
    # baseline = ax.get_yticks()[1] # if Y axis starts above 0
    plt.axhline(y=baseline, color='black', linewidth=.5, linestyle='-')

    # Override Y start and end point if needed
    # ax.set_ylim([10, 100])
    
    # Move legend to right if
    sp = plt.subplot(111)
    sp.legend(bbox_to_anchor=(1, 1))

    # Change Y tick format to insert commas
    yticks = ax.get_yticks()
    ax.set_yticklabels(['{:,.0f}'.format(t) for t in yticks])
    # Change Y tick format, e.g. from decimal to percentage
    # ax.set_yticklabels(['{:,.0%}'.format(x) for x in yticks])

    # Customize X ticks
    # Put x ticks in center of column
    plt.xticks(rotation=0, ha='center')
    # plt.tick_params(axis='x', somevalue='')
