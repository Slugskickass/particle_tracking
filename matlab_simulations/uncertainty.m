function [u] = uncertainty(a,loc,b)
%UNTITLED7 Summary of this function goes here
%   Detailed explanation goes here
loc(3) = loc(3)*a;
loc(5) = loc(5)*a;

u(1) = ((loc(3)^2)+(a^2)/12)/loc(1)+(8*pi*(loc(3)^4)*(b^2))/((a^2)*(loc(1)^2));
u(2) = ((loc(5)^2)+(a^2)/12)/loc(1)+(8*pi*(loc(5)^4)*(b^2))/((a^2)*(loc(1)^2));


end

