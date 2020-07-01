#if !defined(BVEC_LIB)

// basic vector data struct
typedef struct bvec
{
    double x;
    double y;
    double z;
} bvec;

bvec            brief_createVec         (double x, double y);
bvec            brief_createVec3        (double x, double y, double z);
bvec            brief_copyVec           (bvec v);

double          brief_mag               (bvec * v);
double          brief_magSq             (bvec * v);
double          brief_heading           (bvec * v);

void            brief_printVec          (const bvec * v);
void            brief_normVec           (bvec * v);

void            brief_add               (bvec * v);
void            brief_sub               (bvec * v);
void            brief_div               (bvec * v);
void            brief_scl               (bvec * v);

void            brief_add_d             (double n);
void            brief_sub_d             (double n);
void            brief_div_d             (double n);
void            brief_scl_d             (double n);


#define BVEC_LIB
#endif

#if !defined(sqrt)
#include <math.h>
#endif

#if !defined(printf)
#include <stdio.h>
#endif

/** Creates a vector struct from the given data. The "z" coordinate is 0.*/
bvec brief_createVec(double x, double y) {
    bvec v = {x, y, 0};
    return v;
}

/** Creates a vector struct from the given data.*/
bvec brief_createVec3(double x, double y, double z) {
    bvec v = {x, y, z};
    return v;
}

/** Copies the given vector. */
bvec brief_copyVec(bvec v) {
    return brief_createVec3(v.x, v.y, v.z);
}

/** Prints the given vector struct. */
void brief_printVec(const bvec * v) {
    printf("(%f, %f, %f)", v->x, v->y, v->z);
}

/** Normalizes the given vector. */
void brief_normVec(bvec * v) {
    double mag = brief_mag(&(*v));
    v->x = v-> x / mag;
    v->y = v-> y / mag;
    v->z = v-> z / mag;
}

/** Returns the magnitude of the given vector. */
double brief_mag(bvec * v) {return sqrt(v->x * v->x + v->y * v->y + v->z * v->z);}

/** Return the magnitude, squared, of the given vector. */
double brief_magSq(bvec * v) {return pow(brief_mag(&(*v)), 2);}

/** Returns the heading of the given vector in radians. */
double brief_heading(bvec * v) {return atan2(v->y, v->x);}

