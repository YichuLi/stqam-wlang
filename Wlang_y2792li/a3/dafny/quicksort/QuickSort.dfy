include "part.dfy"


method qsort(a:array<int>, l:nat, u:nat)
  requires a != null;
  requires l <= u < a.Length;
  modifies a;

  ensures sorted_between(a, l, u+1);
  
{
  if (l < u) {
    var pivot := partition(a, l, u);
    qsort(a, l, pivot - 1);
    qsort(a, pivot + 1, u);
  }
}