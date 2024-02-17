#include <stdio.h>
#include <math.h>

#define G 6.67430e-11   // Gravitational constant
#define M_BLACK_HOLE 1.0e6  // Mass of the black hole
#define GAMMA 1.5
#define DISK_RADIUS 1.0e6  // Radius of the accretion disk
#define DISK_WIDTH 1.0e5  // Thickness of the accretion disk
#define SIGMA0 1.0e3  // Mass density at the edge of the accretion disk
#define P 0.5  // Power law index for the mass density distribution
#define K 3.0  // Polytropic constant

typedef struct {
    double x, y;  // Particle position (polar coordinates)
    double vx, vy;  // Particle velocity
} Particle;

// Function to calculate the surface density at radius r
double surface_density(double r) {
    return SIGMA0 * pow(r / DISK_RADIUS, -P);
}

// Function to calculate the gravitational potential at radius r
double gravitational_potential(double r) {
    return -G * M_BLACK_HOLE / r;
}

// Function to calculate the polytropic pressure
double polytropic_pressure(double rho) {
    return K * pow(rho, GAMMA);
}

// Function to calculate the pressure force at radius r
double pressure_force(double r) {
    double rho = surface_density(r);  // Mass density at radius r
    double p = polytropic_pressure(rho);  // Pressure at radius r
    double dp_dr = GAMMA * p / rho;  // Pressure gradient

    // Pressure force = - Pressure gradient
    return -dp_dr;
}

// Function to calculate the gravitational and pressure forces on a particle
void calculate_forces(Particle *particle, double r, double *fx, double *fy) {
    double r_squared = r*r;
    double potential = gravitational_potential(r);
    double pressure = pressure_force(r);

    // Calculate x and y components of gravitational and pressure forces
    *fx = potential * particle->x / r_squared - particle->x * pressure;
    *fy = potential * particle->y / r_squared - particle->y * pressure;
}

// Function to integrate the equations of motion using the fourth-order Runge-Kutta (RK4) method
void integrate_particle(Particle *particle, double dt, double fx, double fy, double particle_mass) {
    // Initial values of position and velocity
    double x0 = particle->x;
    double y0 = particle->y;
    double vx0 = particle->vx;
    double vy0 = particle->vy;

    // Calculate the first set of derivatives (k1)
    double k1_x = vx0;
    double k1_y = vy0;
    double k1_vx = fx / particle_mass;
    double k1_vy = fy / particle_mass;

    // Calculate the second set of derivatives (k2)
    double k2_x = vx0 + 0.5 * dt * k1_vx;
    double k2_y = vy0 + 0.5 * dt * k1_vy;
    double k2_vx = (fx + 0.5 * dt * k1_vx) / particle_mass;
    double k2_vy = (fy + 0.5 * dt * k1_vy) / particle_mass;

    // Calculate the third set of derivatives (k3)
    double k3_x = vx0 + 0.5 * dt * k2_vx;
    double k3_y = vy0 + 0.5 * dt * k2_vy;
    double k3_vx = (fx + 0.5 * dt * k2_vx) / particle_mass;
    double k3_vy = (fy + 0.5 * dt * k2_vy) / particle_mass;

    // Calculate the fourth set of derivatives (k4)
    double k4_x = vx0 + dt * k3_vx;
    double k4_y = vy0 + dt * k3_vy;
    double k4_vx = (fx + dt * k3_vx) / particle_mass;
    double k4_vy = (fy + dt * k3_vy) / particle_mass;

    // Update particle position and velocity using the RK4 algorithm
    particle->x = x0 + (dt / 6.0) * (k1_x + 2 * k2_x + 2 * k3_x + k4_x);
    particle->y = y0 + (dt / 6.0) * (k1_y + 2 * k2_y + 2 * k3_y + k4_y);
    particle->vx = vx0 + (dt / 6.0) * (k1_vx + 2 * k2_vx + 2 * k3_vx + k4_vx);
    particle->vy = vy0 + (dt / 6.0) * (k1_vy + 2 * k2_vy + 2 * k3_vy + k4_vy);
}