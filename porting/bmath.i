%module bmath
%{

extern double bm_map(double n ,double start1, double stop1, double start2, double stop2);
extern double bm_clamp(double n, double min, double max);


%}

extern double bm_map(double n ,double start1, double stop1, double start2, double stop2);
extern double bm_clamp(double n, double min, double max);