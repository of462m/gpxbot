#include <stdio.h>
#include <string.h>
#define _USE_MATH_DEFINES
#include <math.h>
#include <unistd.h>
#include <malloc.h>
#include "mylib.h"

void deg2rad(wpt *wpt) {
	wpt->lat = M_PI*wpt->lat/180.0;
	wpt->lon = M_PI*wpt->lon/180.0;
}

double geo_distance_m(wpt wpt1, wpt wpt2) {
	deg2rad(&wpt1);
	deg2rad(&wpt2);
	return 6371000.0 * acos(sin(wpt1.lat)*sin(wpt2.lat) + cos(wpt1.lat)*cos(wpt2.lat)*cos(wpt1.lon-wpt2.lon));
}

double geo2_distance_m(wpt *wpt1) {
	return geo_distance_m(wpt1[0],wpt1[1]);
}

double d_sign(double x) {
        if (x > 0.0) return 1.0;
        if (x < 0.0) return -1.0;
        return 0.0;
}

void get_vec(wpt a, wpt b, vec *res) {
	res->x = b.lon - a.lon;
	res->y = b.lat - a.lat;
	res->r = sqrt(pow(res->x,2.0) + pow(res->y,2.0));
}

double smult(vec a, vec b) {
	return a.x*b.x + a.y*b.y;
}

double get_dir(vec a,vec b) {
        return d_sign(a.x*b.y - a.y*b.x);
}

double get_phi(vec a, vec b) {
	double arg = smult(a,b) / (a.r*b.r);
	if (fabs(arg) > 1.0) arg = d_sign(arg);
	return get_dir(a,b) * acos(arg);
}

int is_wpt_in_sqr_region(wpt pt,sqr_region sreg) {
	if (pt.lat > sreg.min.lat)
		if (pt.lat < sreg.max.lat)
			if (pt.lon > sreg.min.lon)
				if (pt.lon < sreg.max.lon)
					return 1;
	return 0;
}

int is_trk_in_sqr_region(trk tr,sqr_region sreg) {
	for (int i=0; i<tr.n; i++) 
		if (is_wpt_in_sqr_region(tr.points[i],sreg))
			return 1;
	return 0;
}

int is_wpt_in_region(wpt pt,region reg) {
//	if (!is_wpt_in_sqr_region(pt,reg.bounds)) return 0;
	double angle = 0.0;
	vec v0,v,vnext;

	get_vec(pt,reg.points[0],&v0);
	v = v0;

        for(int i=1; i<reg.n; i++) {
                get_vec(pt,reg.points[i],&vnext);
                angle += get_phi(v,vnext);
		v = vnext;
        }

        angle += get_phi(v,v0);
	if (fabs(angle) < 1.0e-5) return 0;
	return 1;
}

int is_trk_in_region(trk tr,region reg) {
	for (int i=0; i<tr.n; i++)
		if (is_wpt_in_region(tr.points[i],reg))
			return 1;
	return 0;
}

void print_string(char *s) {
	printf("-----\n%s\n-----\n",s);
}
