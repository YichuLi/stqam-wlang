// returns an index of the largest element of array 'a' in the range [0..n)
method findMax (a : array<int>, n : int) returns (r:int)
requires 0<n<=a.Length;
ensures 0<=r<n;
ensures forall m :: 0<=m<n ==> a[r]>=a[m];
{
  var mi;
  var i;
  mi := 0;
  i := 0;
  while (i < n)
  invariant mi < n;
  invariant 0<=i<=n;
  invariant forall m :: 0<=m<i ==> a[mi]>=a[m];
  decreases n-i;
  {
    if (a[i] > a[mi])
    { mi := i; }
    i := i + 1;
  }
  return mi;
}
