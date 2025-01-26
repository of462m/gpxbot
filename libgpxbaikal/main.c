#include <stdio.h>
#include <string.h>
#include <dirent.h>
#define _USE_MATH_DEFINES
#include <math.h>
#include <unistd.h>
#include <malloc.h>
#include "mylib.h"

int main(int argc, char *argv[]) {

	FILE *ff;
	DIR* dir;
	struct dirent *dir_ent;
	wpt cpoint,dpoint;
	region reg;
	sqr_region sreg;

/*
	dir = opendir("/home/taras");
	while ((dir_ent = readdir(dir))) {
		printf("%s\n",dir_ent->d_name);
	}
*/
	cpoint.lat=51.86503;
	cpoint.lon=104.74051;
	dpoint.lat=51.86662;
	dpoint.lon=104.74026;

	get_sqr_region(cpoint,400.0,&sreg);
	printf("%lf %lf\n", cpoint.lat, cpoint.lon);
	printf("%lf %lf\n", sreg.min.lat, sreg.min.lon);
	printf("%lf %lf\n", sreg.max.lat, sreg.min.lon);
	printf("%lf %lf\n", sreg.max.lat, sreg.max.lon);
	printf("%lf %lf\n", sreg.min.lat, sreg.max.lon);
	
	printf("[%i]\n",is_wpt_in_sqr_region(cpoint,sreg));
	printf("[%i]\n",is_wpt_in_sqr_region(dpoint,sreg));

	return 0;

//	ff = fopen("unconvex.dat","r");
	ff = fopen("kbzd.dat","r");
		fscanf(ff,"%i",&reg.n);
		reg.points = (wpt *)malloc(reg.n*sizeof(wpt));
		for(int i=0; i<reg.n; i++)
			fscanf(ff,"%lf %lf", &reg.points[i].lat, &reg.points[i].lon);
		is_wpt_in_region(cpoint,reg) ? printf("in\n") : printf("not in\n");
	fclose(ff);
	free(reg.points);

	return 0;
}
