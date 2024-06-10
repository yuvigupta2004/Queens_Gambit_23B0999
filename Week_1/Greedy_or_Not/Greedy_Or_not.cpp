#include<bits/stdc++.h>
using namespace std;




long long int sumRange(long long int arr[], int n, int i, int j) {
    long long int sum = 0;
    for (int k = i; k <= j; ++k) {
        sum += arr[k];
    }
    return sum;
}




int main(){

    long long int n;
    cin>>n;

    long long int nums[n];
    long long int ans[n][n];
    
    long long int sum=0;
    long long int prefix[n];



    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            ans[i][j] = 0;
        }
    }

    for (long long int i=0;i<n;i++){
        int k;
        cin>>k;
        nums[i]=k;
        sum = sum + k ;
        ans[i][i]=k;
        if (i==0)

    }

    for (int i=1; i<n; i++){
        for (int j=0;j<n-i-1;j++){
            if (j+i<n){
                ans[j][j+i] = sumRange(nums,n,j,j+i) - min(ans[j+1][i+j],ans[j][j+i-1]);
            }
        }
    }

    cout<<ans[0][n-1]<<"\n";


}