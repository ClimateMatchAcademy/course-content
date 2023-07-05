
# set initial temperature profile to be the surface temperature (isothermal)
rcm.state.Tatm[:] = rcm.state.Ts

# compute diagnostics
rcm.compute_diagnostics()

#  plot initial data
fig, lines = initial_figure(rcm)

# make animation
animation.FuncAnimation(fig, animate, 50, fargs=(rcm, lines))