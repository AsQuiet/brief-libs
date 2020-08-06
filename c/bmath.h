#if !defined(BMATH_LIB_H)
#define BMATH_LIB_H

double bm_map           (double n ,double start1, double stop1, double start2, double stop2);
double bm_clamp         (double n, double min, double max);

#endif

double bm_map(double n, double start1, double stop1, double start2, double stop2)
{
    return (n - start1) / (stop1 - start1) * (stop2 - start2) + start2;
}

double bm_clamp(double n, double min, double max)
{
    if (n < min)
        return min;
    
    if (n > max)
        return max;
    
    return n;
}

