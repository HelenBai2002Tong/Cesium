def MAT(N,A):
    INVALID=False
    R=0
    while R<N and not INVALID:
        C=0
        while C<N and not INVALID:
            if abs(R-C)>=2 and A[R][C]!=0 or abs(R-C)<2 and A[R][C]==0:
                INVALID=True
        C=C+1
    R=R+1
    return (INVALID)
