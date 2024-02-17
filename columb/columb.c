#include <stdio.h>
#include <math.h>

#define COULUMB_CONST 8.99e9

double columbForce(int case_type, double d1, double d2, double q1, double q2, double r_input) {
    double r = fabs(d2 - d1);
    double r_input_squared = r_input * r_input;

    switch (case_type) {
        case 1: // Electrical force between two point charges
            return (COULUMB_CONST * (q1 * q2)) / (r * r);

        case 2: // Electrical force between a plane and a point charge
            // Assume d1 is the distance from the plane to the charge
            return (COULUMB_CONST * q1 * q2) / (2 * d1);

        case 3: // Electrical force between a toroid and a point charge
            // Assume d1 is the radius of the toroid and d2 is the distance from the center of the toroid to the charge
            return (COULUMB_CONST * q1 * q2) / (2 * 3.1415 * d1 * d2);

        case 4:
            return (COULUMB_CONST * (q1 * q2)) / r_input_squared;

        default:
            printf("Invalid case type!\n");
            return 0.0; // Return 0.0 for invalid case type
    }
}
