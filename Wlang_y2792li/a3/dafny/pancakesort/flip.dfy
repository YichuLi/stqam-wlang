// flips (i.e., reverses) array elements in the range [0..num]
method flip (a: array<int>, num: int)
requires 0 <= num < a.Length;
ensures forall k :: 0 <= k <= num ==> a[k] == old(a[num - k]);
ensures forall k :: num < k < a.Length ==> a[k] == old(a[k]);
ensures multiset(a[..]) == multiset(old(a[..]));
modifies a;
{
  var tmp:int;

  var i := 0;
  var j := num;
  while (i < j)
  decreases j - i;
  invariant 0 <= i <= num;
  invariant 0 <= j <= num;
  invariant i + j == num;
  invariant multiset(a[..]) == multiset(old(a[..]));
  invariant forall k :: 0 <= k < i ==> a[k] == old(a[num - k]);
  invariant forall k :: j < k <= num ==> a[k] == old(a[num - k]);
  invariant forall k :: i <= k <= j ==> a[k] == old(a[k]);
  invariant forall k :: num < k < a.Length ==> a[k] == old(a[k]);
  {
    tmp := a[i];
    a[i] := a[j];
    a[j] := tmp;
    i := i + 1;
    j := j - 1;
  }
}
