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
	wpt cpoint;
	region reg;

/*
	dir = opendir("/home/taras");
	while ((dir_ent = readdir(dir))) {
		printf("%s\n",dir_ent->d_name);
	}
*/
	cpoint.lat=51.86503;
	cpoint.lon=104.74051;

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
