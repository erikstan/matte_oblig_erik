import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Grid-størrelse og radius for ladningens sirkel
Nx, Ny = 100, 100
radius = 0.5

# Koordinater fra -1 til 1
x = np.linspace(-1, 1, Nx)
y = np.linspace(-1, 1, Ny)
X, Y = np.meshgrid(x, y)

# Beregn radius fra origo til hvert punkt
R = np.sqrt(X**2 + Y**2)

# Initialiser ladningsfordelingen
f = np.zeros((Ny, Nx))
f[Ny//2, Nx//2] = 1e5  # Punktladning i midten
f[R > radius] = 0  # Nullstill ladning utenfor sirkelen

# Diskretisering og initialisering av potensial
delta_x = 2.0 / (Nx - 1)
delta_x2 = delta_x**2
u = np.zeros((Ny, Nx))

# Konvergenskriterier
tolerance = 1e-4
max_iter = 10000
converged = False

for i in range(max_iter):
    u_old = u.copy()
    u[1:-1, 1:-1] = 0.25 * (u_old[1:-1, 2:] + u_old[1:-1, :-2] + u_old[2:, 1:-1] + u_old[:-2, 1:-1] - delta_x2 * f[1:-1, 1:-1])
    max_diff = np.max(np.abs(u - u_old))

    if max_diff < tolerance:
        converged = True
        break

print(f"Iterasjonen konvergerte: {converged} etter {i+1} iterasjoner.")

# Plotting av resultater
fig = plt.figure(figsize=(14, 6))

# 2D konturplot
ax1 = fig.add_subplot(121)
contour = ax1.contourf(X, Y, u, levels=50, cmap='viridis')
fig.colorbar(contour, ax=ax1)
ax1.set_title('Fordeling av elektrostatisk potensial rundt enkeltladning')
ax1.set_xlabel('X')
ax1.set_ylabel('Y')

# 3D overflateplott
ax2 = fig.add_subplot(122, projection='3d')
surf = ax2.plot_surface(X, Y, u, cmap='viridis', edgecolor='none')
fig.colorbar(surf, ax=ax2)
ax2.set_title('3D visning av elektrostatisk potensial rundt enkeltladning')
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_zlabel('Potensial U')

plt.show()