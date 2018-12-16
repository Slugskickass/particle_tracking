function [event] = photGauss(nphot,center,sigma)
%PHOTGAUSS Summary of this function goes here
%   Detailed explanation goes here

xc = mod(center(1),1); %calculate center of molecule
yc = mod(center(2),1); %calculate center of molecule
points = randn(nphot,2).*sigma;
points(:,1) = points(:,1) + xc-.5;
points(:,2) = points(:,2) + yc-.5;

event = hist3(points, {-5:1:5,-5:1:5});

end

