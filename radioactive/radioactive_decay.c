#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define MAX_TIMESTEPS 150

double radioDecay(double N0, double Lambda, double t){
    return N0 * exp(-Lambda*t);
};

void simulateDecay(double N0, double Lambda, double dt, double *time_values, double *atom_values) {
    int i;
    double t = 0.0;
    for (i = 0; i < MAX_TIMESTEPS; i++) {
        time_values[i] = t;
        atom_values[i] = radioDecay(N0, Lambda, t);
        t += dt;
    };
};

void simulateDecayWithNoise(double N0, double Lambda, double dt, double total_time,
                             double *time_values, double *atom_values) {
    double t = 0.0;
    double N = N0;
    int i = 0;

    while (t < total_time && N > 0 && i < MAX_TIMESTEPS) {
        double decayed_fraction = ((double)rand() / RAND_MAX) * Lambda;
        double decayed_atoms = N * decayed_fraction;

        N -= decayed_atoms;
        time_values[i] = t;
        atom_values[i] = N;
        t += dt;
        i++;
    };
};