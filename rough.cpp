#include <bits/stdc++.h>
using namespace std;

#define int             long long
#define double          long double
#define pb              push_back
#define all(t)          (t).begin(), (t).end()
#define rep(i,j)        for(int i = 0; i < (j); ++i)
#define rrep(i,j)       for(int i = (j)-1; i >= 0; --i)
typedef vector<int> vi;
typedef vector<vector<int> > vvi;
typedef vector<pair<int, int>> vpi;
const char nl = '\n';
const double eps = 1e-6;

    for(int i=0;i<n;i++){
        if(((n-i-1)*2)<v[i]) ans1=false;
    }
    for(int i=n-1;i>-1;i--){
        if((i*2)<v[i]) ans2=false;
    }
    if(ans1||ans2) yay;
    else nay;
    return;
}
   cin >> T;//Comment this out in case number of test cases are not to be taken as input.
    for(int I = 1; I <= T; I++) {
         
        solve(); 
    }
    return 0;
}
