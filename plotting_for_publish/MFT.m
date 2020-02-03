% This function calculate C(A) according to the MFT calculation
function C = MFT(A, sigma)
    if sigma == 0
        q = 0;
    else
        q = 0.5*erfc(1/(sqrt(2)*sigma));
    end
    a = 2*(1-q);
    C = (A-1+2/(a-1)).*log(0.5*(A-1)*(a-1)+1)/log(a) + A -(A-1)/(a-1);
end