#include <iostream>
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <time.h>
#include <stdlib.h>

int main()
{
  srand(time(NULL));
  int fd = open("bible.txt", O_RDONLY, S_IRUSR);
  if (fd < 0)
  {
    printf("file not found.\n");
    return -1;
  }
  ssize_t n;
  char buffer[100000];
  while (true)
  {
    int r = rand() % 3500000;
    lseek(fd, r, SEEK_SET);
    n = read(fd, buffer, r + 100000);
  }
  return 0;
}