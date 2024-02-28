havoc x;
assume x >= 0;
y := 0;
res := 0;

while x < 0
inv y <= x and res = 5 * y
do
{
    res := res + 5;
    y := y + 1
}
assert res = 5 * x