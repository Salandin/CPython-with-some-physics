#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int TIME_STEPS = 400;
int NUM_SERIES = 1;

void pendulum_edo(double *y, double t){
    double g = 9.81, l = 1.0;
    double theta = y[0], omega = y[1];  // Assign theta and omega values from y array
    double dtheta = omega;
    double domega = -(g / l) * sin(theta);

    // Update the values of y array with dtheta and domega
    y[0] += dtheta;
    y[1] += domega;
};

int generate_pendulums() {    
    for (int i = 0; i < NUM_SERIES; i++) {
        char file_name[50];
        sprintf(file_name, "./dataset/pendulum_%d.csv", i); // Generate unique file name
        
        FILE *fp = fopen(file_name, "w");
        if (fp == NULL) {
            printf("Error opening file!\n");
            return 1;
        }
        
        for (int t = 0; t < TIME_STEPS; t++) {
            double theta = 0;
            double omega = 1.0 * 2 * (((double)rand()/RAND_MAX) - 0.5);
            fprintf(fp, "%f,%f\n", theta, omega);
        }
        
        fclose(fp);
    }
    
    return 0;
};