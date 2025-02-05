#ifndef _MYLIB_H_
#define _MYLIB_H_

typedef struct {
	double lat;
	double lon;
} wpt;

typedef struct {
	double x;
	double y;
	double r;
} vec;

typedef struct {
	int n;
//	sqr_region bounds;
	wpt *points;
} trk;

typedef struct {
	wpt min; // (min.lat,min.lon)
	wpt max; // (max.lat,max.lon)
} sqr_region;

typedef struct {
	int n;
	sqr_region bounds;
	wpt *points;
} region;
/*
REGION FILE FORMAT:
n - size of region array
min.lat min.lon max.lat max.lon - bounds
lat lon
lat lon
...
lat lon
*/

double geo_distance_m(wpt wpt1, wpt wpt2);
double geo2_distance_m(wpt *wpt1);

double d_sign(double x);
void deg2rad(wpt *wpt);

void get_vec(wpt a, wpt b, vec *res);
double smult(vec a, vec b);
double get_dir(vec a,vec b);
double get_phi(vec a, vec b);

void get_sqr_region(wpt pt, double side, sqr_region *sreg);

int is_wpt_in_sqr_region(wpt pt, sqr_region sreg);
int is_wpt_in_region(wpt pt, region reg);

int is_trk_in_sqr_region(trk tr, sqr_region sreg);
int is_trk_in_region(trk tr, region reg);

void print_string(char *s);

#endif /* !_MYLIB_H_ */
