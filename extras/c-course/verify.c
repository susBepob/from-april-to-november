#include <stdio.h>
int main(void){
  printf("B1 %d\n", 17/5);
  printf("B2 %d\n", 17%5);
  printf("B3 %d\n", (17/5)*5 + (17%5));
  printf("B4 %d\n", 45/10);
  printf("B5 %d %d\n", -9/2, -9%2);
  printf("B6 %d\n", 9%-2);
  printf("B7 %d\n", 5/10);
  int t=3725; printf("B8 %d %d %d\n", t/3600, (t%3600)/60, t%60);

  int c1 = 7/2.0; printf("C1 %d\n", c1);
  double c2 = 7/2; printf("C2 %f\n", c2);
  int c3 = 3.99; printf("C3 %d\n", c3);
  int c4 = -3.99; printf("C4 %d\n", c4);
  float c5 = 5/2; printf("C5 %.1f\n", c5);
  printf("C6 %d\n", 010);
  printf("C7 %d\n", 0x1F);
  printf("C8 %d\n", 1 + 2 * 3.0 == 7.0);

  printf("D1 %d\n", 2+3*4);
  printf("D2 %d\n", 10-2-3);
  printf("D3 %d\n", 100/10/2);
  printf("D4 %d\n", 2+10%3);
  printf("D5 %d\n", (2+10)%3);
  printf("D6 %d\n", 7+3*2-4/2);
  int a=2,b=3; printf("D7 %d\n", a*b+a);
  printf("D8 %d\n", 20-4*3+8/2);

  int i=5; int e1=i++; printf("E1 val=%d i=%d\n", e1, i);
  int j=5; int e2=++j; printf("E2 val=%d j=%d\n", e2, j);
  int x=10,y=4; x-=y++; printf("E3 x=%d y=%d\n", x,y);
  int x2=10,y2=4; x2-=++y2; printf("E4 x=%d y=%d\n", x2,y2);
  int p=2; int r=p++*3; printf("E5 r=%d p=%d\n", r,p);
  int p2=2; int r2=++p2*3; printf("E6 r=%d p=%d\n", r2,p2);
  int m=7; m+=3; m/=2; printf("E7 m=%d\n", m);
  int q=4; q*=q; printf("E8 q=%d\n", q);

  int s=0,k=1; s+=k++; s+=k++; s+=k++; printf("F1 s=%d k=%d\n", s,k);
  int n=100; n%=7; n*=2; n-=1; printf("F2 n=%d\n", n);
  int g=1,h=2,z; z=g=h; printf("F3 g=%d h=%d z=%d\n",g,h,z);
  int u=9; int v=u/2*2; printf("F4 v=%d\n", v);
  return 0;
}
