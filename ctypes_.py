from ctypes import cdll, c_uint64


# int
c_file = """
long long func(long long n)
{
    long long result = 0;
    for(n;n>0;n--)
    {
        result += n/3 ;
    }
    return result;
}
"""
dll = cdll.LoadLibrary(r'g:\c.dll')
func = dll.func
func.argtypes = [c_uint64, ]
func.restype = c_uint64
print(func(2**30))
# char
# to be continue
