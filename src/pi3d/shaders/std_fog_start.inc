//NB previousl (in std_head_vs.inc) define fog_start and unif[20]
  fog_start = fract(unif[5][0]);
  if (fog_start == 0.0) {
    fog_start = unif[5][0] * 0.333;
  } else {
    fog_start *= unif[5][0];
  }
